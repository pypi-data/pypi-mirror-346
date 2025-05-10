import os
import json
import logging
import platform
import sys

from pathlib import Path

from argparse import Namespace
from shell_prompt.config import provider_data


def get_config_path() -> Path:
    """
    Returns the path to the configuration file.

    This function determines the correct directory for storing the configuration file based on the
    operating system. It creates the necessary directories if they do not exist and returns the path 
    to the 'config.json' file within the appropriate configuration directory.

    On Windows, it uses the 'LOCALAPPDATA/shell-prompt' directory.
    On other systems, it uses the '~/.config/shell-prompt' directory.

    Returns:
        pathlib.Path: The full path to the configuration file.
    """
    if platform.system() == "Windows":
        local_appdata = Path(os.environ.get("LOCALAPPDATA"))
        config_dir = local_appdata / "shell-prompt"
    else:
        home_dir = Path.home()
        config_dir = home_dir / ".config" / "shell-prompt"

    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.json"
    return config_file


def load_config() -> dict:
    """
    Loads and returns the configuration from the config file.

    This function checks if the configuration file exists. If not, it creates a default
    configuration file with initial values. It then loads the configuration from the file and
    returns it as a dictionary. If the configuration file is corrupt or contains invalid JSON, an
    error is raised.

    Returns:
        dict: The loaded configuration as a dictionary.

    Raises:
        ValueError: If the config file is corrupt or contains invalid JSON.
    """
    config_file = get_config_path()

    if not config_file.exists():
        with open(config_file, "w", encoding="utf-8") as file:
            json.dump({
                "api_keys": {},
                "provider": "",
                "model": "",
                "preview": True
            }, file, indent=4)

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Error: config file {config_file} is corrupt or contains invalid JSON."
        ) from exc



def edit_config(edit_dict: dict) -> None:
    """
    Updates the configuration file with the provided key-value pairs.

    This function loads the current configuration, checks and logs a warning for any invalid keys.
    It then updates the configuration with the valid keys from the provided dictionary and saves the
    updated configuration. Afterward, it logs the updates made to the configuration.

    Args:
        edit_dict (dict): A dictionary of key-value pairs to update in the config.

    Logs:
        - A warning if any invalid keys are attempted to be updated.
        - An info message for each valid key updated.
    """
    config = load_config()
    invalid_keys = [key for key in edit_dict if key not in config]
    if invalid_keys:
        logging.warning("Attempted to update invalid keys: %s", ", ".join(invalid_keys))

    config.update({key: value for key, value in edit_dict.items() if key in config})
    save_config(config)

    for key, value in edit_dict.items():
        if key in config:
            logging.info("Configuration '%s' updated to: %s", key, value)


def save_config(config: dict) -> None:
    """
    Saves the configuration dictionary to the config file in JSON format.

    Args:
        config (dict): The configuration data to save.
    """
    config_file = get_config_path()
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def manage_config(args: Namespace) -> None:
    """
    Updates and manages the configuration based on command-line arguments.
    
    This function modifies the configuration settings such as the provider, model, and API key based
    on user input. It also prints the current configuration if the '--config' argument is provided.
    
    Args:
        args (Namespace): Parsed command-line arguments containing the configuration options and
                          commands to modify.
    """
    if provider := args.set_provider:
        edit_config({"provider": provider})
    if model := args.set_model:
        edit_config({"model": model})
    if api_key := args.set_api_key:
        config = load_config()
        provider = config.get("provider")
        if not provider:
            print("Error: trying to set API key for provider=None."
                  "Set the provider first with --set-provider")
            sys.exit(1)
        new_config = config.get("api_keys", {})
        new_config[provider] = api_key
        edit_config({"api_keys": new_config})
    if args.preview is not None:
        edit_config({"preview": args.preview})
    if args.config:
        config = load_config()
        print(config)
        sys.exit(0)


def validate_config(config: dict):
    """
    Validates the configuration dictionary to ensure all required fields are present 
    and have valid values.

    This includes checking for:
    - A valid provider from the available options
    - A specified model
    - A valid API key for the selected provider
    - A properly formatted 'preview' value

    Args:
        config (dict): The configuration dictionary to validate.

    Raises:
        ValueError: If any of the required fields are missing or invalid.
    """
    provider = config.get("provider")
    if provider not in provider_data.AVAILABLE_PROVIDERS:
        raise ValueError("Invalid or missing provider."
                         f"Must be one of: {list(provider_data.AVAILABLE_PROVIDERS)}")

    model = config.get("model")
    if not model:
        raise ValueError("Missing 'model' in config.")

    api_keys = config.get("api_keys", {})
    if provider not in api_keys or not api_keys[provider]:
        raise ValueError(f"Missing API key for provider '{provider}' in config['api_keys'].")

    preview = config.get("preview")
    if preview in ["true", "false"]:
        preview = preview == "true"
    if preview not in [True, False]:
        raise ValueError("Invalid 'preview' value; should be true/false or omitted.")
