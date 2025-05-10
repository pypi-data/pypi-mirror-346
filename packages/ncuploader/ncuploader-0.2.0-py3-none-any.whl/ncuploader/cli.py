# ncuploader/cli.py
"""
Command-line interface for NCUploader.
"""

import typer
import sys
from pathlib import Path
from typing_extensions import Annotated

from loguru import logger

from . import __version__
from .config import load_config
from .uploader import NextcloudUploader

app = typer.Typer(help="NCUploader - Upload files to Nextcloud with retention policies", add_help_option=True, context_settings={"help_option_names": ["--help", "-h"]})


def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity level."""
    # Remove default handler
    logger.remove()

    # Add console handler with appropriate level
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level)


@app.command()
def main(
    config_path: Annotated[Path, typer.Option("-c", "--config", help="Path to configuration file", exists=True, file_okay=True, dir_okay=False, readable=True, resolve_path=True)] = Path("ncuploader.yaml"),
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="Enable verbose output")] = False,
    version: Annotated[bool, typer.Option("--version", help="Show application version and exit", callback=lambda value: version_callback(value, __version__), is_eager=True)] = False,
    dry_run: Annotated[bool, typer.Option("-n", "--dry-run", help="Run in dry-run mode (no actual uploads or deletions)")] = False
):
    """NCUploader - Upload files to Nextcloud with retention policies"""
    setup_logging(verbose)

    try:
        # Load configuration
        logger.info(f"Loading configuration from: {config_path}")
        config_obj = load_config(config_path)
        config_obj.dry_run = dry_run # Pass dry_run to config or uploader

        # Create uploader
        uploader = NextcloudUploader(config_obj)

        # Process uploads
        success_count, fail_count = uploader.process_uploads()

        # Summary
        logger.info(f"Upload process completed! Success: {success_count}, Failed: {fail_count}")

        # Return appropriate exit code
        if fail_count > 0:
            raise typer.Exit(code=1)

    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        raise typer.Exit(code=1)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        if verbose:
            logger.exception("Detailed error information:")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if verbose:
            logger.exception("Detailed error information:")
        raise typer.Exit(code=1)

def version_callback(value: bool, version_str: str):
    if value:
        print(f"NCUploader {version_str}")
        raise typer.Exit()

if __name__ == "__main__":
    app()
else:
    # This allows the CLI to be invoked via entry points
    # and ensures --help works properly
    def main():
        app()