# tests/test_config.py
import os
import tempfile
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ncuploader.config import Config, load_config


def test_valid_config():
    """Test loading a valid configuration."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as temp_file:
        # Create a temporary file with valid config
        yaml.dump({
            "nextcloud": {
                "url": "https://nextcloud.example.com",
                "username": "testuser",
                "password": "testpass"
            },
            "uploads": [
                {
                    "local_path": Path.cwd().as_posix(),  # Current directory (guaranteed to exist)
                    "remote_path": "/test/destination",
                    "retention_policy": {
                        "delete_after_upload": "30d"
                    }
                }
            ]
        }, temp_file)
        temp_file.flush()  # Ensure the data is written to disk

        # Load and validate the config, but don't load from .env
        config = load_config(temp_file.name, load_dotenv_file=False)

        # Check values
        assert config.nextcloud.url == "https://nextcloud.example.com"
        assert config.nextcloud.username == "testuser"
        assert config.nextcloud.password.get_secret_value() == "testpass"
        assert len(config.uploads) == 1
        assert config.uploads[0].remote_path == "/test/destination"
        assert config.uploads[0].retention_policy.delete_after_upload == "30d"


def test_environment_variables_override():
    """Test that environment variables override config values."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as temp_file:
        # Create a temporary file with valid config
        yaml.dump({
            "nextcloud": {
                "url": "https://old.example.com",
                "username": "olduser",
                "password": "oldpass"
            },
            "uploads": [
                {
                    "local_path": str(Path.cwd()),
                    "remote_path": "/test/destination"
                }
            ]
        }, temp_file)
        temp_file.flush()

        # Set environment variables
        # Updated with mock patch
        from unittest.mock import patch
        
        with patch.dict(os.environ, {
            "NEXTCLOUD_URL": "https://new.example.com",
            "NEXTCLOUD_USERNAME": "newuser",
            "NEXTCLOUD_PASSWORD": "newpass"
        }):
            try:
                # Load config
                config = load_config(temp_file.name, load_dotenv_file=True)
    
                # Check that environment variables were used
                assert config.nextcloud.url == "https://new.example.com"
                assert config.nextcloud.username == "newuser"
                assert config.nextcloud.password.get_secret_value() == "newpass"
            finally:
                # Clean up environment
                del os.environ["NEXTCLOUD_URL"]
                del os.environ["NEXTCLOUD_USERNAME"]
                del os.environ["NEXTCLOUD_PASSWORD"]



def test_invalid_retention_policy():
    """Test validation fails with invalid retention policy."""
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as temp_file:
        # Create config with invalid retention policy
        yaml.dump({
            "nextcloud": {
                "url": "https://nextcloud.example.com",
                "username": "testuser",
                "password": "testpass"
            },
            "uploads": [
                {
                    "local_path": str(Path.cwd()),
                    "remote_path": "/test/destination",
                    "retention_policy": {
                        "delete_after_upload": "30x"  # Invalid unit
                    }
                }
            ]
        }, temp_file)
        temp_file.flush()

        # Should raise validation error
        with pytest.raises(ValidationError):
            load_config(temp_file.name, load_dotenv_file=False)