"""Module providing action_instance functionality."""

import logging
import os
import shlex
import subprocess
import threading
import time
import signal
import urllib.request
from matrice.compute_manager.instance_utils import (
    get_gpu_with_sufficient_memory_for_action,
    get_decrypted_access_key_pair,
    get_max_file_system,
)
from matrice.compute_manager.task_utils import (
    setup_workspace_and_run_task,
)
from matrice.compute_manager.scaling import (
    Scaling,
)


class ActionInstance:
    """Base class for tasks that run in Action containers."""

    def __init__(self, scaling: Scaling, action_info: dict):
        """Initialize an action instance.

        Args:
            scaling (Scaling): Scaling service instance
            action_info (dict): Action information dictionary
        """
        self.scaling = scaling
        self.process = None
        self.stop_thread = False
        self.log_thread = None
        self.log_path = None
        self.cmd = None
        self.matrice_access_key_id = None
        self.matrice_secret_access_key = None
        self.action_info = action_info
        self.action_record_id = action_info["_id"]
        self.action_type = action_info["action"]
        self.action_details = action_info["actionDetails"]
        self.docker_container = self.action_details.get(
            "docker",
            self.action_details.get(
                "docker_container",
                self.scaling.get_data_processing_image(),
            ),
        )
        self.actions_map = {
            "model_train": model_train_execute,
            "model_eval": model_eval_execute,
            "model_export": model_export_execute,
            "deploy_add": model_deploy_execute,
            "data_import": data_processing_execute,
            "data_add": data_processing_execute,
            "data_split": data_split_execute,
            "data_prep": data_preparation_execute,
            "dataset_annotation": dataset_annotation_execute,
            "image_build": image_build_execute,
            "resource_clone": resource_clone_execute,
            "kafka_setup": kafka_setup_execute,
        }
        if self.action_type not in self.actions_map:
            raise ValueError(f"Unknown action type: {self.action_type}")
        self.task = self.actions_map[self.action_type]

    def _init_credentials(self):
        """Initialize Matrice credentials.

        Returns:
            dict: Dictionary containing access key ID and secret access key
        """
        self.matrice_access_key_id = self.scaling.session.access_key
        self.matrice_secret_access_key = self.scaling.session.secret_key
        if not all(
            [
                self.matrice_access_key_id,
                self.matrice_secret_access_key,
            ]
        ):
            raise ValueError(
                "Matrice credentials not found - both access key ID and secret access key are required"
            )
        return {
            "matrice_access_key_id": self.matrice_access_key_id,
            "matrice_secret_access_key": self.matrice_secret_access_key,
        }

    def get_log_path(self):
        """Get log directory path, creating if needed.

        Returns:
            str: Path to log directory
        """
        os.makedirs("logs", exist_ok=True)
        return "logs"

    def is_running(self):
        """Check if task process is running.

        Returns:
            bool: True if process is running, False otherwise
        """
        try:
            return self.process and self.process.poll() is None
        except Exception as err:
            logging.error(
                "Error checking if task is running: %s",
                err,
            )
            return False

    def get_action_details(self):
        """Get action details from scaling service.

        Returns:
            dict: Action details if successful, None otherwise
        """
        resp, error, message = self.scaling.get_action_details(self.action_record_id)
        if error:
            logging.error(
                "Error getting action details: %s",
                error,
            )
            return None
        return resp

    def get_gpu_config(self, action_details):
        """Get GPU configuration string based on available GPUs.

        Args:
            action_details (dict): Action details containing GPU requirements

        Returns:
            str: GPU configuration string
        """
        if not action_details["actionDetails"].get("gpuRequired", False):
            return ""
        gpu_indices = get_gpu_with_sufficient_memory_for_action(action_details=action_details)
        if gpu_indices:
            gpu_str = ",".join(map(str, gpu_indices))
            logging.info("Using GPUs: %s", gpu_str)
            return f'--gpus "device={gpu_str}"'
        logging.info("No GPUs with sufficient memory found.")
        return ""

    def get_base_docker_cmd(
        self,
        work_fs="",
        use_gpu="",
        mount_docker_sock=False,
        action_id="",
        model_key="",
        extra_env_vars=None,
        port_mapping=None,
        destination_workspace_path="/usr/src/workspace",
        docker_workdir="",
    ):
        """Build base Docker command with common options.

        Args:
            work_fs (str): Work filesystem path
            use_gpu (str): GPU configuration string
            mount_docker_sock (bool): Whether to mount Docker socket
            action_id (str): Action ID
            model_key (str): Model key
            extra_env_vars (dict): Additional environment variables
            port_mapping (dict): Port mappings
            destination_workspace_path (str): Container workspace path
            docker_workdir (str): Docker working directory

        Returns:
            str: Base Docker command
        """
        if extra_env_vars is None:
            extra_env_vars = {}
        if port_mapping is None:
            port_mapping = {}
        if not docker_workdir:
            docker_workdir = f"/usr/src/{action_id}"
        cmd_parts = [
            f"docker run {use_gpu} --rm ",
            (
                f"-v {work_fs}/workspace:{destination_workspace_path}"
                if work_fs not in ["", "/"]
                else " "
            ),
            (
                f"-v {work_fs}/{action_id}:/usr/src/{action_id}"
                if work_fs not in ["", "/"] and action_id
                else " "
            ),
            ("-v /var/run/docker.sock:/var/run/docker.sock" if mount_docker_sock else " "),
            (
                "--net=host "
                if not port_mapping
                else " ".join(f"-p {host}:{container}" for host, container in port_mapping.items())
            ),
            f"-e ENV={shlex.quote(os.environ['ENV'])} ",
            f"-e MATRICE_SECRET_ACCESS_KEY={shlex.quote(self.matrice_secret_access_key)} ",
            f"-e MATRICE_ACCESS_KEY_ID={shlex.quote(self.matrice_access_key_id)} ",
            *[f"-e {key}={shlex.quote(str(value))} " for key, value in extra_env_vars.items()],
            (
                f"-e HUGGING_FACE_ACCESS_TOKEN={shlex.quote(self.get_hugging_face_token(model_key))}"
                if model_key
                else ""
            ),
            f"--shm-size=30G --pull=always {shlex.quote(self.docker_container)} /bin/bash -c \"cd {docker_workdir} && "
            f"if [ -f requirements.txt ]; then pip install -r requirements.txt; fi && pip install --upgrade --force-reinstall --index-url https://{'' if os.environ['ENV'] == 'prod' else 'test.'}pypi.org/simple/ matrice && ",
        ]
        return " ".join(filter(None, cmd_parts))

    def get_hugging_face_token(self, model_key):
        """Get Hugging Face token for specific model keys.

        Args:
            model_key (str): Model key to check

        Returns:
            str: Hugging Face token if available, empty string otherwise
        """
        hugging_face_token = ""
        if model_key and (model_key.startswith("microsoft") or model_key.startswith("timm")):
            secret_name = "hugging_face"
            resp, error, message = self.scaling.get_model_secret_keys(secret_name)
            if error is not None:
                logging.error(
                    "Error getting Hugging Face token: %s",
                    message,
                )
            else:
                hugging_face_token = resp["user_access_token"]
        return hugging_face_token

    def get_internal_api_key(self, action_id):
        """Get internal API key for action.

        Args:
            action_id (str): Action ID

        Returns:
            str: Internal API key if available, empty string otherwise
        """
        internal_api_key = ""
        resp, error, message = self.scaling.get_internal_api_key(action_id)
        if error is not None:
            logging.error(
                "Error getting internal api key: %s",
                message,
            )
        else:
            internal_api_key = resp["internal_api_key"]
        return internal_api_key

    def setup_action_requirements(
        self,
        action_details,
        work_fs="",
        model_family="",
        action_id="",
    ):
        """Setup action requirements.

        Args:
            action_details (dict): Action details
            work_fs (str): Work filesystem path
            model_family (str): Model family name
            action_id (str): Action ID

        Raises:
            Exception: If setup fails
        """
        if model_family:
            model_codebase_url, error, message = self.scaling.get_model_codebase(model_family)
            (
                model_codebase_requirements_url,
                error,
                message,
            ) = self.scaling.get_model_codebase_requirements(model_family)
            setup_workspace_and_run_task(
                work_fs,
                action_id,
                model_codebase_url,
                model_codebase_requirements_url,
            )
        try:
            creds, error, message = self.scaling.get_docker_hub_credentials()
            if error:
                raise Exception(f"Failed to get Docker credentials: {message}")
            username = creds["username"]
            password = creds["password"]
            login_cmd = f"docker login -u {shlex.quote(username)} -p {shlex.quote(password)}"
            subprocess.run(login_cmd, shell=True, check=True)
        except Exception as err:
            logging.error(
                "Docker login failed: %s",
                str(err),
            )
            raise
        try:
            (
                user_access_key_pair,
                error,
                message,
            ) = self.scaling.get_user_access_key_pair(action_details["_idUser"])
            if error:
                raise Exception(f"Failed to get user access key pair: {message}")
            access_key = user_access_key_pair["access_key"]
            secret_key = user_access_key_pair["secret_key"]
            (
                self.matrice_access_key_id,
                self.matrice_secret_access_key,
            ) = get_decrypted_access_key_pair(access_key, secret_key)
        except Exception as err:
            logging.error(
                "Failed to setup credentials: %s",
                str(err),
            )
            raise

    def send_logs_continuously(self):
        """Continuously read and send logs from the log file to the scaling service."""
        last_position = 0
        while not self.stop_thread and os.path.exists(self.log_path):
            try:
                with open(self.log_path, "rb") as log_file:
                    log_file.seek(last_position)
                    new_content = log_file.read()
                    if new_content:
                        decoded_content = new_content.decode(
                            "utf-8",
                            errors="replace",
                        )
                        self._send_logs_to_scaling(decoded_content)
                        self._check_cuda(decoded_content)
                    last_position = log_file.tell()
            except IOError as err:
                logging.error(
                    "Error reading log file: %s",
                    err,
                )
            except Exception as err:
                logging.exception(
                    "Unexpected error in send_logs_continuously: %s",
                    err,
                )
            time.sleep(30)

    def _send_logs_to_scaling(self, log_content):
        """Send logs to the scaling service.

        Args:
            log_content (str): Log content to send
        """
        try:
            _, error, message = self.scaling.update_action_docker_logs(
                action_record_id=self.action_record_id,
                log_content=log_content,
            )
            if error:
                logging.error(
                    "Error from update_action_docker_logs: %s",
                    error,
                )
        except Exception as err:
            logging.exception(
                "Exception in update_action_docker_logs: %s",
                err,
            )

    def _check_cuda(self, log_content):
        """Check for CUDA out of memory errors in logs and update action status.

        Args:
            log_content (str): Log content to check
        """
        try:
            if "CUDA error: out of memory" in log_content:
                action_details = self.get_action_details()
                if not action_details:
                    return
                self.scaling.update_action(
                    id=self.action_record_id,
                    step_code="ERROR",
                    action_type=action_details["action"],
                    status="ERROR",
                    status_description="CUDA error: out of memory",
                    service="bg-job-scheduler",
                    job_params=action_details["jobParams"],
                )
        except Exception as err:
            logging.exception("Error in _check_cuda: %s", err)

    def start_process(self, cmd, log_name):
        """Start the process and initialize logging.

        Args:
            cmd (str): Command to execute
            log_name (str): Name for log file

        Raises:
            Exception: If process fails to start
        """
        self.cmd = cmd
        self.log_path = f"{self.get_log_path()}/{log_name}_{self.action_record_id}.txt"
        try:
            with open(self.log_path, "wb") as out:
                self.process = subprocess.Popen(
                    shlex.split(self.cmd),
                    stdout=out,
                    stderr=out,
                    env={**os.environ},
                    start_new_session=True,
                )
        except Exception as err:
            logging.error(
                "Failed to start process: %s",
                str(err),
            )
            raise

    def start(self, cmd, log_name):
        """Start the process and log monitoring thread.

        Args:
            cmd (str): Command to execute
            log_name (str): Name for log file
        """
        self.start_process(cmd, log_name)
        self.log_thread = threading.Thread(
            target=self.send_logs_continuously,
            daemon=True,
        )
        self.log_thread.start()

    def stop(self):
        """Stop the process and log monitoring thread."""
        try:
            self.stop_thread = True
            if self.process:
                os.killpg(
                    os.getpgid(self.process.pid),
                    signal.SIGTERM,
                )
                self.process.wait(timeout=30)
            if self.log_thread and self.log_thread.is_alive():
                self.log_thread.join(timeout=30)
        except Exception as err:
            logging.error(
                "Error stopping process: %s",
                str(err),
            )
            if self.process:
                self.process.kill()

    def execute(self):
        """Execute the task."""
        self.task(self)


def data_preparation_execute(
    self: ActionInstance,
):
    """Execute data preparation task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details, work_fs, model_family="")
    action = {"jobParams": action_details["jobParams"]}
    dataset_id_version = (
        action_details["jobParams"]["dataset_id"] + action_details["jobParams"]["dataset_version"]
    )
    action["jobParams"].update(
        {
            "dataset_host_path_map": {dataset_id_version: f"{work_fs}/workspace"},
            "dataset_local_path_map": {dataset_id_version: "/usr/src/app/workspace"},
            "host_file_system": work_fs,
        }
    )
    self.scaling.update_action(
        id=self.action_record_id,
        step_code="DCK_LNCH",
        action_type=action_details["action"],
        status=action_details["status"],
        sub_action=action_details["subAction"],
        status_description="Job is assigned to docker",
        service="bg-job-scheduler",
        job_params=action["jobParams"],
    )
    if action["jobParams"].get("model_train_docker"):
        logging.info("Pulling the docker image")
        pull_cmd = f"docker pull {action['jobParams']['model_train_docker']}"
        process = subprocess.Popen(
            pull_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logging.info(
            "Started pulling Docker image with PID: %s",
            process.pid,
        )
    cmd = f'{self.get_base_docker_cmd(work_fs, destination_workspace_path="/usr/src/app/workspace", docker_workdir="/usr/src/app/workspace")} python3 /usr/src/app/data_preparation.py {self.action_record_id} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "data_preparation_log")


def data_processing_execute(self: ActionInstance):
    """Execute data processing task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details, work_fs, model_family="")
    action = {"jobParams": action_details["jobParams"]}
    action["jobParams"].update(
        {
            "dp_dv_host_paths": [f"{work_fs}/workspace"],
            "dp_dv_local_paths": ["/usr/src/app/workspace"],
        }
    )
    self.scaling.update_action(
        id=self.action_record_id,
        step_code="DCK_LNCH",
        action_type=action_details["action"],
        status="ACK",
        status_description="Job is assigned to docker",
        service="bg-job-scheduler",
        job_params=action["jobParams"],
    )
    cmd = f'{self.get_base_docker_cmd(work_fs)} python3 /usr/src/app/main.py {self.action_record_id} "'
    logging.info("cmd: %s", cmd)
    self.start(cmd, "data_processing_log")


def data_split_execute(self: ActionInstance):
    """Execute data split task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details, work_fs, model_family="")
    cmd = f'{self.get_base_docker_cmd(work_fs)} python3 /usr/src/app/data_split.py {self.action_record_id} "'
    logging.info("cmd: %s", cmd)
    self.start(cmd, "data_split")


def dataset_annotation_execute(
    self: ActionInstance,
):
    """Execute dataset annotation task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details, work_fs)
    cmd = f'{self.get_base_docker_cmd(work_fs)} python3 /usr/src/app/dataset_annotation.py {self.action_record_id} "'
    logging.info("cmd: %s", cmd)
    self.start(cmd, "dataset_annotation")


def model_deploy_execute(self: ActionInstance):
    """Execute model deployment task."""
    external_port = self.scaling.get_open_port()
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    action_id = action_details["_id"]
    model_family = action_details["actionDetails"]["modelFamily"]
    self.setup_action_requirements(
        action_details,
        work_fs,
        model_family=model_family,
        action_id=action_id,
    )
    use_gpu = self.get_gpu_config(action_details)

    cmd = f'{self.get_base_docker_cmd(work_fs, use_gpu, mount_docker_sock=True, action_id=action_id, port_mapping={external_port: 80})} python3 deploy.py {self.action_record_id} {external_port}"'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "deploy_log")


def model_train_execute(self: ActionInstance):
    """Execute model training task."""
    action_details = self.get_action_details()
    if not action_details:
        return
    action_id = action_details["_id"]
    use_gpu = self.get_gpu_config(action_details)
    work_fs = action_details["jobParams"]["host_file_system"]
    model_key = action_details["actionDetails"]["modelKey"]
    model_family = action_details["actionDetails"]["modelFamily"]
    self.setup_action_requirements(
        action_details,
        work_fs,
        model_family=model_family,
        action_id=action_id,
    )
    cmd = f'{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id, model_key=model_key)} python3 train.py {self.action_record_id} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "train_log")


def model_eval_execute(self: ActionInstance):
    """Execute model evaluation task."""
    action_details = self.get_action_details()
    if not action_details:
        return
    action_id = action_details["_id"]
    work_fs = action_details["jobParams"]["host_file_system"]
    model_family = action_details["actionDetails"]["modelFamily"]
    use_gpu = self.get_gpu_config(action_details)
    self.setup_action_requirements(
        action_details,
        work_fs,
        model_family=model_family,
        action_id=action_id,
    )
    cmd = f'{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id)} python3 eval.py {self.action_record_id} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "eval_log")


def model_export_execute(self: ActionInstance):
    """Execute model export task."""
    work_fs = get_max_file_system()
    action_details = self.get_action_details()
    if not action_details:
        return
    action_id = action_details["_id"]
    if "host_file_system" in action_details["jobParams"]:
        work_fs = action_details["jobParams"]["host_file_system"]
        logging.info("host_file_system: %s", work_fs)
    use_gpu = self.get_gpu_config(action_details)
    model_family = action_details["actionDetails"]["modelFamily"]
    self.setup_action_requirements(
        action_details,
        work_fs,
        model_family=model_family,
        action_id=action_id,
    )
    cmd = f'{self.get_base_docker_cmd(work_fs, use_gpu, action_id=action_id)} python3 export.py {self.action_record_id} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "export_log")


def image_build_execute(self: ActionInstance):
    """Execute image building task."""
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details)
    model_family_id = action_details["_idService"]
    action_id = action_details["_id"]
    internal_api_key = self.get_internal_api_key(action_id)
    extra_env_vars = {"MATRICE_INTERNAL_API_KEY": internal_api_key}
    cmd = f'{self.get_base_docker_cmd(mount_docker_sock=True, extra_env_vars=extra_env_vars)} python3 main.py {model_family_id} {action_id}"'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "image_build_log")


def resource_clone_execute(self: ActionInstance):
    """Execute resource clone task."""
    action_details = self.get_action_details()
    if not action_details:
        return
    self.setup_action_requirements(action_details)
    cmd = f'{self.get_base_docker_cmd()} python3 main.py {self.action_record_id} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "resource_clone")


def kafka_setup_execute(self: ActionInstance):
    """Execute kafka server task."""
    action_details = self.get_action_details()
    if not action_details:
        return
    host_port = self.scaling.get_open_port()
    host_ip = urllib.request.urlopen("https://ident.me", timeout=10).read().decode("utf8")
    container_port = 9092
    kafka_config = {
        "KAFKA_NODE_ID": 1,
        "KAFKA_PROCESS_ROLES": "broker,controller",
        "KAFKA_LISTENERS": "PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093",
        "KAFKA_ADVERTISED_LISTENERS": f"PLAINTEXT://{host_ip}:{host_port}",
        "KAFKA_CONTROLLER_LISTENER_NAMES": "CONTROLLER",
        "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT",
        "KAFKA_CONTROLLER_QUORUM_VOTERS": "1@localhost:9093",
        "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": 1,
        "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR": 1,
        "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR": 1,
        "KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS": 0,
        "KAFKA_NUM_PARTITIONS": 1,  
    }
    base_cmd = self.get_base_docker_cmd(port_mapping={host_port: container_port}, docker_workdir="/opt/kafka/bin", extra_env_vars=kafka_config)
    cmd = f'{base_cmd} /etc/kafka/docker/run & python3 main.py {self.action_record_id} {host_port} "'
    logging.info("cmd is: %s", cmd)
    self.start(cmd, "kafka_setup")
