# ncuploader/index.py
"""
Index for tracking uploaded files and their retention policies.
"""

import json
import re
from datetime import datetime, timedelta, UTC
from pathlib import Path
from typing import Dict, List, Any

from loguru import logger
from pydantic import BaseModel


class IndexEntry(BaseModel):
    """Entry in the upload index."""
    local_path: Path
    remote_path: str
    upload_time: datetime
    retention_policy: Dict[str, Any] | None = None

    def should_delete(self, current_time=None) -> bool:
        """
        Check if this entry should be deleted based on retention policy.

        Args:
            current_time: The current time for comparison (defaults to now)

        Returns:
            True if the file should be deleted, False otherwise
        """
        if not self.retention_policy:
            return False

        if "delete_after_upload" not in self.retention_policy or not self.retention_policy["delete_after_upload"]:
            return False

        # Get current time
        if current_time is None:
            current_time = datetime.now(UTC)

        # Parse retention period
        retention = self.retention_policy["delete_after_upload"]
        pattern = r'^(\d+)([a-zA-Z]+)$'
        match = re.match(pattern, retention)

        if not match:
            logger.warning(f"Invalid retention format: {retention}")
            return False

        value = int(match.group(1))
        unit = match.group(2)

        # Calculate timedelta based on the unit
        if unit == 'd':
            delta = timedelta(days=value)
        elif unit == 'h':
            delta = timedelta(hours=value)
        elif unit == 'min':
            delta = timedelta(minutes=value)
        elif unit == 's':
            delta = timedelta(seconds=value)
        elif unit == 'w':
            delta = timedelta(weeks=value)
        elif unit == 'y':
            # Approximate - using 365.25 days per year
            delta = timedelta(days=value * 365.25)
        else:
            logger.warning(f"Unknown retention unit: {unit}")
            return False

        # Check if the file should be deleted
        expiry_time = self.upload_time + delta
        return current_time >= expiry_time


class UploadIndex(BaseModel):
    """Index of uploaded files with their metadata."""
    entries: Dict[str, IndexEntry] = {}

    def add_entry(self,
                  local_path: Path,
                  remote_path: str,
                  retention_policy: Dict[str, Any] | None = None) -> None:
        """
        Add a new entry to the index.

        Args:
            local_path: Local path of the uploaded file
            remote_path: Remote path on Nextcloud
            retention_policy: Retention policy for the file
        """
        key = f"{local_path}:{remote_path}"
        self.entries[key] = IndexEntry(
            local_path=local_path,
            remote_path=remote_path,
            upload_time=datetime.now(UTC),
            retention_policy=retention_policy
        )

    def has_entry(self, local_path: Path, remote_path: str) -> bool:
        """
        Check if a file is in the index.

        Args:
            local_path: Local path of the file
            remote_path: Remote path on Nextcloud

        Returns:
            bool: True if the file is in the index
        """
        key = f"{local_path}:{remote_path}"
        return key in self.entries

    def get_entry(self, local_path: Path, remote_path: str) -> IndexEntry | None:
        """
        Get entry from the index.

        Args:
            local_path: Local path of the file
            remote_path: Remote path on Nextcloud

        Returns:
            IndexEntry if found, None otherwise
        """
        key = f"{local_path}:{remote_path}"
        return self.entries.get(key)

    def remove_entry(self, local_path: Path, remote_path: str) -> None:
        """
        Remove an entry from the index.

        Args:
            local_path: Local path of the file
            remote_path: Remote path on Nextcloud
        """
        key = f"{local_path}:{remote_path}"
        if key in self.entries:
            del self.entries[key]

    def list_entries_to_delete(self) -> List[IndexEntry]:
        """
        List entries that should be deleted based on retention policy.

        Returns:
            List of entries to delete
        """
        entries_to_delete = []
        for entry in self.entries.values():
            if entry.should_delete():
                entries_to_delete.append(entry)
        return entries_to_delete


def load_index(index_path: Path) -> UploadIndex:
    """
    Load the upload index from a file.

    Args:
        index_path: Path to the index file

    Returns:
        UploadIndex object
    """
    if not index_path.exists():
        logger.info(f"Index file not found, creating new index: {index_path}")
        return UploadIndex()

    try:
        with open(index_path, "r") as f:
            data = json.load(f)
        return UploadIndex.model_validate(data)
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        logger.warning("Creating new index")
        return UploadIndex()


def save_index(index: UploadIndex, index_path: Path) -> None:
    """
    Save the upload index to a file.

    Args:
        index: UploadIndex object to save
        index_path: Path to save the index file
    """
    try:
        with open(index_path, "w") as f:
            json.dump(index.model_dump(), f, indent=2, default=str)
        logger.debug(f"Index saved to {index_path}")
    except Exception as e:
        logger.error(f"Error saving index: {e}")