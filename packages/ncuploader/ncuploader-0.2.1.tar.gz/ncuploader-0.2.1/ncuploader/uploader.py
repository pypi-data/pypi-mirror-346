# ncuploader/uploader.py
"""
Core functionality for uploading files to Nextcloud.
"""

from datetime import datetime, UTC
from pathlib import Path
from typing import List, Any, Optional, Union, Tuple

from .config import Config  # Added Config import

from nc_py_api import Nextcloud  # Changed NextcloudApp to Nextcloud
from loguru import logger

from .retention import RetentionPolicy
from .index import UploadIndex, IndexEntry, load_index, save_index


class NextcloudUploader:
    """Main class for uploading files to Nextcloud with retention policies."""

    def __init__(self, config: Config):  # Changed type hint to Config
        """
        Initialize the uploader with configuration.

        Args:
            config: Configuration object with Nextcloud credentials and settings
        """
        self.config = config
        self.nc_client = self._connect_to_nextcloud()
        self.index_path = Path(config.index_path)  # Changed to attribute access
        self.index = load_index(self.index_path)
        self.dry_run = config.dry_run

    def _connect_to_nextcloud(self) -> Nextcloud:  # Changed return type hint
        """Create and return a Nextcloud client connection."""
        if not self.config.nextcloud:
            raise ValueError("Missing Nextcloud configuration section")

        url = str(self.config.nextcloud.url)  # Attribute access, ensure string
        username = self.config.nextcloud.username    # Attribute access
        password = self.config.nextcloud.password.get_secret_value()  # Attribute access and get secret

        if not all([url, username, password]):
            raise ValueError("Missing Nextcloud configuration (url, username, or password)")

        # Use Nextcloud from nc_py_api for client applications
        client = Nextcloud(nextcloud_url=url, nc_auth_user=username, nc_auth_pass=password)
        # For Nextcloud class, explicit login might be needed or handled by first API call
        # Checking if perform_login is necessary or if it's handled automatically.
        # Based on nc_py_api, login is typically handled by the first request or can be called explicitly.
        # For simplicity and to ensure connection, let's try to update server info which implies login.
        try:
            client.update_server_info()  # This will attempt to connect and authenticate
        except Exception as e:
            logger.error(f"Failed to connect to Nextcloud or authenticate: {e}")
            raise ValueError(f"Failed to connect/authenticate: {e}") from e
        return client

    def upload_file(self,
                    local_path: Union[str, Path],
                    remote_path: str,
                    retention_policy: Optional[RetentionPolicy] = None) -> bool:
        """
        Upload a single file to Nextcloud.

        Args:
            local_path: Path to the local file
            remote_path: Destination path on Nextcloud
            retention_policy: Optional retention policy for the file

        Returns:
            True if upload successful, False otherwise
        """
        local_path = Path(local_path)

        if not local_path.exists() or not local_path.is_file():
            logger.error(f"File not found: {local_path}")
            return False

        # Check if already uploaded
        if self.index.has_entry(local_path, remote_path):
            logger.info(f"Already uploaded: {local_path} -> {remote_path}")
            return True

        try:
            if self.dry_run:
                logger.info(f"[DRY RUN] Would upload file: {local_path} -> {remote_path}")
            else:
                # Perform the upload using nc_py_api syntax
                with open(local_path, "rb") as f:
                    self.nc_client.files.upload_stream(remote_path, f)

            # Add to index
            self.index.add_entry(
                local_path=local_path,
                remote_path=remote_path,
                retention_policy=retention_policy.to_dict() if retention_policy else None
            )

            # Save index
            save_index(self.index, self.index_path)

            logger.info(f"Uploaded file: {local_path} -> {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Error uploading file {local_path}: {e}")
            return False

    def upload_directory(self,
                         local_path: Union[str, Path],
                         remote_path: str,
                         retention_policy: Optional[RetentionPolicy] = None) -> Tuple[int, int]:
        """
        Upload a directory to Nextcloud.

        Args:
            local_path: Path to the local directory
            remote_path: Destination path on Nextcloud
            retention_policy: Optional retention policy for the directory

        Returns:
            Tuple of (successful_uploads, failed_uploads)
        """
        local_path = Path(local_path)

        if not local_path.exists() or not local_path.is_dir():
            logger.error(f"Directory not found: {local_path}")
            return (0, 0)

        # Check if directory itself is already uploaded
        if self.index.has_entry(local_path, remote_path):
            logger.info(f"Already uploaded: {local_path} -> {remote_path}")
        else:
            # Create directory on Nextcloud using nc_py_api syntax
            try:
                # Ensure parent directories exist
                parent_path = Path(remote_path).parent
                current_check_path = ""
                # Split the parent path and create each segment if it doesn't exist
                # Ensure leading slash is handled correctly for absolute paths on Nextcloud
                path_segments = [seg for seg in str(parent_path).split('/') if seg]
                if str(parent_path).startswith('/'):
                    current_check_path = '/'
                
                for segment in path_segments:
                    if not current_check_path.endswith('/') and current_check_path != '/': # Avoid double slashes unless it's just root
                        current_check_path += '/'
                    current_check_path += segment
                    if current_check_path == '/': # Skip if it's just the root, cannot create root
                        continue
                    # if not self.nc_client.files.exists(current_check_path):
                    #    logger.info(f"Creating parent directory: {current_check_path}")
                    #    self.nc_client.files.mkdir(current_check_path)
                    try:
                        # listdir will raise an exception if the path does not exist (e.g. a 404 from server)
                        # or return a list of FsNode objects if it does.
                        self.nc_client.files.listdir(current_check_path) 
                        logger.debug(f"Parent directory/path {current_check_path} already exists.")
                    except Exception as e: # Broad exception, ideally should be more specific if nc_py_api has custom exceptions for 404
                        logger.info(f"Parent directory/path {current_check_path} not found or error accessing: {e}. Attempting to create.")
                        if not self.dry_run:
                            self.nc_client.files.mkdir(current_check_path)
                        else:
                            logger.info(f"[DRY RUN] Would create parent directory: {current_check_path}")
                
                # Now create the target directory if it doesn't exist
                try:
                    self.nc_client.files.listdir(remote_path)
                    logger.info(f"Target directory {remote_path} already exists.")
                except Exception as e:
                    logger.info(f"Target directory {remote_path} not found or error accessing: {e}. Attempting to create.")
                    if not self.dry_run:
                        self.nc_client.files.mkdir(remote_path)
                    else:
                        logger.info(f"[DRY RUN] Would create target directory: {remote_path}")

                # Add to index
                self.index.add_entry(
                    local_path=local_path,
                    remote_path=remote_path,
                    retention_policy=retention_policy.to_dict() if retention_policy else None
                )

                save_index(self.index, self.index_path)

                logger.info(f"Created directory: {remote_path}")
            except Exception as e:
                logger.warning(f"Error creating directory {remote_path}: {e}")

        # Upload files in the directory
        success_count = 0
        fail_count = 0

        for item in local_path.iterdir():
            if item.is_file():
                remote_file_path = f"{remote_path}/{item.name}"
                success = self.upload_file(item, remote_file_path, retention_policy)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            elif item.is_dir():
                remote_dir_path = f"{remote_path}/{item.name}"
                s, f = self.upload_directory(item, remote_dir_path, retention_policy) # Pass original retention_policy for subdirs
                success_count += s
                fail_count += f

        return (success_count, fail_count)

    def process_retention_policies(self) -> List[str]:
        """
        Process retention policies and delete expired files.

        Returns:
            List of deleted file paths
        """
        entries_to_delete = self.index.list_entries_to_delete()
        deleted_files = []

        for entry in entries_to_delete:
            logger.info(f"Deleting {entry.remote_path} due to expired retention policy")
            try:
                if self.dry_run:
                    logger.info(f"[DRY RUN] Would delete {entry.remote_path} due to expired retention policy")
                else:
                    self.nc_client.files.delete(entry.remote_path)  # Use nc_py_api syntax
                self.index.remove_entry(Path(entry.local_path), entry.remote_path)
                deleted_files.append(entry.remote_path)
            except Exception as e:
                logger.error(f"Error deleting {entry.remote_path}: {e}")

        # Save index after processing
        save_index(self.index, self.index_path)

        return deleted_files

    def process_uploads(self) -> Tuple[int, int]:
        """
        Process all uploads defined in the configuration.

        Returns:
            Tuple of (successful_uploads, failed_uploads)
        """
        success_count = 0
        fail_count = 0

        for upload_item in self.config.uploads:  # Changed to attribute access and iterate over UploadItem objects
            local_path = Path(upload_item.local_path)
            remote_path = upload_item.remote_path

            # Parse retention policy if present
            parsed_retention_policy: Optional[RetentionPolicy] = None
            if upload_item.retention_policy and upload_item.retention_policy.delete_after_upload:
                parsed_retention_policy = RetentionPolicy(
                    delete_after_upload=upload_item.retention_policy.delete_after_upload
                )

            if local_path.is_file():
                success = self.upload_file(local_path, remote_path, parsed_retention_policy)
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            elif local_path.is_dir():
                s, f = self.upload_directory(local_path, remote_path, parsed_retention_policy)
                success_count += s
                fail_count += f
            else:
                logger.error(f"Path not found: {local_path}")
                fail_count += 1

        # Process retention policies
        self.process_retention_policies()

        return (success_count, fail_count)

    def close(self):
        """Close connections and clean up resources."""
        # Save index one last time
        save_index(self.index, self.index_path)
        # No explicit close needed for nextcloud client