#!/usr/bin/env python3

import subprocess

from shell_prompt.cli import parser
from shell_prompt.config import config_manager
from shell_prompt.config import llm


def run_command(command: str, preview: bool):
    """
    Executes a shell command, asking for confirmation if preview mode is enabled.

    Args:
        command (str): The shell command to execute.
        preview (bool): Whether to prompt the user before execution.

    Returns:
        None
    """
    if preview:
        print(f"Command to run:\n{command}")
        confirm = input("Execute this command? [y/N]: ").strip().lower()
        if confirm in {"y", "yes"}:
            print(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)
        else:
            print("Aborted.")
    else:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True)


def main():
    """
    Entry point for the shell-prompt command-line tool.

    This function parses command-line arguments, updates and validates the configuration, and
    processes the user's natural language input to generate a shell command using an LLM. If the
    preview mode is enabled, it prompts the user to confirm before executing the generated command.

    Steps:
    1. Parse the command-line arguments.
    2. Update the configuration based on the arguments and validate it.
    3. If a command is provided, process it using the LLM and run the generated shell command.
    """
    args = parser.get_parser()

    config_manager.manage_config(args)
    config = config_manager.load_config()

    if args.command:
        config_manager.validate_config(config)
        response = llm.process_command(args.command, config)
        run_command(response, config["preview"])


if __name__ == "__main__":
    main()
