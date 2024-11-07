#!/bin/bash
cd "$(dirname "$0")" || exit 1
source venv/bin/activate
export PYTHONPATH=$(pwd)  # Ensure Python can find the project directory
python src/main.py
