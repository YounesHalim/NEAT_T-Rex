#!/bin/bash

VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    if command -v python3 &>/dev/null; then
        PYTHON_CMD=python3
    elif command -v python &>/dev/null; then
        PYTHON_CMD=python
    else
        echo "Python is not installed. Please install Python to continue."
        exit 1
    fi
    $PYTHON_CMD -m venv $VENV_DIR
    source $VENV_DIR/bin/activate
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Please ensure it is present in the directory."
        exit 1
    fi
else
    echo "Virtual environment already exists. Skipping creation."
    source $VENV_DIR/bin/activate
fi

if [ -f "main.py" ]; then
    echo "Running main.py..."
    python main.py
else
    echo "main.py not found. Please ensure it is present in the directory."
    exit 1
fi
