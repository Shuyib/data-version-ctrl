#!/bin/bash
# This script downloads the insurance dataset from kaggle
# change mirichoi0218/insurance to the dataset you want to download

# This command will exit the script if any command returns a non-zero exit code
set -euo pipefail

# check if kaggle and unzip are installed
for cmd in kaggle unzip; do
    if ! command -v $cmd &> /dev/null; then
        echo "$cmd could not be found"
        echo "Please install $cmd"
        exit
    fi
done

# Try downloading the dataset from kaggle
# Retry 5 times with a 15 second delay in case of failure 
# timeout will stop the download if it takes more than 60 seconds
# If the download fails, the script will exit
echo "Downloading dataset from kaggle"
echo "This may take a few minutes..."
echo "Link: https://www.kaggle.com/mirichoi0218/insurance"
for i in {1..5}; do
    timeout 60 kaggle datasets download -d mirichoi0218/insurance && break || sleep 15
done

# Check if the download was successful
if [ ! -f insurance.zip ]; then
    echo "Failed to download dataset"
    exit
fi

# Unzip the dataset
unzip -o insurance.zip

# Remove the zip file
rm insurance.zip

# Move the dataset to the data folder under original data
mkdir -p -v data/original_data
mv insurance.csv data/original_data/

# Print success message and list the files in the data folder
echo "Dataset downloaded successfully and moved to data folder"
ls data/original_data