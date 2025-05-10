# ncuploader/__init__.py
"""
NCUploader: Upload files to Nextcloud with retention policies.
"""

__version__ = "0.1.0"

# Public API
from .uploader import NextcloudUploader
from .retention import RetentionPolicy
from .config import load_config, Config # Added Config here
from .index import UploadIndex, IndexEntry, load_index, save_index


__all__ = [
    "NextcloudUploader",
    "RetentionPolicy",
    "Config",  # Assuming Config will be exposed
    "load_config",
    "UploadIndex",
    "IndexEntry",
    "load_index",
    "save_index"
]