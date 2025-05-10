#!/bin/bash

# e2e_run.sh
# Orchestrates the full end-to-end test: preparation, execution, and cleanup.

CONFIG_FILE_NAME="e2e_config.yaml"

# Ensure the script exits on error
set -e

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Navigate to the script's directory to ensure relative paths work
cd "$SCRIPT_DIR"

echo "Running e2e preparation script..."
if command -v python3 &> /dev/null; then
    python3 e2e_prep.py
elif command -v python &> /dev/null; then
    python e2e_prep.py
else
    echo "Error: python3 or python command not found. Please ensure Python is installed and in your PATH."
    exit 1
fi


echo "Running ncuploader (first run)..."
# Assuming ncuploader is in PATH or uv run can find it
# If ncuploader is installed in a venv and not globally, 
# you might need to activate the venv or use `uv run ncuploader`
if command -v ncuploader &> /dev/null; then
    ncuploader -c "${CONFIG_FILE_NAME}"
elif command -v uv &> /dev/null; then
    uv run ncuploader -c "${CONFIG_FILE_NAME}"
else
    echo "Error: ncuploader command not found. Please ensure it's installed and in your PATH or uv is available."
    exit 1
fi


echo "\nWaiting 2 seconds for short retention files to expire..."
time_start=$(date +%s)
sleep 2
time_end=$(date +%s)
echo "Slept for $((time_end - time_start)) seconds."

echo "\nRunning ncuploader (second run, verbose)..."
if command -v ncuploader &> /dev/null; then
    ncuploader -c "${CONFIG_FILE_NAME}" --verbose
elif command -v uv &> /dev/null; then
    uv run ncuploader -c "${CONFIG_FILE_NAME}" --verbose
else
    echo "Error: ncuploader command not found. Please ensure it's installed and in your PATH or uv is available."
    exit 1
fi

echo "\nNcuploader execution finished."

echo "\nRunning e2e cleanup script..."
if command -v python3 &> /dev/null; then
    python3 e2e_cleanup.py
elif command -v python &> /dev/null; then
    python e2e_cleanup.py
else
    echo "Error: python3 or python command not found. Please ensure Python is installed and in your PATH."
    exit 1
fi

echo "\nE2E test lifecycle finished."