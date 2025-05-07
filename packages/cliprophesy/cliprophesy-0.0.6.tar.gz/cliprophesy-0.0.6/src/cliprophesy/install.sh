#!/usr/bin/env bash

set -euo pipefail  # safer bash settings

# --- Check for Python 3 ---
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required but not found. Aborting."
    exit 1
fi

# --- Setup temporary venv ---
VENV_DIR=".cliprophesy_build_env"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# --- Install requirements ---
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found, proceeding anyway..."
fi

# --- Install pyinstaller and build ---
pip install pyinstaller
pyinstaller --onefile cliprophesy.py

# --- Find a good install location ---
OS_TYPE="$(uname)"
PREFERRED_DIRS=()

if [ "$OS_TYPE" = "Darwin" ]; then
    PREFERRED_DIRS=(
        "/usr/local/bin"
        "/opt/homebrew/bin"  # for M1/M2 Macs
        "/usr/bin"
        "$HOME/.local/bin"
    )
else
    PREFERRED_DIRS=(
        "/usr/local/bin"
        "/usr/bin"
        "$HOME/.local/bin"
    )
fi

TARGET_DIR=""

# Try preferred dirs first
for dir in "${PREFERRED_DIRS[@]}"; do
    if [ -d "$dir" ] && [ -w "$dir" ]; then
        TARGET_DIR="$dir"
        break
    fi
done

# If none of the preferred ones are writable, fallback to any writable dir in PATH
if [ -z "$TARGET_DIR" ]; then
    IFS=':' read -r -a path_dirs <<< "$PATH"
    for dir in "${path_dirs[@]}"; do
        if [ -d "$dir" ] && [ -w "$dir" ]; then
            TARGET_DIR="$dir"
            break
        fi
    done
fi

# Last chance: try to create ~/.local/bin if it doesn't exist
if [ -z "$TARGET_DIR" ]; then
    mkdir -p "$HOME/.local/bin"
    if [ -w "$HOME/.local/bin" ]; then
        TARGET_DIR="$HOME/.local/bin"
    fi
fi

# If still no target, fail
if [ -z "$TARGET_DIR" ]; then
    echo "Error: No writable directory found in PATH. Aborting."
    deactivate
    rm -rf "$VENV_DIR"
    exit 1
fi

# --- Move the built binary ---
BUILT_FILE="dist/cliprophesy"
if [ ! -f "$BUILT_FILE" ]; then
    echo "Error: Build failed. $BUILT_FILE not found."
    deactivate
    rm -rf "$VENV_DIR"
    exit 1
fi

chmod +x "$BUILT_FILE"
mv "$BUILT_FILE" "$TARGET_DIR/cliprophesy"

echo "✅ cliprophesy installed to $TARGET_DIR/cliprophesy"

# --- Clean up ---
deactivate
rm -rf "$VENV_DIR"
rm -rf build dist __pycache__ cliprophesy.spec

echo "✅ Installation complete."
