"""Module providing __init__ functionality."""

from matrice.compute_manager.instance_manager import (
    InstanceManager,
)
from matrice.utils import dependencies_check

dependencies_check(["docker", "psutil"])

__all__ = ["InstanceManager"]
