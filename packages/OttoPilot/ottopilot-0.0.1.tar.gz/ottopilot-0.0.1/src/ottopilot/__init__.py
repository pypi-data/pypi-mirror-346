"""
OttoPilot: Utility library for Ascend product repository.

This package provides common functionality for scripts in the Ascend product repository.
"""

from ottopilot.commands import run_command
from ottopilot.log_utils import get_logger, setup_logging
from ottopilot.cli import cli_entry_point as main

__all__ = ["run_command", "setup_logging", "get_logger", "main"]
