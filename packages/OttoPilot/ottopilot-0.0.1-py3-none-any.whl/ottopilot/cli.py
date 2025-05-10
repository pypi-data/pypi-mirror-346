"""
OttoPilot CLI module.

This module provides a concise CLI for running AI tools with claude, managing
context from AGENTS.md, bin/ commands, and task files.
"""

from pathlib import Path
from typing import List, Optional

import typer

from ottopilot import run_command, setup_logging

# Setup application and logging
app = typer.Typer(help="OttoPilot CLI for the Ascend product repository.")
logger = setup_logging(name="ottopilot")


def build_prompt(task_path: Optional[str] = None, no_task: bool = False) -> str:
    """Build the initial prompt for claude with appropriate context.

    Args:
        task_path: Optional path to a task file. If None, defaults to 'task.md'
        no_task: If True, ignores task file even if it exists

    Returns:
        A formatted prompt string with appropriate context and instructions
    """
    prompt = "Carefully read @AGENTS.md. Utilities are available in @bin. "

    # Handle no-task mode or standard mode with task file checking
    if no_task:
        prompt += (
            "Do not do anything. Wait for further instructions in my next message."
        )
        logger.info("Task file ignored due to --no-task flag")
        return prompt

    # Check for task file existence
    task_file = Path(task_path) if task_path else Path("task.md")
    if task_file.exists():
        prompt += f"Execute on @{task_file}."
        logger.info(f"Using task file: {task_file}")
    else:
        prompt += (
            "Do not do anything. Wait for further instructions in my next message."
        )
        logger.warning(f"Task file not found: {task_file}")

    return prompt


@app.command()
def main(
    args: Optional[List[str]] = typer.Argument(None, help="Prompt to send to claude"),
    task: Optional[str] = typer.Option(
        None, "--task", "-t", help="Path to task file (defaults to 'task.md')"
    ),
    no_task: bool = typer.Option(
        False, "--no-task", "-n", help="Ignore task.md file even if it exists"
    ),
    headless: bool = typer.Option(
        False, "--headless", "-h", help="Run in headless mode (no REPL)"
    ),
) -> int:
    """
    OttoPilot CLI for the Ascend product repository.

    Launches claude with context from AGENTS.md, bin/, and optional task file.
    Any additional arguments are passed as a prompt to claude.

    Args:
        args: Optional prompt text to send to claude
        task: Path to task file (defaults to 'task.md' in current directory)
        no_task: If True, ignores task file even if it exists
        headless: If True, runs in non-interactive mode (no REPL)

    Returns:
        Return code from the claude process
    """
    initial_prompt = build_prompt(task, no_task)
    cmd = ["claude", "--dangerously-skip-permissions"]

    # Handle headless mode (no REPL)
    if headless:
        cmd.append("--print")

    # Handle command execution consistently whether args are provided or not
    if args:
        # If args provided, override task instructions with custom prompt
        prompt_args = " ".join(args)
        # Strip the "wait for instructions" text if present
        base_context = "Carefully read @AGENTS.md. Utilities are available in @bin. "
        combined_prompt = f"{base_context}{prompt_args}"
        logger.info(
            f"Running claude with override prompt: {prompt_args[:50]}{'...' if len(prompt_args) > 50 else ''}"
        )
    else:
        # No args provided, just use the initial prompt
        combined_prompt = initial_prompt
        task_file = Path(task) if task else Path("task.md")
        logger.info(
            f"Running claude with task file: {task_file if task_file.exists() else 'None'}"
        )

    # Add the prompt to the command arguments instead of using stdin
    cmd.append(combined_prompt)

    # Run claude with the prompt as a command argument
    if headless:
        # In headless mode, capture the output
        returncode, stdout, stderr = run_command(cmd, check=False, capture_output=True)
        # Handle stdout and stderr
        if stdout:
            print(stdout)
        if stderr and stderr.strip():
            logger.error(f"claude stderr: {stderr}")
    else:
        # In interactive mode, don't capture output to allow proper REPL behavior
        returncode, _, _ = run_command(cmd, check=False)

    return returncode


def cli_entry_point():
    """Entry point for the ottopilot command."""
    app()

if __name__ == "__main__":
    app()