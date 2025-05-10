# ncuploader/index.py
"""
Index for tracking uploaded files and their retention policies.
"""

import datetime
import json
from pathlib import Path
from typing import Dict, List, Any

from loguru import logger
from pydantic import BaseModel


class IndexEntry(BaseModel):
    """Entry in the upload index."""
    local_path: str
    remote_path: str
    upload_time: datetime.datetime
    retention_policy: Dict[str, Any] | None = None
    
    def should_delete(self) -> bool:
        """
        Check if file should be deleted based on retention policy.
        
        Returns:
            bool: True if the file should be deleted
        """
        if not self.retention_policy or "delete_after_upload" not in self.retention_policy:
            return False
            
        policy = self.retention_policy["delete_after_upload"]
        if not policy:
            return False
            
        unit = policy[-1]
        value = int(policy[:-1])
        
        now = datetime.datetime.now(tz=datetime.UTC)
        delta = now - self.upload_time
        
        if unit == 'd':
            return delta.days >= value
        elif unit == 'w':
            return delta.days >= value * 7
        elif unit == 'm':
            # Approximate months as 30 days
            return delta.days >= value * 30
        else:
            logger.warning(f"Unknown retention unit: {unit}")
            return False


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
            local_path=str(local_path),
            remote_path=remote_path,
            upload_time=datetime.datetime.now(tz=datetime.UTC),
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
        return [entry for entry in self.entries.values() if entry.should_delete()]


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