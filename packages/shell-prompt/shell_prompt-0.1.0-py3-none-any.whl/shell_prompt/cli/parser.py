import argparse

from shell_prompt.__version__ import __version__
from shell_prompt.config import provider_data


def get_parser() -> argparse.Namespace:
    """
    Creates and returns the command-line argument parser for the shell-prompt tool.

    This parser defines arguments for version, configuration, provider, model, API key, preview
    mode, and the natural language command to be processed.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Shell Prompt: A CLI tool that converts natural language to shell commands" \
                     "and executes them.")
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--config", action="store_true", help="Show program's configuration.")
    parser.add_argument("--set-provider",
                        type=str,
                        choices=provider_data.AVAILABLE_PROVIDERS,
                        help="Set the LLM provider (e.g., 'openai', 'google-genai', 'anthropic')")
    parser.add_argument("--set-model", type=str, help="Set the specific model.")
    parser.add_argument("--set-api-key",
                        type=str,
                        help="Set api-key for currently selected provider")
    parser.add_argument("--preview",
                        action=argparse.BooleanOptionalAction,
                        help="Enable or disable preview mode (e.g., --preview or --no-preview).")
    parser.add_argument("command",
                        nargs="?",
                        type=str,
                        help="The natural language command to process.")
    return parser.parse_args()
