#!/bin/bash

# Find the file starting with 'shell'
file=$(find . -type f -name 'shell*' | head -n 1)

# Check if file was found
if [[ -z "$file" ]]; then
  echo "No file starting with 'shell' found."
  exit 1
fi

echo "Found file: $file"

# Run your Python program in the background
python your_python_script.py &
python_pid=$!

# Allow some time for the Python script to start and run
sleep 2

# Send SIGINT signal twice
kill -SIGINT $python_pid
sleep 1  # Wait a moment before sending the second SIGINT
kill -SIGINT $python_pid

# Optional: Wait for the Python program to end
# wait $python_pid

echo "SIGINT signals sent to the Python program."
