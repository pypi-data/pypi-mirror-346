"""Module providing actions_manager functionality."""

import logging
import os
import traceback
import time
from matrice.compute_manager.action_instance import (
    ActionInstance,
)
from matrice.compute_manager.instance_utils import (
    has_gpu,
    get_mem_usage,
    cleanup_docker_storage,
)
from matrice.compute_manager.scaling import (
    Scaling,
)
from matrice.utils import log_error


class ActionsManager:
    """Class for managing actions."""

    def __init__(self, scaling: Scaling):
        """Initialize an action manager.

        Args:
            scaling (Scaling): Scaling service instance
        """
        self.current_actions = {}
        self.scaling = scaling
        self.memory_threshold = 0.9
        self.poll_interval = 10

    def fetch_actions(self):
        """Poll for actions and process them if memory threshold is not exceeded.

        Returns:
            list: List of fetched actions
        """
        actions = []
        logging.info("Polling backend for new jobs")
        fetched_actions, error, _ = self.scaling.assign_jobs(has_gpu())
        if error:
            logging.error("Error assigning jobs: %s", error)
            return actions
        if not isinstance(fetched_actions, list):
            fetched_actions = [fetched_actions]
        for action in fetched_actions:
            if not action:
                continue
            if action["_id"] != "000000000000000000000000":
                actions.append(action)
                logging.info(
                    "Fetched action details: %s",
                    actions,
                )
        return actions

    def process_action(self, action):
        """Process the given action.

        Args:
            action (dict): Action details to process

        Returns:
            ActionInstance: Processed action instance or None if failed
        """
        try:
            logging.info(
                "Processing action: %s",
                action["_id"],
            )
            action_instance = ActionInstance(self.scaling, action)
            self.scaling.update_action_status(
                service_provider=os.environ["SERVICE_PROVIDER"],
                action_record_id=action["_id"],
                status="starting",
                action_duration=0,
            )
            logging.info("locking action")
            self.scaling.update_action_status(
                service_provider=os.environ["SERVICE_PROVIDER"],
                status="started",
                action_record_id=action["_id"],
                isRunning=True,
                action_duration=0,
                cpuUtilisation=0.0,
                gpuUtilisation=0.0,
                memoryUtilisation=0.0,
                gpuMemoryUsed=0,
            )
            self.scaling.update_status(
                action["_id"],
                action["action"],
                "bg-job-scheduler",
                "JBSS_LCK",
                "OK",
                "Job is locked for processing",
            )
            action_instance.execute()
            logging.info(
                "action %s started.",
                action_instance.action_record_id,
            )
            return action_instance
        except Exception as exc:
            log_error(
                "actions_manager.py",
                "process_action",
                exc,
            )
            logging.error(
                "Failed to add action to queue: %s",
                exc,
            )
            traceback.print_exc()
            return None

    def process_actions(self):
        """Process fetched actions."""
        for action in self.fetch_actions():
            action_instance = self.process_action(action)
            if action_instance:
                self.current_actions[action["_id"]] = action_instance

    def purge_unwanted(self):
        """Purge completed or failed actions."""
        for action_id, instance in list(self.current_actions.items()):
            if not instance.is_running():
                logging.info(
                    "action %s is not running",
                    action_id,
                )
                del self.current_actions[action_id]
                logging.info(
                    "action %s purged from queue.",
                    action_id,
                )

    def get_current_actions(self):
        """Get the current actions.

        Returns:
            dict: Current active actions
        """
        self.purge_unwanted()
        return self.current_actions

    def start_actions_manager(self):
        """Start the actions manager main loop."""
        while True:
            try:
                mem_usage = get_mem_usage()
                logging.info("Memory usage: %d", mem_usage)
                waiting_time = int(
                    min(
                        self.poll_interval
                        / max(
                            0.001,
                            self.memory_threshold - mem_usage,
                        ),
                        120,
                    )
                )
                if mem_usage < self.memory_threshold:
                    self.process_actions()
                    logging.info(
                        "Waiting for %d seconds before next poll",
                        waiting_time,
                    )
                else:
                    logging.info(
                        "Memory threshold exceeded, waiting for %d seconds",
                        waiting_time,
                    )
                cleanup_docker_storage()
            except Exception as exc:
                logging.error(
                    "Error in actions_manager start_actions_manager: %s",
                    str(exc),
                )
            time.sleep(waiting_time)
