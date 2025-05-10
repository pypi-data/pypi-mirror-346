#!/usr/bin/env python3
"""
E2E test preparation script for ncuploader.
Creates test directories, files, and generates a configuration file.
"""

import os
import random
import string
import shutil
from pathlib import Path
import yaml
from dotenv import load_dotenv
from nc_py_api import Nextcloud, NextcloudApp, FsNode # Added FsNode
from nc_py_api._exceptions import NextcloudExceptionNotFound # Import NextcloudExceptionNotFound

BASE_TEST_DIR_NAME = "e2e_test_data"
CONFIG_FILE_NAME = "e2e_config.yaml"
INDEX_FILE_NAME = "e2e_index.json"
REMOTE_BASE_TEST_DIR = "/test-upload" # Define remote base directory

def generate_random_text(size_kb=10):
    """Generate random text content of specified size in KB."""
    chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"
    return ''.join(random.choice(chars) for _ in range(size_kb * 1024))

def generate_random_binary(size_mb=1):
    """Generate random binary content of specified size in MB."""
    return os.urandom(size_mb * 1024 * 1024)

def create_test_files_in_dir(base_dir: Path):
    """Create test directories and files within the given base directory."""
    # Create directory structure
    dirs_to_create = [
        base_dir / "dir1",
        base_dir / "dir1" / "subdir1",
        base_dir / "dir2"
    ]
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory.resolve()}")

    # Create text files
    text_files_to_create = [
        base_dir / "file1.txt",
        base_dir / "dir1" / "file2.txt",
        base_dir / "dir1" / "subdir1" / "file3.txt"
    ]
    for i, file_path in enumerate(text_files_to_create):
        with open(file_path, 'w') as f:
            f.write(generate_random_text(size_kb=5 * (i + 1)))
        print(f"Created text file: {file_path.resolve()} ({file_path.stat().st_size} bytes)")

    # Create binary files
    binary_files_to_create = [
        (base_dir / "binary1.dat", 1),  # 1MB
        (base_dir / "dir2" / "binary2.dat", 3)  # 3MB
    ]
    for file_path, size in binary_files_to_create:
        with open(file_path, 'wb') as f:
            f.write(generate_random_binary(size_mb=size))
        print(f"Created binary file: {file_path.resolve()} ({file_path.stat().st_size} bytes)")

    # Create files with short retention period
    short_retention_files_to_create = [
        base_dir / "short_retention1.txt",
        base_dir / "dir1" / "short_retention2.txt",
    ]
    for file_path in short_retention_files_to_create:
        with open(file_path, 'w') as f:
            f.write(generate_random_text(size_kb=1))
        print(f"Created short retention file: {file_path.resolve()} ({file_path.stat().st_size} bytes)")

    created_files = text_files_to_create + [f[0] for f in binary_files_to_create] + short_retention_files_to_create
    created_dirs = dirs_to_create
    return created_files, created_dirs

def create_config_file_for_e2e(test_files: list[Path], test_dirs: list[Path], config_output_path: Path, index_file_path: Path):
    """Create a configuration file for ncuploader."""
    load_dotenv()

    nextcloud_url = os.getenv("NEXTCLOUD_URL", "https://your-nextcloud-instance.com")
    nextcloud_username = os.getenv("NEXTCLOUD_USERNAME", "your_username")
    nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD", "your_password")

    uploads = []

    # Add individual files
    for file_path in test_files:
        if file_path.is_file():
            remote_p = f"{REMOTE_BASE_TEST_DIR}/{file_path.name}" # Use REMOTE_BASE_TEST_DIR
            retention = "1s" if "short_retention" in file_path.name else "30d"
            uploads.append({
                "local_path": str(file_path.resolve()),
                "remote_path": remote_p,
                "retention_policy": {"delete_after_upload": retention}
            })

    # Add directories
    for dir_path in test_dirs:
        if dir_path.is_dir():
            remote_p = f"{REMOTE_BASE_TEST_DIR}/{dir_path.name}" # Use REMOTE_BASE_TEST_DIR
            uploads.append({
                "local_path": str(dir_path.resolve()),
                "remote_path": remote_p,
                "retention_policy": {"delete_after_upload": None}
            })

    config = {
        "nextcloud": {
            "url": nextcloud_url,
            "username": nextcloud_username,
            "password": nextcloud_password
        },
        "uploads": uploads,
        "index_path": str(index_file_path.resolve())
    }

    with open(config_output_path, 'w') as f:
        yaml.dump(config, f)
    print(f"Created configuration file: {config_output_path.resolve()}")

def cleanup_remote_nextcloud(nc: Nextcloud):
    """Clean up the remote Nextcloud test directory."""
    print(f"Attempting to remove remote directory: {REMOTE_BASE_TEST_DIR}")
    try:
        # Check existence by trying to list the directory. If it doesn't exist, listdir will raise an exception.
        # If it exists and is a file, listdir might also behave differently or error, 
        # but for a directory, it should list contents or be empty.
        # A more direct check would be nc.files.stat(REMOTE_BASE_TEST_DIR), which raises an exception if not found.
        try:
            nc.files.stat(REMOTE_BASE_TEST_DIR) # Check if path exists
            # If stat succeeds, the path exists. Proceed to delete.
            print(f"Remote directory {REMOTE_BASE_TEST_DIR} exists. Attempting to delete.")
            nc.files.delete(REMOTE_BASE_TEST_DIR) # nc.files.delete is recursive for directories
            print(f"Successfully removed remote directory: {REMOTE_BASE_TEST_DIR}")
        except NextcloudExceptionNotFound: # Specific exception for path not found
            print(f"Remote directory not found, no cleanup needed: {REMOTE_BASE_TEST_DIR}")
        except Exception as e_stat_delete: # Catch other potential errors during stat or delete
            print(f"Error during remote cleanup of {REMOTE_BASE_TEST_DIR} (stat or delete): {e_stat_delete}")
            print("Continuing with test preparation, but conflicts might occur.")

    except Exception as e_outer: # Catch any other unexpected errors in the cleanup logic itself
        print(f"An unexpected error occurred in cleanup_remote_nextcloud for {REMOTE_BASE_TEST_DIR}: {e_outer}")
        print("Continuing with test preparation, but conflicts might occur.")


def main():
    """Main function to prepare the e2e test environment."""
    print("Starting e2e test preparation...")
    load_dotenv() # Load .env for Nextcloud credentials

    nextcloud_url = os.getenv("NEXTCLOUD_URL")
    nextcloud_username = os.getenv("NEXTCLOUD_USERNAME")
    nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD")

    if not all([nextcloud_url, nextcloud_username, nextcloud_password]):
        print("Error: NEXTCLOUD_URL, NEXTCLOUD_USERNAME, and NEXTCLOUD_PASSWORD must be set in .env or environment.")
        return

    try:
        # Corrected Nextcloud client instantiation with keyword arguments
        nc_client = Nextcloud(nextcloud_url=nextcloud_url, nc_auth_user=nextcloud_username, nc_auth_pass=nextcloud_password)
        nc_client.update_server_info() # Ensures connection and authentication
        print(f"Successfully connected to Nextcloud: {nextcloud_url}")
        cleanup_remote_nextcloud(nc_client) # Perform remote cleanup
    except Exception as e:
        print(f"Error connecting to Nextcloud or during initial remote cleanup: {e}")
        print("Proceeding with local setup, but remote operations might fail or conflict.")

    cwd = Path.cwd()
    base_dir_path = cwd / BASE_TEST_DIR_NAME
    config_file_path = cwd / CONFIG_FILE_NAME
    index_file_path = cwd / INDEX_FILE_NAME

    # Clean up from previous run if necessary
    if base_dir_path.exists():
        print(f"Removing existing test data directory: {base_dir_path.resolve()}")
        shutil.rmtree(base_dir_path)
    if config_file_path.exists():
        print(f"Removing existing config file: {config_file_path.resolve()}")
        config_file_path.unlink(missing_ok=True)
    if index_file_path.exists():
        print(f"Removing existing index file: {index_file_path.resolve()}")
        index_file_path.unlink(missing_ok=True)

    base_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Created base test directory: {base_dir_path.resolve()}")

    created_files, created_dirs = create_test_files_in_dir(base_dir_path)
    create_config_file_for_e2e(created_files, created_dirs, config_file_path, index_file_path)

    print("\nPreparation complete.")
    print(f"Test data directory: {base_dir_path.resolve()}")
    print(f"Config file: {config_file_path.resolve()}")
    print(f"Index file will be created at: {index_file_path.resolve()}")

if __name__ == "__main__":
    main()