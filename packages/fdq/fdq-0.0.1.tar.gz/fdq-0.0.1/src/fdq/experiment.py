import os
import sys
import json
import math
import torch
import wandb
import shutil
import argparse
import importlib
import funkybob
from tqdm import tqdm
from typing import List
from datetime import datetime
from lossFunctions import createLoss
from ui_functions import iprint, wprint
from optimizer import createOptimizer, set_lr_schedule
from misc import (
    remove_file,
    store_processing_infos,
    FCQmode,
    recursive_dict_update,
    DictToObj,
    replace_tilde_with_abs_path,
    save_train_history,
)


class fdqExperiment:
    def __init__(self, inargs: argparse.Namespace) -> None:
        self.inargs = inargs
        self.parse_and_clean_args()
        # ------------- GLOBALS ------------------------------
        self.project = self.exp_def.globals.project.replace(" ", "_")
        self.experimentName = self.experiment_file_path.split("/")[-1].split(".json")[0]
        self.funky_name = None
        self.checkpoint_frequency = self.exp_def.store.checkpoint_frequency
        self.mode = FCQmode()
        self.creation_time = datetime.now()
        self.finish_time = None
        self.run_time = None
        self.run_info = {}
        # ------------- Train parameters ------------------------------
        self.gradacc_iter = self.exp_def.train.args.get(
            "accumulate_grad_batches", default=1
        )
        self.useAMP = bool(self.exp_def.train.args.use_AMP)
        self.nb_epochs = self.exp_def.train.args.epochs
        # ------------- Train variables ------------------------------
        self.current_epoch = 0
        self.start_epoch = 0
        self.data = {}
        self.models = {}
        self.inference_model_paths = {}
        self.optimizers = {}
        self.lr_schedulers = {}
        self.losses = {}
        self.last_model_path = {}
        self.best_val_model_path = {}
        self.best_train_model_path = {}
        self.checkpoint_path = None
        self._results_dir = None
        self._test_dir = None
        self._valLoss = float("inf")
        self._trainLoss = float("inf")
        self.bestValLoss = float("inf")
        self.bestTrainLoss = float("inf")
        self.valLoss_per_ep: List[float] = []
        self.trainLoss_per_ep: List[float] = []
        self.new_best_train_loss = False  # flag to indicate if a new best epoch was reached according to train loss
        self.new_best_train_loss_ep_id = None
        self.new_best_val_loss = False  # flag to indicate if a new best epoch was reached according to val loss
        self.new_best_val_loss_ep_id = None
        self.early_stop_detected = False
        # ------------- MGMT attributes ------------------------------
        self.useTensorboard = self.exp_file.get("store", {}).get("tensorboard", False)
        self.tb_writer = None
        self.useWandb = self.exp_file.get("store", {}).get("use_wandb", False)
        self.wandb_project = self.exp_file.get("store", {}).get("wandb_project", None)
        self.wandb_entity = self.exp_file.get("store", {}).get("wandb_entity", None)
        self.wandb_key = self.exp_file.get("store", {}).get("wandb_key", None)
        self.wandb_initialized = False
        # ------------- SLURM ------------------------------
        slurm_job_id = os.getenv("SLURM_JOB_ID")
        if isinstance(slurm_job_id, str) and slurm_job_id.isdigit():
            self.is_slurm = True
            self.slurm_job_id = slurm_job_id
        else:
            self.is_slurm = False
            self.slurm_job_id = None
        self.previous_slurm_job_id = None
        # ------------- CUDA / CPU -------------------------
        if torch.cuda.is_available() and bool(self.exp_def.train.args.use_GPU):
            torch.cuda.empty_cache()
            self.device = torch.device("cuda")
            self.is_cuda = True
            iprint(
                f"CUDA available: {torch.cuda.is_available()}. NB devices: {torch.cuda.device_count()}"
            )
        else:
            wprint("NO CUDA available - CPU mode")
            self.device = torch.device("cpu")
            self.is_cuda = False

    def parse_and_clean_args(self):
        self.experiment_file_path = self.inargs.experimentfile

        with open(self.experiment_file_path, "r", encoding="utf8") as fp:
            try:
                self.exp_file = json.load(fp)
            except Exception as exc:
                raise ValueError(
                    f"Error loading experiment file {self.experiment_file_path} (check syntax?)."
                ) from exc

        self.globals = self.exp_file.get("globals")
        if self.globals is None:
            raise ValueError(
                f"Error: experiment file does not comply - please check template! {self.experiment_file_path}."
            )

        parent = self.globals.get("parent", {})
        # parent must be in same directory or defined with absolute path
        if parent is not None:
            if parent[0] == "/":
                self.parent_file_path = parent
            else:
                self.parent_file_path = os.path.abspath(
                    os.path.join(os.path.split(self.experiment_file_path)[0], parent)
                )

            if not os.path.exists(self.parent_file_path):
                raise FileNotFoundError(
                    f"Error: File {self.parent_file_path} not found."
                )

            with open(self.parent_file_path, "r", encoding="utf8") as fp:
                try:
                    parent_expfile = json.load(fp)
                except Exception as exc:
                    raise ValueError(
                        f"Error loading experiment file {self.parent_file_path} (check syntax?)."
                    ) from exc

            self.exp_file = recursive_dict_update(
                d_parent=parent_expfile, d_child=self.exp_file
            )

        else:
            self.parent_file_path = None
        replace_tilde_with_abs_path(self.exp_file)
        self.exp_def = DictToObj(self.exp_file)

    def setupData(self):
        for data_name, data_source in self.exp_def.data.items():
            processor_path = data_source.processor

            if not os.path.exists(processor_path):
                raise FileNotFoundError(f"Processor file not found: {processor_path}")

            parent_dir = os.path.dirname(processor_path)
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)

            module_name = os.path.splitext(os.path.basename(processor_path))[0]
            processor = importlib.import_module(module_name)
            self.data[data_name] = DictToObj(processor.createDatasets(self))

    def runEvaluator(self):
        evaluator_path = self.exp_def.test.evaluator

        if not os.path.exists(evaluator_path):
            raise FileNotFoundError(f"Evaluator file not found: {evaluator_path}")

        parent_dir = os.path.dirname(evaluator_path)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        module_name = os.path.splitext(os.path.basename(evaluator_path))[0]
        currentEvaluator = importlib.import_module(module_name)

        return currentEvaluator.createEvaluator(self)

    def createModel(self, instantiate=True):
        for model_name, model_source in self.exp_def.models:
            model_path = model_source.name

            if not os.path.exists(model_path):
                current_file_path = os.path.abspath(__file__)
                networks_dir = os.path.abspath(
                    os.path.join(os.path.dirname(current_file_path), "../networks/")
                )
                model_path = os.path.join(networks_dir, model_path)

                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model file not found: {model_path}")

            parent_dir = os.path.dirname(model_path)
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)

            module_name = os.path.splitext(os.path.basename(model_path))[0]
            model = importlib.import_module(module_name)
            if instantiate:
                self.models[model_name] = model.createNetwork(self).to(self.device)

    def copy_data_to_scratch(self):
        """
        Copy all datasets to scratch dir, and update the paths
        """

        def _mkdir(path):
            if not os.path.exists(path):
                os.makedirs(path)

        def _cp_files(paths, name):
            if paths is not None:
                if not isinstance(paths, list):
                    raise ValueError(f"{name} must be defined as a list!")

                try:
                    dst_path = os.path.join(self.clusterDataBasePath, name + "/")
                    _mkdir(dst_path)

                    for i, pf in enumerate(tqdm(paths, desc=f"Copying {name} files")):
                        new_path = os.path.join(dst_path, os.path.basename(pf))
                        os.system(f"rsync -au {pf} {new_path}")
                        paths[i] = new_path

                except Exception as exc:
                    raise ValueError(
                        f"Unable to copy {pf} to scratch location!"
                    ) from exc

        if self.clusterDataBasePath is None:
            return

        _mkdir(self.clusterDataBasePath)

        if self.dataBasePath is not None:
            try:
                dst_path = os.path.join(self.clusterDataBasePath, "base_path/")
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(self.dataBasePath, dst_path)
                self.dataBasePath = dst_path
            except Exception as exc:
                raise ValueError(
                    f"Unable to copy {self.dataBasePath} to scratch location!"
                ) from exc

        # if self.run_train: TODO
        _cp_files(self.trainFilesPath, "train_files_path")
        _cp_files(self.valFilesPath, "val_files_path")
        # if self.run_test or self.run_test_auto:
        _cp_files(self.testFilesPath, "test_files_path")

        iprint("----------------------------------------------------")
        iprint("Copy datasets to temporary scratch location... Done!")
        iprint("----------------------------------------------------")

    def prepareTrainLoop(self):
        train_path = self.exp_def.train.train_loop

        if not os.path.exists(train_path):
            raise FileNotFoundError(f"Training file not found: {train_path}")

        parent_dir = os.path.dirname(train_path)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)

        module_name = os.path.splitext(os.path.basename(train_path))[0]
        self.trainer = importlib.import_module(module_name)

        # try:
        #     self.train_function = importlib.import_module(
        #         f"trainings.{self.training_strategy}"
        #     )
        # except Exception as exc:
        #     raise ImportError(
        #         f"Error loading training strategy {self.training_strategy}."
        #     ) from exc

        # self.copy_data_to_scratch()

    def prepareTraining(self):
        self.mode.train()
        self.setupData()
        self.prepareTrainLoop()
        self.createModel()
        createOptimizer(self)
        set_lr_schedule(self)
        createLoss(self)

        if self.useAMP:
            self.scaler = torch.amp.GradScaler(device=self.device, enabled=True)

        if self.inargs.resume_path is not None:
            iprint(
                "--------------------------------------------------------------------------"
            )
            iprint(f"Loading checkpoint: {self.inargs.resume_pathh}")

            self.load_checkpoint(self.inargs.resume_path)

        self.cp_to_res_dir(file_path=self.experiment_file_path)

        if self.parent_file_path is not None:
            self.cp_to_res_dir(file_path=self.parent_file_path)

        store_processing_infos(self)

    @property
    def results_dir(self):
        if self._results_dir is None:
            dt_string = self.creation_time.strftime("%Y%m%d_%H_%M_%S")
            if self.funky_name is None:
                self.funky_name = next(iter(funkybob.RandomNameGenerator()))

            folder_name = f"{dt_string}__{self.funky_name}"

            if self.is_slurm:
                folder_name += f"__{self.slurm_job_id}"

            if self.is_slurm:
                res_base_path = self.exp_file.get("store", {}).get(
                    "cluster_results_path", None
                )
                if res_base_path is None:
                    raise ValueError("Error, cluster_results_path was not defined.")

            else:
                res_base_path = self.exp_file.get("store", {}).get("results_path", None)
                if res_base_path is None:
                    raise ValueError("Error, result path was not defined.")

                if res_base_path[0] == "~":
                    res_base_path = os.path.expanduser(res_base_path)

            self._results_dir = os.path.join(
                res_base_path, self.project, self.experimentName, folder_name
            )

            if not os.path.exists(self._results_dir):
                os.makedirs(self._results_dir)

        return self._results_dir

    @property
    def results_output_dir(self):
        if self._results_output_dir is None:
            self._results_output_dir = os.path.join(
                self.results_dir, "training_outputs"
            )
            if not os.path.exists(self._results_output_dir):
                os.makedirs(self._results_output_dir)
        return self._results_output_dir

    @property
    def test_dir(self):
        if self._test_dir is None:
            folder_name = self.creation_time.strftime("%Y%m%d_%H_%M_%S")
            if self.is_slurm:
                folder_name += f"__{self.slurm_job_id}"
            self._test_dir = os.path.join(self.results_dir, "test", folder_name)
            if not os.path.exists(self._test_dir):
                os.makedirs(self._test_dir)
        return self._test_dir

    @property
    def valLoss(self):
        return self._valLoss

    @valLoss.setter
    def valLoss(self, value):
        self._valLoss = value
        self.valLoss_per_ep.append(value)
        if not math.isnan(value):
            self.bestValLoss = min(self.bestValLoss, self._valLoss)
            self.new_best_val_loss = self.bestValLoss == value
            self.new_best_val_loss_ep_id = self.current_epoch

    @property
    def trainLoss(self):
        return self._trainLoss

    @trainLoss.setter
    def trainLoss(self, value):
        self._trainLoss = value
        self.trainLoss_per_ep.append(value)
        if not math.isnan(value):
            self.bestTrainLoss = min(self.bestTrainLoss, self._trainLoss)
            self.new_best_train_loss = self.bestTrainLoss == value
            self.new_best_train_loss_ep_id = self.current_epoch

    def cp_to_res_dir(self, file_path):
        fn = file_path.split("/")[-1]
        iprint(f"Saving {fn} to {self.results_dir}...")
        shutil.copyfile(file_path, f"{self.results_dir}/{fn}")

    def copy_files_to_test_dir(self, file_path):
        fn = file_path.split("/")[-1]
        iprint(f"Saving {fn} to {self.test_dir}...")
        shutil.copyfile(file_path, f"{self.test_dir}/{fn}")

    def load_checkpoint(self, path):
        """
        Load checkpoint to resume training.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Error, checkpoint file {path} not found.")

        try:
            checkpoint = torch.load(path)
            self.start_epoch = checkpoint["epoch"]
            self.trainLoss = checkpoint["train_loss"]
            self.valLoss = checkpoint["val_loss"]
            self.funky_name = checkpoint["funky_name"]
            self.previous_slurm_job_id = checkpoint.get("slurm_job_id")
        except Exception as exc:
            raise ValueError(f"Error loading checkpoint {path}.") from exc

        iprint(
            f"Loaded checkpoint {self.start_epoch}. Train loss: {self.trainLoss:.4f}, val loss: {self.valLoss:.4f}"
        )

        if self.start_epoch >= self.nb_epochs - 1:
            raise ValueError(
                f"Error, checkpoint epoch {self.start_epoch + 1} already reached defined nb epochs ({self.nb_epochs})."
            )

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

    def save_checkpoint(self):
        if self.checkpoint_frequency is None or self.checkpoint_frequency == 0:
            return

        if self.current_epoch % self.checkpoint_frequency != 0:
            return

        remove_file(self.checkpoint_path)
        self.checkpoint_path = os.path.join(
            self.results_dir, f"checkpoint_e{self.current_epoch}.fdqcpt"
        )

        iprint(f"Saving checkpoint to {self.checkpoint_path}")

        if self.optimizers == {}:
            optimizer_state = "No optimizers used"
        else:
            optimizer_state = {
                optim_name: optim.state_dict()
                for optim_name, optim in self.optimizers.items()
            }

        model_state = {
            model_name: model.state_dict() for model_name, model in self.models.items()
        }

        checkpoint = {
            "epoch": self.current_epoch,
            "model_state_dict": model_state,
            "optimizer": optimizer_state,
            "train_loss": self.trainLoss_per_ep[-1],
            "val_loss": self.valLoss_per_ep[-1],
            "funky_name": self.funky_name,
            "slurm_job_id": self.slurm_job_id,
        }

        torch.save(checkpoint, self.checkpoint_path)

    def save_current_model(self):
        """
        Store model including weights.
        This is run at the end of every epoch.
        """

        for model_name, model in self.models.items():
            if self.exp_def.store.get("save_last_model", False):
                remove_file(self.last_model_path.get(model_name))
                self.last_model_path[model_name] = os.path.join(
                    self.results_dir,
                    f"last_{model_name}_e{self.current_epoch}.fdqm",
                )
                torch.save(model, self.last_model_path[model_name])

            # new best val loss (default!)
            best_model_path = os.path.join(
                self.results_dir,
                f"best_val_{model_name}_e{self.current_epoch}.fdqm",
            )
            if (
                self.current_epoch == self.start_epoch
                or self.exp_def.store.get("save_best_val_model", False)
                and self.new_best_val_loss
            ):
                remove_file(self.best_val_model_path.get(model_name))
                self.best_val_model_path[model_name] = best_model_path
                torch.save(model, best_model_path)

            # save best model according to train loss
            # this might be useful if we use dummy validation losses like in diffusion
            best_train_model_path = os.path.join(
                self.results_dir,
                f"best_train_{model_name}_e{self.current_epoch}.fdqm",
            )
            if (
                self.current_epoch == self.start_epoch
                or self.exp_def.store.get("save_best_train_model", False)
                and self.new_best_train_loss
            ):
                remove_file(self.best_train_model_path.get(model_name))
                self.best_train_model_path[model_name] = best_train_model_path
                torch.save(model, best_train_model_path)

    def load_models(self):
        self.createModel(instantiate=False)
        for model_name, _ in self.exp_def.models:
            path = self.inference_model_paths[model_name]
            iprint(f"Loading model {model_name} from {path}")
            self.models[model_name] = torch.load(path, weights_only=False).to(
                self.device
            )
            self.models[model_name].eval()

    def dump_model(self, res_folder=None):
        # https://pytorch.org/tutorials/advanced/cpp_export.html
        iprint("Start model dumping")

        example = torch.rand(
            1, self.nb_in_channels, self.net_input_size[0], self.net_input_size[1]
        ).to(self.device)

        # jit tracer to serialize model using example
        # this only works if there is no flow control applied in the model.
        # otherwise, the model has to be annotated and the torch script compiler applied.
        traced_script_module = torch.jit.trace(self.model, example)

        # test network
        # test_out = traced_script_module(example)
        # print(test_out)

        iprint(f"Storing model to {os.path.join(res_folder, 'serialized_model.fdqpt')}")
        traced_script_module.save(os.path.join(res_folder, "serialized_model.fdqpt"))

    def get_next_export_fn(self, name=None, file_ending="jpg"):
        if self.mode.is_test():
            if name is None:
                path = os.path.join(
                    self.test_dir, f"test_image_{self.test_output_id:02}.{file_ending}"
                )
            else:
                path = os.path.join(
                    self.test_dir,
                    f"test_image_{self.test_output_id:02}__{name}.{file_ending}",
                )

            self.test_output_id += 1

        else:
            if name is None:
                path = os.path.join(
                    self.results_output_dir,
                    f"out_e{self.current_epoch:02}_{self.train_output_id:02}.{file_ending}",
                )
            else:
                path = os.path.join(
                    self.results_output_dir,
                    f"out_e{self.current_epoch:02}_{self.train_output_id:02}__{name}.{file_ending}",
                )
            self.train_output_id += 1

        return path

    def print_dataset_infos(self):
        iprint("-------------------------------------------")
        if self.valset_is_train_subset:
            iprint("Validation set is a subset of the training set.")
            iprint(f"Validation subset ratio: {self.val_from_train_ratio}")
        iprint(f"Nb samples train: {self.trainset_size}")
        iprint(f"Train subset: {self.train_subset}")
        iprint(f"Nb samples val: {self.valset_size}")
        iprint(f"Validation subset: {self.val_subset}")
        iprint(f"Nb samples test: {self.testset_size}")
        iprint(f"Test subset: {self.test_subset}")
        iprint("-------------------------------------------")

    def clean_up(self):
        iprint("-------------------------------------------")
        iprint("Training done!\nCleaning up..")
        iprint("-------------------------------------------")
        if self.useTensorboard:
            self.tb_writer.close()

        if self.wandb_initialized:
            wandb.finish()

        store_processing_infos(self)

    def check_early_stop(self):
        """
        1) Stop training if the validation los over last last N epochs did not further decrease.
        We want at least N epochs in each training start, also if its a resume from checkpoint training.
        (--> Therefore, (cur_epoch - self.start_epoch) > self.early_stop_val_loss)

        2) Stop training if the loss is NaN for N epochs.
        """
        e_stop_nan = self.exp_def.train.args.early_stop_nan
        e_stop_val = self.exp_def.train.args.early_stop_val_loss
        e_stop_train = self.exp_def.train.args.early_stop_train_loss

        # early stop NaN ?
        if e_stop_nan is not None:
            if all(math.isnan(x) for x in self.trainLoss_per_ep[-e_stop_nan:]):
                self.early_stop_nan_detected = "NaN detected"
                wprint(
                    "\n###############################\n"
                    f"!! Early Stop NaN EP {self.current_epoch} !!\n"
                    "###############################\n"
                )
                return True

        # early stop val loss?
        # did we have a new best val loss within the last N epochs?
        # we want at least N losses
        if e_stop_val is not None and len(self.valLoss_per_ep) >= e_stop_val:
            # was there a new best val loss within the last N epochs?
            if min(self.valLoss_per_ep[-e_stop_val:]) != self.bestValLoss:
                self.early_stop_nan_detected = "ValLoss_stagnated"
                wprint(
                    "\n###############################\n"
                    f"!! Early Stop Val Loss EP {self.current_epoch} !!\n"
                    "###############################\n"
                )
                return True

        # early stop train loss?
        elif e_stop_train is not None and len(self.trainLoss_per_ep) >= e_stop_train:
            if min(self.trainLoss_per_ep[-e_stop_train:]) != self.bestTrainLoss:
                wprint(
                    "\n###############################\n"
                    f"!! Early Stop Train Loss EP {self.current_epoch} !!\n"
                    "###############################\n"
                )
                self.early_stop_nan_detected = "TrainLoss_stagnated"
                return True

        return False

    def update_gradients(self, b_idx, loader_name, model_name):
        length_loader = self.data[loader_name].n_train_batches

        if ((b_idx + 1) % self.gradacc_iter == 0) or (b_idx + 1 == length_loader):
            if self.useAMP:
                self.scaler.step(self.optimizers[model_name])
                self.scaler.update()
            else:
                self.optimizers[model_name].step()

            self.optimizers[model_name].zero_grad()

    def finalize_epoch(self):
        # update learning rate
        for model_name in self.models:
            scheduler = self.lr_schedulers[model_name]
            if scheduler is not None:
                current_LR = scheduler.get_last_lr()
                scheduler.step()
                new_LR = scheduler.get_last_lr()
                if current_LR != new_LR:
                    iprint(f"Updating LR of {model_name} from {current_LR} to {new_LR}")

        # end of last epoch
        if self.current_epoch == self.nb_epochs - 1:
            self.finish_time = datetime.now()
            store_processing_infos(self)

        try:
            self.run_time = datetime.now() - self.creation_time
            td = self.run_time
            run_t_string = f"days: {td.days}, hours: {td.seconds // 3600}, minutes: {td.seconds % 3600 / 60.0:.0f}"
            iprint(f"Current run time: {run_t_string}")
            store_processing_infos(self)
        except Exception:
            pass

        save_train_history(self)
        self.save_checkpoint()
        self.save_current_model()
