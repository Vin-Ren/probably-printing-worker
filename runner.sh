#!/bin/bash
# Install dependencies and run the main script
sudo apt-get update -y
sudo apt-get install -y libcups2-dev libcairo2 pango1.0-tools libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fonts-dejavu cups cups-pdf python3-dev libcups2-dev build-essential

# Check whether is in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # Not in a virtual environment
    # Check for virtual env directory
    directories=("venv" ".venv" "env" ".env")
    for dir in "${directories[@]}"; do
        if [ -d "$dir" ]; then
            echo "Virtual environment found in $dir. Activating..."
            source "$dir/bin/activate"
            pip install -r requirements.txt
            echo "Running the main script..."
            echo "------------------------"
            python main.py "$@"
            exit 0
        fi
    done
    echo "Please activate a virtual environment before running this script."
    echo "Do you want to create and activate a new virtual environment now? (y/n)"
    read answer
    if [ "$answer" == "y" ]; then
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "Running the main script..."
        echo "------------------------"
        python main.py "$@"
    else
        echo "Exiting. Please activate a virtual environment and try again."
    exit 1
    fi
else
    python main.py "$@"
fi

