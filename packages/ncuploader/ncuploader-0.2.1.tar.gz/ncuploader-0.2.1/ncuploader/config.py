# ncuploader/config.py
"""
Configuration handling for NCUploader.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Union, Optional

from loguru import logger
import os
from pydantic import BaseModel, Field, SecretStr, field_validator
from pathlib import Path
import yaml


class NextcloudConfig(BaseModel):
    url: str
    username: str
    password: SecretStr

    model_config = {
        "env_prefix": "NEXTCLOUD_"
    }

class RetentionPolicyConfig(BaseModel):
    delete_after_upload: Optional[str] = None

    @field_validator("delete_after_upload")
    def validate_retention_string(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        import re
        if not re.match(r"^\d+[dwmys]$|^never$", value, re.IGNORECASE):
            raise ValueError(
                "Invalid retention policy string. Must be like '30d', '4w', '1m', '1y', '60s', or 'never'."
            )
        return value.lower()

class UploadItem(BaseModel):
    local_path: Path
    remote_path: str
    retention_policy: Optional[RetentionPolicyConfig] = None

    @field_validator("local_path", mode="before")
    def ensure_path_object(cls, value: Any) -> Path:
        if isinstance(value, str):
            return Path(value).expanduser()
        if not isinstance(value, Path):
            raise ValueError("local_path must be a string or Path object")
        return value.expanduser()

class Config(BaseModel):
    nextcloud: NextcloudConfig
    uploads: List[UploadItem] = []
    index_path: Path = Field(default_factory=lambda: Path("ncuploader_index.json"))
    dry_run: bool = False


from pydantic import ValidationError

def load_config(config_path: str | Path, load_dotenv_file: bool = True) -> Config:
    """
    Load configuration from a YAML file and environment variables.

    Args:
        config_path: Path to the configuration file
        load_dotenv_file: Whether to load .env file (for testing)

    Returns:
        Configuration object

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        ValueError: If the configuration is invalid (e.g., YAML format, validation error)
    """
    config_path_obj = Path(config_path)

    if not config_path_obj.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path_obj}")

    try:
        with open(config_path_obj, 'r') as f:
            parsed_yaml_data = yaml.safe_load(f)

        # Ensure config_data_for_validation is a dict, even if YAML is empty or not a dict root.
        config_data_for_validation = parsed_yaml_data if isinstance(parsed_yaml_data, dict) else {}

        if load_dotenv_file:  # This flag indicates whether to allow env vars to override YAML
            # Ensure 'nextcloud' key exists and is a dict for updating
            if "nextcloud" not in config_data_for_validation or \
               not isinstance(config_data_for_validation.get("nextcloud"), dict):
                config_data_for_validation["nextcloud"] = {}
            
            # Apply environment variable overrides for Nextcloud settings
            if "NEXTCLOUD_URL" in os.environ:
                config_data_for_validation["nextcloud"]["url"] = os.environ["NEXTCLOUD_URL"]
            if "NEXTCLOUD_USERNAME" in os.environ:
                config_data_for_validation["nextcloud"]["username"] = os.environ["NEXTCLOUD_USERNAME"]
            if "NEXTCLOUD_PASSWORD" in os.environ:
                config_data_for_validation["nextcloud"]["password"] = os.environ["NEXTCLOUD_PASSWORD"]
        
        # Pydantic will validate the structure and raise ValidationError for missing/invalid fields.
        validated_config = Config.model_validate(config_data_for_validation)
        return validated_config

    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration from {config_path_obj}: {e}")
        raise ValueError(f"Invalid YAML format in {config_path_obj}: {e}") from e
    except ValidationError: # Pydantic's validation error
        # Logger call can be added here if specific logging for ValidationError is needed
        # logger.error(f"Configuration validation error for {config_path_obj}: {e}")
        raise # Re-raise Pydantic's ValidationError to be caught by tests or calling code
    except Exception as e:
        logger.error(f"Unexpected error loading configuration from {config_path_obj}: {e}")
        # Wrap unexpected errors in a ValueError or re-raise if appropriate
        raise ValueError(f"Unexpected error loading configuration from {config_path_obj}: {e}") from e