#!/bin/bash

# Set script to exit on any error
set -e

# Change to the directory containing this script
cd "$(dirname "$0")"

echo "Updating main repository..."
git pull

echo "Updating submodules..."
git submodule update --init --recursive --remote

echo "All repositories have been updated successfully."