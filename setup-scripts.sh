#!/bin/bash

# Set script to exit on any error
set -e

# Change to the directory containing this script
cd "$(dirname "$0")"

# Create the GUIs/Active directory if it doesn't exist
mkdir -p GUIs/Active

# Read the repos from the file
REPOS_FILE="repos.txt"

# Check if the repos file exists
if [ ! -f "$REPOS_FILE" ]; then
    echo "Error: $REPOS_FILE not found in the current directory!"
    echo "Current directory: $(pwd)"
    echo "Contents of current directory:"
    ls -la
    exit 1
fi

# Clone or update each repository
while IFS= read -r repo
do
    # Skip empty lines and comments
    [[ "$repo" =~ ^[[:space:]]*$ || "$repo" =~ ^# ]] && continue

    # Extract the repo name from the URL
    repo_name=$(basename "$repo" .git)
    
    # Check if the repository already exists
    if [ -d "GUIs/Active/$repo_name" ]; then
        echo "Updating $repo_name..."
        cd "GUIs/Active/$repo_name"
        git pull
        cd ../../..
    else
        echo "Cloning $repo_name..."
        git clone "$repo" "GUIs/Active/$repo_name"
    fi
done < "$REPOS_FILE"

echo "All repositories have been cloned or updated successfully."