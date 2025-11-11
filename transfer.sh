#!/bin/bash

# If on Windows, run from Git Bash
# Usage: <path_to_this_file> <path_to_pico_root>
# Example: ./transfer.sh D:

PROJECT_DIR="./src/pico"

# Check if destination directory parameter was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <destination_directory>"
    exit 1
fi

DEST_DIR="$1"

# Check if destination directory exists
if [ ! -d "$DEST_DIR" ]; then
    echo "Error: Destination directory '$DEST_DIR' does not exist."
    exit 1
fi

# Transfer files (preserving directory structure)
echo "Transferring files from $PROJECT_DIR to $DEST_DIR..."
cp -r "$PROJECT_DIR"/* "$DEST_DIR"/

# Check if transfer was successful
if [ $? -eq 0 ]; then
    echo "Transfer complete! All files copied to $DEST_DIR"
else
    echo "Error: Transfer failed."
    exit 1
fi