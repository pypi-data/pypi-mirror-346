#!/usr/bin/env python3
"""
E2E test cleanup script for ncuploader.
Removes test directories, files, configuration, and index files.
"""

import shutil
from pathlib import Path

BASE_TEST_DIR_NAME = "e2e_test_data"
CONFIG_FILE_NAME = "e2e_config.yaml"
INDEX_FILE_NAME = "e2e_index.json"

def main():
    """Main function to clean up the e2e test environment."""
    print("Starting e2e test cleanup...")
    
    cwd = Path.cwd()
    base_dir_path = cwd / BASE_TEST_DIR_NAME
    config_file_path = cwd / CONFIG_FILE_NAME
    index_file_path = cwd / INDEX_FILE_NAME

    if base_dir_path.exists() and base_dir_path.is_dir():
        print(f"Removing test data directory: {base_dir_path.resolve()}")
        shutil.rmtree(base_dir_path)
    else:
        print(f"Test data directory not found or not a directory: {base_dir_path.resolve()}")

    if config_file_path.exists() and config_file_path.is_file():
        print(f"Removing configuration file: {config_file_path.resolve()}")
        config_file_path.unlink()
    else:
        print(f"Configuration file not found or not a file: {config_file_path.resolve()}")

    if index_file_path.exists() and index_file_path.is_file():
        print(f"Removing index file: {index_file_path.resolve()}")
        index_file_path.unlink()
    else:
        print(f"Index file not found or not a file: {index_file_path.resolve()}")

    print("\nCleanup complete.")

if __name__ == "__main__":
    main()