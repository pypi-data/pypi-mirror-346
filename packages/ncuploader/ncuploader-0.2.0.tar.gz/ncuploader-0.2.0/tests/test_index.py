# tests/test_index.py
import datetime
from pathlib import Path
import tempfile
from datetime import UTC, timezone # Python 3.11+ native import for UTC

from ncuploader.index import UploadIndex, IndexEntry, load_index, save_index

# This global entry instantiation seems problematic for tests and might not be needed.
# If it's for a specific default or example, it should be clearly defined or scoped.
# For now, I'll correct its usage of datetime, assuming it's intended.
# However, test-specific data should ideally be created within test functions.
entry_example_for_global_scope_if_needed = IndexEntry(
    local_path=Path("/example/local"), # Added to satisfy IndexEntry requirements
    remote_path="/example/remote",    # Added to satisfy IndexEntry requirements
    upload_time=datetime.datetime.now(UTC) # Corrected usage
)


def test_add_entry():
    """Test adding entries to the index."""
    index = UploadIndex()

    # Add an entry
    index.add_entry(
        local_path=Path("/test/local"),
        remote_path="/test/remote",
        retention_policy={"delete_after_upload": "30d"}
    )

    # Verify entry was added
    assert index.has_entry(Path("/test/local"), "/test/remote")

    # Verify entry data
    entry = index.get_entry(Path("/test/local"), "/test/remote")
    assert entry is not None
    assert entry.local_path == Path("/test/local")
    assert entry.remote_path == "/test/remote"
    assert entry.retention_policy == {"delete_after_upload": "30d"}


def test_remove_entry():
    """Test removing entries from the index."""
    index = UploadIndex()

    # Add an entry
    index.add_entry(
        local_path=Path("/test/local"),
        remote_path="/test/remote"
    )

    # Verify entry was added
    assert index.has_entry(Path("/test/local"), "/test/remote")

    # Remove the entry
    index.remove_entry(Path("/test/local"), "/test/remote")

    # Verify entry was removed
    assert not index.has_entry(Path("/test/local"), "/test/remote")


def test_retention_policy_days():
    """Test retention policy checking for days."""
    # Create entry with upload time 31 days ago
    thirty_one_days_ago = datetime.datetime.now(UTC) - datetime.timedelta(days=31)
    entry = IndexEntry(
        local_path=Path("/test/local"),
        remote_path="/test/remote",
        upload_time=thirty_one_days_ago,
        retention_policy={"delete_after_upload": "30d"}
    )

    # Should be deleted
    assert entry.should_delete()

    # Create entry with upload time 29 days ago
    twenty_nine_days_ago = datetime.datetime.now(UTC) - datetime.timedelta(days=29)
    entry = IndexEntry(
        local_path=Path("/test/local"),
        remote_path="/test/remote",
        upload_time=twenty_nine_days_ago,
        retention_policy={"delete_after_upload": "30d"}
    )

    # Should not be deleted
    assert not entry.should_delete()


def test_save_load_index():
    """Test saving and loading the index."""
    with tempfile.NamedTemporaryFile() as tmp:
        # Create index
        index = UploadIndex()
        index.add_entry(
            local_path=Path("/test/local1"),
            remote_path="/test/remote1"
        )
        index.add_entry(
            local_path=Path("/test/local2"),
            remote_path="/test/remote2",
            retention_policy={"delete_after_upload": "30d"}
        )

        # Save index
        save_index(index, Path(tmp.name))

        # Load index
        loaded_index = load_index(Path(tmp.name))

        # Verify entries
        assert loaded_index.has_entry(Path("/test/local1"), "/test/remote1")
        assert loaded_index.has_entry(Path("/test/local2"), "/test/remote2")

        entry = loaded_index.get_entry(Path("/test/local2"), "/test/remote2")
        assert entry is not None
        assert entry.retention_policy == {"delete_after_upload": "30d"}