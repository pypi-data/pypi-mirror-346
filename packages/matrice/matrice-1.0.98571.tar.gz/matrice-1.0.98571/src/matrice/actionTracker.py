import math
import os
import sys
import time
import requests
from PIL import Image
import gc
import io
import subprocess

from matrice.session import Session
from matrice.dataset import Dataset
from matrice.utils import log_error
from matrice.model_store import ModelFamily, ModelArch
from matrice.projects import Projects

class _dotdict(dict):
    """
    A dictionary subclass that allows dot notation access to its attributes.

    This class enables both standard dictionary key access and dot notation access for easier manipulation
    of data attributes. It can be particularly useful for handling configuration parameters or other data
    structures where attributes are frequently accessed.

    Example
    -------
    >>> my_dict = _dotdict({'key': 'value'})
    >>> print(my_dict.key)  # Outputs: value
    >>> print(my_dict['key'])  # Outputs: value

    Parameters
    ----------
    initial_data : dict, optional
        An optional dictionary to initialize the `_dotdict`. If provided, the items will be added to the `_dotdict`.

    Attributes
    ----------
    None

    Methods
    -------
    __getattr__(key)
        Retrieves the value associated with the given key using dot notation.

    __setattr__(key, value)
        Sets the value for the given key using dot notation.

    __delattr__(key)
        Deletes the specified key from the dictionary using dot notation.

    Examples
    --------
    >>> my_dict = _dotdict({'name': 'Alice', 'age': 30})
    >>> print(my_dict.name)  # Outputs: Alice
    >>> my_dict.location = 'Wonderland'
    >>> print(my_dict['location'])  # Outputs: Wonderland
    >>> del my_dict.age
    >>> print(my_dict)  # Outputs: _dotdict({'name': 'Alice', 'location': 'Wonderland'})
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class LocalActionTracker:
    pass


class ActionTracker:
    """
    Tracks and manages the status, actions, and related data of a model's lifecycle, including training, evaluation, and deployment processes.

    The `ActionTracker` is responsible for tracking various stages of an action (e.g., model training, evaluation, or deployment),
    logging details, fetching configuration parameters, downloading model checkpoints, and handling error logging.
    It interacts with the backend system to retrieve and update action statuses.

    Parameters
    ----------
    action_id : str, optional
        The unique identifier of the action to be tracked. If not provided, the class will initialize without an active action.
        The `action_id` is typically linked to specific activities such as model training, evaluation, or deployment.

    Attributes
    ----------
    rpc : RPCClient
        A Remote Procedure Call (RPC) client for interacting with the backend API.
    action_id : bson.ObjectId
        The ObjectId representing the action being tracked. This is used for retrieving action details from the backend.
    action_id_str : str
        The string representation of the `action_id`.
    action_doc : dict
        The detailed document containing information about the action, including its status, type, and related model details.
    action_type : str
        The type of action being tracked, such as 'model_train', 'model_eval', or 'deploy_add'.
    _idModel : bson.ObjectId
        The ObjectId of the model associated with the current action.
    _idModel_str : str
        The string representation of `_idModel`.
    session : Session
        A session object that manages the user session and ensures that API requests are authorized.

    Examples
    --------
    >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
    >>> tracker.get_job_params()
    >>> tracker.update_status("training", "in_progress", "Model training started")
    >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
    """

    def __init__(self, action_id=None):
        """
        Initializes the ActionTracker instance and retrieves details related to the specified action ID.

        This constructor fetches the action document, which contains metadata about the action, including the model's ID.
        If no `action_id` is provided, the tracker is initialized without an action.

        Parameters
        ----------
        action_id : str, optional
            The unique identifier of the action to track. If not provided, the instance is initialized without an action.

        Raises
        ------
        ConnectionError
            If there is an error retrieving action details from the backend.
        SystemExit
            If there is a critical error during initialization, causing the system to terminate.

        Examples
        --------
        >>> tracker = ActionTracker(action_id="60f5f5bfb5a1c2a123456789")
        >>> print(tracker.action_type)  # Outputs the action type, e.g., "model_train"
        """
        try:
            self.session = Session(
                account_number="",
                secret_key=os.environ["MATRICE_SECRET_ACCESS_KEY"],
                access_key=os.environ["MATRICE_ACCESS_KEY_ID"],
            )
            self.rpc = self.session.rpc

            # If no action_id provided, initialize empty tracker
            if action_id is None:
                self.action_id = None
                print("ActionTracker initialized but no action found")
                return

            self._init_action_tracker_attributes(action_id)
            self._init_action_details()
            self._refresh_session()
            self._init_export_format_info()
            self.job_params = self.get_job_params()
            self._init_model_id()
            self._init_checkpoint_path()
            self._init_project_info()

        except Exception as e:
            log_error(__file__, "__init__", str(e))
            self.update_status("error", "error", "Initialization failed")
            sys.exit(1)

    def _init_action_tracker_attributes(self, action_id):
        self.action_start_time = time.time()
        self.epochs_times = []
        self.last_epoch_time = None
        self.action_id = action_id
        self.action_id_str = str(self.action_id)
        self.num_inference_samples = 0

    def _init_action_details(self):
        url = f"/v1/project/action/{self.action_id_str}/details"
        self.action_doc = self.rpc.get(url)["data"]
        self.action_details = self.action_doc["actionDetails"]
        self.action_type = self.action_doc["action"]

    def _refresh_session(self):
        try:
            self.session.update(project_id=self.action_doc["_idProject"])
        except Exception as e:
            print("Update project error:", e)

    def _init_project_info(self):
        self.project = Projects(self.session, project_id=self.action_doc['_idProject'])
        self.project_type = self.project.output_type

    def _init_export_format_info(self):
        self.export_format = ""
        if self.action_type == "model_export":
            self.is_exported = False
            if isinstance(self.action_details.get("exportFormats"), list):
                self.export_format = self.action_details["exportFormats"][0]
            else:
                self.export_format = self.action_details.get("exportFormat") or self.action_details.get("runtimeFramework") or "" 
        else:
            self.export_format = self.action_details.get("exportFormat") or self.action_details.get("runtimeFramework") or ""
            self.is_exported = self.export_format.lower() not in ["pytorch", "tensorflow", ""]

    def _init_model_id(self):
        if self.action_type in ("model_train", "model_eval"):
            self._idModel = self.action_doc["_idService"]
        elif self.action_type == "deploy_add":
            self.server_type = self.action_details["server_type"].lower()
            self._idModel = self.action_details["_idModelDeploy"]
        else:
            self._idModel = self.action_details["_idModel"]
        self._idModel_str = str(self._idModel)

    def _init_checkpoint_path(self):
        try:
            self.checkpoint_path, self.pretrained = self.get_checkpoint_path(
                self.job_params
            )
        except Exception as e:
            print("Get checkpoint error:", e)

    def log_error(self, filename, function_name, error_message):
        log_error(filename, function_name, error_message)

    def get_checkpoint_path(self, overrides={}):
        """
        Determines the checkpoint path for the model based on the configuration provided.

        This function checks if the model's checkpoint should be retrieved from a pre-trained source or a specific model ID.
        It also handles downloading the model if necessary.

        Parameters
        ----------
        overrides : dict
            A dictionary containing configuration parameters to override the default job parameters,
            such as `checkpoint_type` and `checkpoint_value`.

        Returns
        -------
        tuple
            A tuple containing:
            - The absolute path of the model checkpoint if found, None otherwise
            - A boolean indicating whether the model is pre-trained

        Raises
        ------
        FileNotFoundError
            If the model checkpoint cannot be downloaded or located
        ConnectionError
            If there is an issue communicating with the model's API
        ValueError
            If an invalid checkpoint type is provided

        Examples
        --------
        >>> config = {"checkpoint_type": "model_id", "checkpoint_value": "12345abcde"}
        >>> checkpoint_path, is_pretrained = tracker.get_checkpoint_path(config)
        >>> print(checkpoint_path, is_pretrained)
        """
        try:
            # Setup checkpoint directory
            checkpoint_dir = "./checkpoints"
            os.makedirs(checkpoint_dir, exist_ok=True)

            # Get checkpoint configuration
            checkpoint_type = self.action_details.get(
                "checkpoint_type",
                self.job_params.get("checkpoint_type", "")
            ).lower()
            checkpoint_value = self.action_details.get(
                "checkpoint_value",
                self.job_params.get("checkpoint_value", "")
            ).lower()

            if overrides: # Apply overrides
                checkpoint_type = overrides.get("checkpoint_type", checkpoint_type)
                checkpoint_value = overrides.get("checkpoint_value", checkpoint_value)

            # Handle different checkpoint types
            if checkpoint_type == "model_id":
                if not checkpoint_value:
                    raise ValueError("checkpoint_value is required for model_id type")
                model_path = os.path.join(checkpoint_dir, f"{checkpoint_value}.pt")
                success = self.download_model(
                    model_path=model_path,
                    model_type="trained" if not self.is_exported else "exported",
                    model_id=checkpoint_value,
                )
                if not success:
                    raise Exception("Failed to download model")
                return model_path, True

            elif checkpoint_type == "url":
                if not checkpoint_value:
                    raise ValueError("checkpoint_value is required for url type")
                filename = checkpoint_value.split("?")[0].split("/")[-1]
                model_path = os.path.join(checkpoint_dir, filename)
                try:
                    response = requests.get(checkpoint_value, timeout=30)
                    response.raise_for_status()
                    with open(model_path, "wb") as f:
                        f.write(response.content)
                    return model_path, True
                except (requests.RequestException, IOError) as e:
                    log_error(__file__, "get_checkpoint_path", f"Failed to download from URL: {str(e)}")
                    raise Exception(f"Failed to download from URL: {str(e)}")

            elif checkpoint_type in ["predefined", "pretrained"]:
                return None, checkpoint_value or True

            elif checkpoint_type in ["", "none"]:
                return None, checkpoint_value or False

            else:
                raise ValueError(f"Invalid checkpoint type: {checkpoint_type}")

        except Exception as e:
            log_error(__file__, "get_checkpoint_path", str(e))
            print(f"Exception in get_checkpoint_path: {str(e)}")
            return None, False

    def get_job_params(self):
        """
        Fetches the parameters for the job associated with the current action.

        This method retrieves the parameters required to perform a specific action, such as model training or evaluation.
        The parameters are returned as a dot-accessible dictionary (`_dotdict`) for convenience.

        Returns
        -------
        _dotdict
            A dot-accessible dictionary containing the job parameters.

        Raises
        ------
        KeyError
            If the job parameters cannot be found in the action document.
        SystemExit
            If the job parameters cannot be retrieved and the system needs to terminate.

        Examples
        --------
        >>> job_params = tracker.get_job_params()
        >>> print(job_params.learning_rate)  # Accessing parameters using dot notation
        """
        try:
            self.jobParams = self.action_doc["jobParams"]
            return _dotdict(self.jobParams)
        except Exception as e:
            log_error(__file__, "get_job_params", str(e))
            print(f"Exception in get_job_params: {str(e)}")
            self.update_status("error", "error", "Failed to get job parameters")
            sys.exit(1)

    def update_status(self, stepCode, status, status_description):
        """
        Updates the status of the tracked action in the backend system.

        This method allows changing the action's status, such as from "in progress" to "completed" or "error".
        It logs the provided message with the updated status.

        Parameters
        ----------
        action_name : str
            The name of the action being tracked (e.g., "training", "evaluation").
        status : str
            The new status to set for the action (e.g., "in_progress", "completed", "error").
        message : str
            A message providing context about the status update.

        Returns
        -------
        None

        Examples
        --------
        >>> tracker.update_status("training", "completed", "Training completed successfully")
        """
        try:
            print(status_description)
            url = "/v1/project/action"

            payload = {
                "_id": self.action_id_str,
                "action": self.action_type,
                "serviceName": self.action_doc["serviceName"],
                "stepCode": stepCode,
                "status": status,
                "statusDescription": status_description,
            }

            if status.lower() == "success":
                self._log_action_benchmark_results()
                self._clear_cache()
            else:
                if not self._check_gpu():
                    print("ERROR: NO GPU")
                    # payload['status'] = "SCLS_QUE_PROC"
                    # payload['statusDescription'] = "NO GPU"
                    # self.rpc.put(path=url, payload=payload)
                    # sys.exit(1) TODO enable after fixing gpu usage bug

            self.rpc.put(path=url, payload=payload)

        except Exception as e:
            log_error(__file__, "update_status", str(e))
            print(f"Exception in update_status: {str(e)}")

    def _check_gpu(self):
        """
        Function to check if the system has a GPU
        """
        if self.action_type != "data_prep" and self.action_details.get("gpuRequired", False):
            try:
                subprocess.check_output('nvidia-smi', stderr=subprocess.STDOUT)
                return True
            except Exception:
                return False

    def _log_action_benchmark_results(self):
        def get_batch_size():
            batch_params = {
                k: v for k, v in self.job_params.items() if "batch" in k.lower()
            }
            batch_size = (
                self.job_params.get("batch_size")
                or self.job_params.get("batch")
                or next(iter(batch_params.values()), 1)
                or 1
            )
            return batch_size

        def get_dataset_num_images():
            dataset_id = self.action_details.get("_idDataset")
            dataset_version = self.action_details.get("datasetVersion", "v1.0")
            dataset = Dataset(self.session, dataset_id=dataset_id)
            dataset_num_images = [
                version_stats["versionStats"]["total"]
                for version_stats in dataset.dataset_details["stats"]
                if version_stats["version"] == dataset_version
            ][0]
            return dataset_num_images

        try:
            if self.action_type == "model_train":

                avg_epoch_time = sum(self.epochs_times) / len(self.epochs_times) * 1000
                batch_size = get_batch_size()
                num_iterations = get_dataset_num_images() / batch_size
                iteration_time = avg_epoch_time / num_iterations

                self.save_benchmark_results(
                    latency_ms=iteration_time,
                    batch_size=batch_size,
                )
            elif self.action_type == "model_eval":
                batch_size = get_batch_size()
                num_iterations = get_dataset_num_images() / batch_size
                eval_time = (
                    self.save_evaluation_results_time - self.model_download_time
                ) * 1000

                self.save_benchmark_results(
                    latency_ms=eval_time / num_iterations, batch_size=batch_size
                )

            elif self.action_type == "model_export":
                self.save_benchmark_results(
                    latency_ms=(time.time() - self.action_start_time) * 1000
                )
            elif self.action_type == "deploy_add":
                resp = self.rpc.get(f"/v1/model_prediction/get_minimum_prediction_latency/{self.action_details['_idModelDeployInstance']}")
                if resp['success']:
                    self.save_benchmark_results(
                        latency_ms=float(resp.get("data")) * 1000,
                        batch_size=get_batch_size(),
                    )
                else:
                    print(f"Failed to get minimum prediction latency: {resp['message']}")

        except Exception as e:
            log_error(__file__, "_log_action_benchmark_results", str(e))
            print(f"Exception in _log_action_benchmark_results: {str(e)}")

    def _clear_cache(self):
        try:
            gc.collect()
            import torch
            torch.cuda.empty_cache()
        except Exception as e:
            log_error(__file__, "_clear_cache", str(e))
            print(f"Exception in _clear_cache: {str(e)}")

    def log_epoch_results(self, epoch, epoch_result_list):
        """
        Logs the results of an epoch during model training or evaluation.

        This method records various metrics (like loss and accuracy) for a specific epoch.
        It updates the action status and logs the results for tracking purposes.

        Parameters
        ----------
        epoch : int
            The epoch number for which the results are being logged.
        results : list of dict
            A list of dictionaries containing the metric results for the epoch.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the epoch number is invalid.

        Examples
        --------
        >>> tracker.log_epoch_results(1, [{'loss': 0.25, 'accuracy': 0.92}])
        """
        if self.last_epoch_time is not None:
            self.epochs_times.append(time.time() - self.last_epoch_time)
        self.last_epoch_time = time.time()
        try:
            epoch_result_list = self.round_metrics(epoch_result_list)
            model_log_payload = {
                "_idModel": self._idModel_str,
                "_idAction": self.action_id_str,
                "epoch": epoch,
                "epochDetails": epoch_result_list,
            }

            headers = {"Content-Type": "application/json"}
            path = f"/v1/model_logging/model/{self._idModel_str}/train_epoch_log"

            self.rpc.post(path=path, headers=headers, payload=model_log_payload)
        except Exception as e:
            log_error(__file__, "log_epoch_results", str(e))
            print(f"Exception in log_epoch_results: {str(e)}")
            self.update_status("error", "error", "Failed to log epoch results")
            sys.exit(1)

    def round_metrics(self, epoch_result_list):
        """Rounds the metrics in the epoch results to 4 decimal places.

        Parameters
        ----------
        epoch_result_list : list
            A list of result dictionaries for the epoch. Each dictionary contains:
                - "metricValue" (float): The value of the metric to be rounded.

        Returns
        -------
        list
            The updated list of epoch results with rounded metrics. Each metric value is rounded to four decimal places, with special handling for invalid values (NaN or infinity).

        Examples
        --------
        >>> results = [{'metricValue': 0.123456}, {'metricValue': float('inf')}, {'metricValue': None}]
        >>> rounded_results = round_metrics(results)
        >>> print(rounded_results)
        [{'metricValue': 0.1235}, {'metricValue': 0}, {'metricValue': 0.0001}]
        """
        for metric in epoch_result_list:
            if metric["metricValue"] is not None:
                # Check if the value is within JSON-compliant range
                if math.isinf(metric["metricValue"]) or math.isnan(
                    metric["metricValue"]
                ):
                    metric["metricValue"] = 0
                else:
                    metric["metricValue"] = round(metric["metricValue"], 4)
                if metric["metricValue"] == 0:
                    metric["metricValue"] = 0.0001
        return epoch_result_list

    def upload_checkpoint(self, checkpoint_path, model_type="trained"):
        """Uploads a model checkpoint to the backend system.

        Parameters
        ----------
        checkpoint_path : str
            The file path of the checkpoint to upload. This should point to a valid model checkpoint file.
        model_type : str, optional
            The type of the model ("trained" or "exported"). Defaults to "trained", which refers to a model that has been trained but not yet exported.

        Returns
        -------
        bool
            True if the upload was successful, False otherwise. The function will log an error and exit if an exception occurs during the upload process.

        Examples
        --------
        >>> success = upload_checkpoint("path/to/checkpoint.pth")
        >>> if success:
        >>>     print("Checkpoint uploaded successfully!")
        >>> else:
        >>>     print("Checkpoint upload failed.")
        """
        try:
            if self.action_type == "model_export" and model_type == "exported":
                model_id = self.action_doc["_idService"]
            else:
                model_id = self._idModel_str

            presigned_url = self.rpc.get(
                path="/v1/model/get_model_upload_path",
                params={
                    "modelID": model_id,
                    "modelType": model_type,
                    "filePath": checkpoint_path.split("/")[-1],
                    "expiryTimeInMinutes": 59,
                },
            )["data"]

            with open(checkpoint_path, "rb") as file:
                response = requests.put(presigned_url, data=file)

            self.model_upload_time = time.time()

            if response.status_code == 200:
                print("Upload Successful")
                return True
            else:
                print(f"Upload failed with status code: {response.status_code}")
                return False
        except Exception as e:
            log_error(__file__, "upload_checkpoint", str(e))
            print(f"Exception in upload_checkpoint: {str(e)}")
            self.update_status("error", "error", "Checkpoint upload failed")
            sys.exit(1)

    def download_model(self, model_path, model_type="trained", model_id=None):
        """Downloads a model from the backend system.

        Parameters
        ----------
        model_path : str
            The path to save the downloaded model. The file will be saved at this location after downloading.
        model_type : str, optional
            The type of the model ("trained" or "exported"). Defaults to "trained".

        Returns
        -------
        bool
            True if the download was successful, False otherwise. The function will log an error and exit if an exception occurs during the download process.

        Examples
        --------
        >>> success = download_model("path/to/save/model.pth")
        >>> if success:
        >>>     print("Model downloaded successfully!")
        >>> else:
        >>>     print("Model download failed.")
        """
        self.model_download_time = time.time()
        try:
            if not model_id:
                model_id = self._idModel_str

            if model_type == "trained":
                presigned_url = self.rpc.post(
                    path="/v1/model/get_model_download_path",
                    payload={
                        "modelID": model_id,
                        "modelType": model_type,
                        "expiryTimeInMinutes": 59,
                    },
                )["data"]

            elif model_type == "exported":
                presigned_url = self.rpc.post(
                    path="/v1/model/get_model_download_path",
                    payload={
                        "modelID": model_id,
                        "modelType": model_type,
                        "expiryTimeInMinutes": 59,
                        "exportFormat": self.export_format,
                    },
                )["data"]

            response = requests.get(presigned_url)

            if response.status_code == 200:
                with open(model_path, "wb") as file:
                    file.write(response.content)
                print("Download Successful")
                return True
            else:
                print(f"Download failed with status code: {response.status_code}")
                return False
        except Exception as e:
            log_error(__file__, "download_model", str(e))
            print(f"Exception in download_model: {str(e)}")
            self.update_status("error", "error", "Model download failed")
            sys.exit(1)

    def _validate_eval_results(self, list_of_result_dicts, check_for_categories=False):
        """
        Validates the evaluation results to ensure all required splits, metrics, and categories are present.

        Parameters
        ----------
        list_of_result_dicts : list
            A list of dictionaries containing the evaluation results. Each dictionary should include 'split', 'metric', 'value', and optionally 'category'.

        Raises
        ------
        ValueError
            If any required split, metric, or category is missing.
        """
        # Validate input data
        model_family, _, _ = self.get_model_details()
        model_family = ModelFamily(self.session, model_family)
        supported_metrics = model_family.supported_metrics

        list_of_result_dicts = [
            result for result in list_of_result_dicts if result.get("metricName") in supported_metrics
        ]

        if check_for_categories:
            # categories = list(self.get_index_to_category().values()) + ["all"]
            # TODO: Add the logic to check for categories
            pass

        return list_of_result_dicts

    def _remove_duplicate_results(self, list_of_result_dicts):
        """Checks for duplicate results in the evaluation results.

        Parameters
        ----------
        list_of_result_dicts : list
            A list of dictionaries containing evaluation results to check for duplicates.
            Each dict should have splitType, metricName, and category fields.

        Raises
        ------
        ValueError
            If duplicate results are found for the same split type, metric and category.
        """
        seen = set()
        new_results = []
        for result in list_of_result_dicts:
            key = (
                result.get("splitType"),
                result.get("metricName"),
                result.get("category"),
            )
            if key not in seen:
                new_results.append(result)
                seen.add(key)
            else:
                print(
                    f"Duplicate result found for split type '{key[0]}', metric '{key[1]}', category '{key[2]}'"
                )
        list_of_result_dicts[:] = new_results

    def save_evaluation_results(self, list_of_result_dicts):
        """Saves the evaluation results for a model.

        Parameters
        ----------
        list_of_result_dicts : list
            A list of dictionaries containing the evaluation results. Each dictionary should include relevant metrics and their values for the model's performance.

        Raises
        ------
        Exception
            Logs an error and exits if an exception occurs during the saving process.

        Examples
        --------
        >>> evaluation_results = [
        >>>     {"metricName": "accuracy", "metricValue": 0.95, "splitType": "val", "category": "all"},
        >>>     {"metricName": "loss", "metricValue": 0.05, "splitType": "val", "category": "class_1"},
        >>> ]
        >>> save_evaluation_results(evaluation_results)
        """
        self.save_evaluation_results_time = time.time()
        try:
            self._remove_duplicate_results(list_of_result_dicts)
        except Exception as e:
            self.log_error(__file__, "remove_duplicate_results", str(e))
            print(f"Exception in remove_duplicate_results: {str(e)}")

        try:
            list_of_result_dicts = self._validate_eval_results(list_of_result_dicts)
        except Exception as e:
            self.log_error(__file__, "validate_evaluation_results", str(e))
            print(f"Exception in validate_evaluation_results: {str(e)}")

        try:

            url = "/v1/model/add_eval_results"

            Payload = {
                "_idModel": self._idModel,
                "_idDataset": self.action_details["_idDataset"],
                "_idProject": self.action_doc["_idProject"],
                "isOptimized": self.action_details.get("isOptimized", False),
                "runtimeFramework": self.export_format,
                "datasetVersion": self.action_details["datasetVersion"],
                "splitTypes": "",
                "evalResults": list_of_result_dicts,
            }

            self.rpc.post(path=url, payload=Payload)
        except Exception as e:
            self.log_error(__file__, "save_evaluation_results", str(e))
            print(f"Exception in save_evaluation_results: {str(e)}")
            self.update_status("error", "error", "Failed to save evaluation results")
            sys.exit(1)

    def add_index_to_category(self, indexToCat):
        """Adds an index-to-category mapping to the model.

        This function is used to establish a relationship between numerical indices
        and their corresponding categorical labels for the model. This mapping is
        essential for interpreting the model's output, particularly when the
        model is designed to classify input data into distinct categories.

        When to Use:
        -------------
        - This function is typically called after the model has been trained
        but before deploying the model for inference. It ensures that the
        indices output by the model during predictions can be accurately
        translated to human-readable category labels.
        - It is also useful when there are changes in the class labels
        or when initializing a new model.

        Parameters
        ----------
        indexToCat : dict
            A dictionary mapping integer indices to category names. For example,
            `{0: 'cat', 1: 'dog', 2: 'bird'}` indicates that index 0 corresponds
            to 'cat', index 1 to 'dog', and index 2 to 'bird'.

        Raises
        ------
        Exception
            If an error occurs while trying to add the mapping, it logs the error
            details and exits the process.

        Examples
        --------
        >>> index_mapping = {0: 'cat', 1: 'dog', 2: 'bird'}
        >>> add_index_to_category(index_mapping)
        """
        try:
            url = f"/v1/model/{self._idModel}/update_index_to_cat"
            payload = {"indexToCat": indexToCat}
            self.rpc.put(path=url, payload=payload)
        except Exception as e:
            log_error(__file__, "add_index_to_category", str(e))
            print(f"Exception in add_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to add index to category")
            sys.exit(1)

    def get_index_to_category(self, is_exported=False):
        """Fetches the index-to-category mapping for the model.

        This function retrieves the current mapping of indices to categories
        from the backend system. This is crucial for understanding the model's
        predictions, as it allows users to decode the model outputs back
        into meaningful category labels.

        When to Use:
        -------------
        - This function is often called before making predictions with the model
        to ensure that the index-to-category mapping is up to date and correctly
        reflects the model's configuration.
        - It can also be used after exporting a model to validate that the
        expected mappings are correctly stored and accessible.

        Parameters
        ----------
        is_exported : bool, optional
            A flag indicating whether to fetch the mapping for an exported model.
            Defaults to False. If True, the mapping is retrieved based on the export ID.

        Returns
        -------
        dict
            The index-to-category mapping as a dictionary, where keys are indices
            and values are corresponding category names.

        Raises
        ------
        Exception
            If an error occurs during the retrieval process, it logs the error
            details and exits the process.

        Examples
        --------
        >>> mapping = get_index_to_category()
        >>> print(mapping)
        {0: 'cat', 1: 'dog', 2: 'bird'}

        >>> exported_mapping = get_index_to_category(is_exported=True)
        >>> print(exported_mapping)
        {0: 'cat', 1: 'dog'}
        """
        try:
            url = "/v1/model/model_train/" + str(self._idModel_str)
            if is_exported:
                url = f"/v1/model/get_model_train_by_export_id?exportId={self._idModel_str}"

            modelTrain_doc = self.rpc.get(url)["data"]
            self.index_to_category = modelTrain_doc.get("indexToCat", {})

            return self.index_to_category
        except Exception as e:
            log_error(__file__, "get_index_to_category", str(e))
            print(f"Exception in get_index_to_category: {str(e)}")
            self.update_status("error", "error", "Failed to get index to category")
            sys.exit(1)

    def get_model_train(self, is_exported=False):
        try:
            url = "/v1/model/model_train/" + str(self._idModel_str)
            if is_exported:
                url = f"/v1/model/get_model_train_by_export_id?exportId={self._idModel_str}"
            model_train_doc = self.rpc.get(url)["data"]
            return model_train_doc

        except Exception as e:
            log_error(__file__, "get_model_train", str(e))
            print(f"Exception in get_model_train: {str(e)}")
            self.update_status("error", "error", "Failed to get model train")
            sys.exit(1)

    def get_input_size(self): # TODO: Test this
        model_family, model_key, _ = self.get_model_details()
        model_arch = ModelArch(self.session, model_family, model_key)
        return model_arch.input_size

    def get_model_details(self):
        model_train_doc = self.get_model_train(self.is_exported)
        model_family = model_train_doc["modelFamilyName"]
        model_key = model_train_doc["modelKey"]
        params_million = model_train_doc["paramsInMillion"]

        return model_family, model_key, params_million

    def save_benchmark_results(self, latency_ms, batch_size=1):

        try:
            model_family, model_key, params_million = self.get_model_details()

            payload = {
                "_idActionRecord": self.action_id_str,
                "modelFamily": self.action_details.get("modelFamily",model_family) ,
                "modelKey": self.action_details.get("modelKey", model_key),
                "paramsInMillion": self.action_details.get("paramsInMillion", params_million),
                "exportFormat": self.export_format,
                "actionType": self.action_type,
                "gpuName": self.action_details.get("gpuName", ""),
                "serviceProvider": self.action_details.get(
                    "serviceProvider",
                    self.action_details.get("CPUInfo", {}).get("serviceProvider", ""),
                ),
                "instanceType": self.action_details.get(
                    "instanceType",
                    self.action_details.get("CPUInfo", {}).get("instanceType", ""),
                ),
                "batchSize": batch_size,
                "latencyMs": latency_ms,
            }
            self.rpc.post(path="/v1/model_store/model_benchmarks", payload=payload)
        except Exception as e:
            log_error(__file__, "save_benchmark_results", str(e))
            print(f"Exception in save_benchmark_results: {str(e)}")
            self.update_status(
                "error", "error", f"Failed to save benchmark results: {str(e)}"
            )

    def calculate_metrics(
        self,
        split_type,
        outputs,
        targets,
        project_type,
        images=None,
    ):
        try:
            from matrice.metrics_calculator import (
            get_classification_evaluation_results,
            get_object_detection_evaluation_results,
            )
            if project_type == "classification":
                metrics = get_classification_evaluation_results(
                    split_type,
                    outputs,
                    targets,
                    self.get_index_to_category(self.is_exported),
                )
            elif project_type == "detection":
                metrics = get_object_detection_evaluation_results(
                    split_type,
                    outputs, 
                    targets,
                    self.get_index_to_category(self.is_exported),
                )
            else:
                raise ValueError(
                    f"Unsupported project type: {project_type}. Supported types are 'classification' and 'detection'"
                )

            if images:
                try:
                    self.store_inference_results(
                        images, outputs, targets, split_type, project_type
                    )
                except Exception as e:
                    log_error(
                        __file__,
                        "calculate_metrics",
                        f"Failed to store inference results: {str(e)}",
                    )
                    print(f"Failed to store inference results: {str(e)}")

            return metrics

        except Exception as e:
            log_error(__file__, "calculate_metrics", str(e))
            print(f"Failed to calculate metrics: {str(e)}")
            raise

    def _reformat_inference_results(self, outputs, project_type):
        results = []
        try:
            import torch.nn.functional as F
            import torch
            if project_type == "classification":
                for output in outputs:
                    output = output.unsqueeze(0)
                    probabilities = F.softmax(output, dim=1)
                    predicted_class = torch.argmax(output, 1).item()
                    confidence = round(probabilities[0, predicted_class].item(), 2)
                    results.append({
                        "category": self.index_to_category[str(predicted_class)],
                        "confidence": confidence
                    })

            elif project_type == "detection":
                for output in outputs:
                    boxes = output["boxes"].detach().cpu().numpy()
                    scores = output["scores"].detach().cpu().numpy()
                    labels = output["labels"].detach().cpu().numpy()

                    results.append([
                        {
                            "category": self.index_to_category[str(labels[i])],
                            "confidence": float(scores[i]),
                            "bounding_box": {
                                "xmin": int(boxes[i][0]),
                                "ymin": int(boxes[i][1]), 
                                "xmax": int(boxes[i][2]),
                                "ymax": int(boxes[i][3]),
                            },
                        }
                        for i in range(len(boxes))
                    ])
            else:
                raise ValueError(
                    f"Unsupported project type: {project_type}. Supported types are 'classification' and 'detection'"
                )

        except Exception as e:
            log_error(__file__, "_reformat_inference_results", str(e))

        return results

    def _reformat_inference_targets(self, targets, project_type):
        results = []
        try:
            if project_type == "classification":
                results = [
                    {
                        "category": self.index_to_category[str(target.detach().cpu().item())],
                        "confidence": 1
                    }
                    for target in targets
                ]

            elif project_type == "detection":
                for target in targets:
                    boxes = target["boxes"].detach().cpu().numpy()
                    labels = target["labels"].detach().cpu().numpy()

                    results.append([
                        {
                            "category": self.index_to_category[str(int(labels[i]))],
                            "confidence": 1,
                            "bounding_box": {
                                "xmin": int(boxes[i][0]),
                                "ymin": int(boxes[i][1]),
                                "xmax": int(boxes[i][2]),
                                "ymax": int(boxes[i][3]),
                            },
                        }
                        for i in range(len(boxes))
                    ])
            else:
                raise ValueError(
                    f"Unsupported project type: {project_type}. Supported types are 'classification' and 'detection'"
                )

        except Exception as e:
            log_error(__file__, "_reformat_inference_targets", str(e))

        return results

    def _reformat_inference_results_yolo(self, outputs):
        results = []
        for output in outputs:
            result = []
            for cls, xyxy, conf in zip(
                output.boxes.cls.detach().detach().cpu().numpy(),
                output.boxes.xyxy.detach().cpu().numpy(),
                output.boxes.conf.detach().cpu().numpy()
            ):
                x_min, y_min, x_max, y_max = map(int, xyxy)
                result.append({
                    "category": str(int(cls)),
                    "confidence": float(conf),
                    "bounding_box": {
                        "xmin": x_min,
                        "ymin": y_min,
                        "xmax": x_max,
                        "ymax": y_max
                    }
                })
            results.append(result)
        return results

    def _reformat_inference_targets_yolo(self, images, targets):
        def load_targets_file(file_path):
            labels = []
            with open(file_path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        raise ValueError(f"Invalid target format: {line}")
                    cls, x_center, y_center, width, height = parts
                    labels.append([
                        cls,
                        float(x_center),
                        float(y_center),
                        float(width),
                        float(height)
                    ])
            return labels

        images_list = []
        targets_list = []

        for image_path, target_path in zip(images, targets):
            image = Image.open(image_path).convert('RGB')
            img_width, img_height = image.size
            target = []

            for target_data in load_targets_file(target_path):
                cls, x_center, y_center, width, height = target_data

                # Convert normalized coordinates to absolute coordinates
                x_center_abs = float(x_center) * img_width
                y_center_abs = float(y_center) * img_height
                width_abs = float(width) * img_width
                height_abs = float(height) * img_height

                # Calculate bounding box coordinates
                x_min = int(x_center_abs - width_abs / 2)
                y_min = int(y_center_abs - height_abs / 2)
                x_max = int(x_center_abs + width_abs / 2)
                y_max = int(y_center_abs + height_abs / 2)

                target.append({
                    "category": str(int(cls)),
                    "confidence": 1.0,
                    "bounding_box": {
                        "xmin": x_min,
                        "ymin": y_min,
                        "xmax": x_max,
                        "ymax": y_max
                    }
                })

            targets_list.append(target)
            images_list.append(image)

        return images_list, targets_list

    def store_inference_results(
        self,
        images,
        outputs,
        targets,
        split_type,
        project_type,
        format_inputs=True,
        pil_images=False,
        yolo_format=False
    ):
        try:
            from torchvision.transforms import ToPILImage
            import torch
            self.index_to_category = self.get_index_to_category(self.is_exported)
            if format_inputs:
                if yolo_format:
                    outputs = self._reformat_inference_results_yolo(outputs)
                    images, targets = self._reformat_inference_targets_yolo(images, targets)
                    pil_images = True
                else:
                    outputs = self._reformat_inference_results(outputs, project_type)
                    targets = self._reformat_inference_targets(targets, project_type)
                    if isinstance(images, list):
                        images = torch.stack(images)

            if self.num_inference_samples >= 20:
                return

            num_samples = min(10, len(outputs))
            self.num_inference_samples += num_samples

            samples = [
                {
                    "_idModel": self._idModel_str,
                    "modelType": "exported" if self.is_exported else "trained",
                    "splitType": split_type,
                    "prediction": prediction,
                    "target": target,
                }
                for prediction, target in zip(outputs[:num_samples], targets[:num_samples])
            ]

            try:
                presigned_urls = self.rpc.post(
                    path="/v1/model/add_test_sample",
                    payload=samples
                ).get('data')
            except Exception as e:
                log_error(__file__, "store_inference_results", str(e))
                print(f"Failed to store inference results: {str(e)}")
                return

            # Upload images to presigned URLs
            for image, presigned_url in zip(images[:num_samples], presigned_urls):
                try:
                    if not pil_images:
                        image = ToPILImage()(image)

                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format="JPEG")
                    img_byte_arr.seek(0)

                    response = requests.put(presigned_url, data=img_byte_arr)

                    if response.status_code == 200:
                        print(f"Successfully uploaded image to {presigned_url}")
                    else:
                        print(f"Failed to upload image to {presigned_url}, Status Code: {response.status_code}")

                except requests.RequestException as e:
                    print(f"Error uploading image to {presigned_url}: {e}")

        except Exception as e:
            log_error(__file__, "store_inference_results", str(e))
            print(f"Failed to process inference results: {str(e)}")

    def update_prediction_results(self, predictions):
        if not self.action_details.get("class_index_map"):
            return predictions
        if not self.action_details.get("modelType") == "pretrained":
            return predictions
        try:
            index_to_category = self.action_details.get("class_index_map")
            if self.project_type == "classification":
                predictions["category"] = index_to_category.get(
                    str(predictions["category"]), predictions["category"]
                )
            else:
                for prediction in predictions:
                    prediction["category"] = index_to_category.get(
                        str(prediction["category"]), prediction["category"]
                    )
        except Exception:
            ...
        return predictions