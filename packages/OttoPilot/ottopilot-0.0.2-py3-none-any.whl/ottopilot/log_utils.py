"""
Logging utilities for consistent logging across scripts.
"""

import logging
import os
from typing import Dict, Optional, Union

from rich.console import Console
from rich.logging import RichHandler

# Create console instance
console = Console()

# Default logging configuration
DEFAULT_FORMAT = "%(message)s"
DEFAULT_DATE_FORMAT = "[%X]"
DEFAULT_LEVEL = logging.INFO
DEFAULT_RICH_TRACEBACKS = True

# Keep track of initialized loggers to avoid duplicate setup
_initialized_loggers: Dict[str, logging.Logger] = {}
_root_logger_initialized = False


def setup_logging(
    level: Union[int, str] = DEFAULT_LEVEL,
    name: Optional[str] = None,
    format_str: str = DEFAULT_FORMAT,
    datefmt: str = DEFAULT_DATE_FORMAT,
    rich_tracebacks: bool = DEFAULT_RICH_TRACEBACKS,
    force: bool = False,
) -> logging.Logger:
    """
    Set up consistent logging with Rich formatting.

    This function ensures that the root logger is only configured once,
    and subsequent calls only adjust the level of the specified logger.

    Args:
        level: Logging level (default: INFO) - can be int or string like 'INFO', 'DEBUG'
        name: Logger name (default: root logger)
        format_str: Log format string
        datefmt: Date format string
        rich_tracebacks: Whether to enable rich tracebacks
        force: Force reconfiguration of the logger even if already initialized

    Returns:
        Configured logger instance
    """
    global _root_logger_initialized

    # Convert string level to int if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper(), DEFAULT_LEVEL)

    # Configure the root logger only once
    if not _root_logger_initialized or force:
        # Remove all existing handlers to avoid duplicates
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Configure with Rich handler
        logging.basicConfig(
            level=level,
            format=format_str,
            datefmt=datefmt,
            handlers=[RichHandler(rich_tracebacks=rich_tracebacks, console=console)],
        )
        _root_logger_initialized = True

    # Get or create the requested logger
    logger_name = name or ""  # Empty string for root logger

    # Check if we've already initialized this logger
    if logger_name in _initialized_loggers and not force:
        logger = _initialized_loggers[logger_name]
        # Update the level if it's different
        if logger.level != level:
            logger.setLevel(level)
        return logger

    # Setup a new logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Enable debug logging if DEBUG env var is set
    if os.environ.get("DEBUG") and logger_name:
        logger.setLevel(logging.DEBUG)

    # Store in initialized loggers
    _initialized_loggers[logger_name] = logger

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    If the logger has already been initialized with setup_logging,
    returns the existing logger. Otherwise, returns a new logger
    with default settings.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    if name in _initialized_loggers:
        return _initialized_loggers[name]

    # Create a new logger with default settings
    return setup_logging(name=name)
