#!/bin/bash

# Check if repos.txt exists
if [ ! -f "repos.txt" ]; then
    echo "Error: repos.txt not found in the current directory."
    exit 1
fi

# Read each line from repos.txt
while IFS= read -r repo_url; do
    # Skip empty lines
    if [ -z "$repo_url" ]; then
        continue
    fi

    # Extract the repository name from the URL
    repo_name=$(basename -s .git "$repo_url")

    # Check if the destination already exists
    if [ -d "$repo_name" ]; then
        echo "Warning: Destination already exists: $repo_name"
        continue
    fi

    # Clone the repository
    echo "Cloning $repo_name..."
    git clone "$repo_url"

    # Check if the clone was successful
    if [ $? -eq 0 ]; then
        echo "Successfully cloned $repo_name"
    else
        echo "Error: Failed to clone $repo_name"
    fi

done < repos.txt

echo "All repositories processed."