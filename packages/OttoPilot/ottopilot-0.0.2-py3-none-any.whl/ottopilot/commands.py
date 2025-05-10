"""
Command utilities for running shell commands.
"""

import subprocess
from typing import List, Optional, Tuple, Union

from ottopilot.log_utils import get_logger

# Get logger
logger = get_logger("ottopilot.commands")


def run_command(
    cmd: Union[str, List[str]],
    input_text: Optional[str] = None,
    check: bool = True,
    capture_output: bool = False,
) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Run a shell command with proper logging and error handling.

    Args:
        cmd: Command to run (string or list of strings)
        input_text: Optional input to pass to the command
        check: Whether to raise an exception on non-zero return code
        capture_output: Whether to capture and return stdout/stderr

    Returns:
        Tuple of (return_code, stdout, stderr)

    Raises:
        subprocess.CalledProcessError: If the command returns non-zero and check is True
        FileNotFoundError: If the command is not found and check is True
    """
    # Standardize command representation for logging and execution
    if isinstance(cmd, str):
        cmd_str = cmd
        shell = True
    else:
        cmd_str = " ".join(str(part) for part in cmd)
        shell = False

    logger.debug(f"Running command: {cmd_str}")

    # Configure subprocess I/O based on parameters
    run_kwargs = {
        "text": True,
        "shell": shell,
    }

    if capture_output:
        run_kwargs["stdout"] = subprocess.PIPE
        run_kwargs["stderr"] = subprocess.PIPE

    # Handle command with input differently than command without input
    try:
        if input_text is not None:
            run_kwargs["stdin"] = subprocess.PIPE
            with subprocess.Popen(cmd, **run_kwargs) as proc:
                stdout_text, stderr_text = proc.communicate(input=input_text)
                returncode = proc.returncode
        else:
            # Don't set check=True here - we want to handle errors ourselves
            result = subprocess.run(cmd, **run_kwargs)
            returncode = result.returncode
            stdout_text = result.stdout if capture_output else None
            stderr_text = result.stderr if capture_output else None

        # Log command result based on return code
        if returncode != 0:
            logger.warning(f"Command exited with code {returncode}: {cmd_str}")
            if stderr_text and stderr_text.strip():
                logger.warning(f"Command stderr: {stderr_text.strip()}")
            if check:
                # Create a CalledProcessError but don't raise it yet
                # This allows us to use the same error handling code path
                error = subprocess.CalledProcessError(returncode, cmd)
                error.stdout = stdout_text
                error.stderr = stderr_text
                raise error
        else:
            logger.debug(f"Command completed successfully: {cmd_str}")

        return returncode, stdout_text, stderr_text

    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with code {e.returncode}: {cmd_str}")
        if hasattr(e, "stderr") and e.stderr and e.stderr.strip():
            logger.error(f"Command stderr: {e.stderr.strip()}")
        if check:
            raise
        return (
            e.returncode,
            e.stdout if hasattr(e, "stdout") else None,
            e.stderr if hasattr(e, "stderr") else None,
        )

    except FileNotFoundError as e:
        error_msg = f"Command not found: {cmd_str}"
        logger.error(error_msg)
        if check:
            raise FileNotFoundError(error_msg) from e
        return 127, None, error_msg  # 127 is standard "command not found" exit code
