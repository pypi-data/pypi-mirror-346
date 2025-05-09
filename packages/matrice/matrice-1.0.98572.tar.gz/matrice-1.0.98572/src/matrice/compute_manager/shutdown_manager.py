"""Module providing shutdown_manager functionality."""

import logging
import time
import os
import sys
from matrice.utils import log_error
from matrice.compute_manager.scaling import (
    Scaling,
)


class ShutdownManager:
    """Class for managing compute instance shutdown."""

    def __init__(self, scaling: Scaling):
        """Initialize ShutdownManager.

        Args:
            scaling: Scaling instance to manage shutdown
        """
        self.scaling = scaling
        self.launch_time = time.time()
        self._load_shutdown_configuration()
        self.last_no_queued_time = None
        self.shutdown_threshold = 500
        self.launch_duration = 1
        self.instance_source = "auto"
        self.encryption_key = None
        self.reserved_instance = None

    def _load_shutdown_configuration(self):
        """Load shutdown configuration from AWS secrets and initialize parameters."""
        response, error, message = self.scaling.get_shutdown_details()
        if error is None:
            self.shutdown_threshold = response["shutdownThreshold"] or 500
            self.launch_duration = response["launchDuration"] or 1
            self.instance_source = response["instanceSource"] or "auto"
            self.encryption_key = response.get("encryptionKey")
        self.launch_duration_seconds = self.launch_duration * 60 * 60
        self.reserved_instance = self.instance_source == "reserved"

    def do_cleanup_and_shutdown(self):
        """Clean up resources and shut down the instance."""
        try:
            self.scaling.stop_instance()
        except Exception as err:
            log_error(
                "instance_utils.py",
                "do_cleanup_and_shutdown",
                err,
            )
        try:
            if os.environ.get("SERVICE_PROVIDER"):
                os.system("shutdown now")
                sys.exit(0)
        except Exception as err:
            log_error(
                "instance_utils.py",
                "do_cleanup_and_shutdown",
                err,
            )
        sys.exit(1)

    def handle_shutdown(self, tasks_running):
        """Check idle time and trigger shutdown if threshold is exceeded.

        Args:
            tasks_running: Boolean indicating if there are running tasks
        """
        # Update idle time tracking
        if tasks_running:
            self.last_no_queued_time = None
        elif self.last_no_queued_time is None:
            self.last_no_queued_time = time.time()
            
        if self.last_no_queued_time is not None:
            idle_time = time.time() - self.last_no_queued_time
            launch_time_passed = (time.time() - self.launch_time) > self.launch_duration_seconds
            
            # Log current status
            logging.info(
                "Time since last action: %s seconds. Time left to shutdown: %s seconds.",
                idle_time,
                max(0, self.shutdown_threshold - idle_time),
            )
            
            # Check if we should shut down
            if idle_time <= self.shutdown_threshold:
                return
                
            # For reserved instances, only shut down if launch duration has passed and idle time is exceeded
            if self.reserved_instance and not launch_time_passed:
                logging.info(
                    "Reserved instance not shutting down yet. Launch duration: %s seconds, elapsed: %s seconds",
                    self.launch_duration_seconds,
                    time.time() - self.launch_time
                )
                return
                
            logging.info(
                "Idle time %s seconds exceeded threshold %s seconds. Shutting down.",
                idle_time,
                self.shutdown_threshold
            )
            
            self.do_cleanup_and_shutdown()
