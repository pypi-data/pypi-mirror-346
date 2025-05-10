"""
Logging utilities for consistent logging across scripts.
"""

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

# Create console instance
console = Console()


def setup_logging(
    level: int = logging.INFO,
    name: Optional[str] = None,
    format_str: str = "%(message)s",
    datefmt: str = "[%X]",
    rich_tracebacks: bool = True,
) -> logging.Logger:
    """
    Set up consistent logging with Rich formatting.

    Args:
        level: Logging level (default: INFO)
        name: Logger name (default: root logger)
        format_str: Log format string
        datefmt: Date format string
        rich_tracebacks: Whether to enable rich tracebacks

    Returns:
        Configured logger instance
    """
    # Configure the root logger
    logging.basicConfig(
        level=level,
        format=format_str,
        datefmt=datefmt,
        handlers=[RichHandler(rich_tracebacks=rich_tracebacks, console=console)],
    )

    # Get the requested logger (or root logger if none specified)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
