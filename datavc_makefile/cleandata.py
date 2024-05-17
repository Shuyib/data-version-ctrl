"""This module contains functions to clean the data.

It includes data loading, data cleaning, and data saving functions.


Functions:
----------
load_data: Load the data from the file path.
summary: Return the summary of the data.
check_missing: Return the missing values in the data.
encode_data: Encode the data.

These functions will be run as a command line tool using argparse.

How to run the script:
----------------------
python cleandata.py load_data --file_path data/original_data/insurance.csv
python cleandata.py summary --file_path data/original_data/insurance.csv
python cleandata.py check_missing --file_path data/original_data/insurance.csv
python cleandata.py check_duplicate --file_path data/original_data/insurance.csv
python cleandata.py encode_data --file_path data/original_data/insurance.csv

Or
make clean_data if Makefile is available in your working directory."""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import LabelEncoder


# print versions of python, pandas, numpy and sklearn
print("Let's check the versions of the libraries used in this script.")
print(f"python version: {sys.version}")
print(f"pandas version: {pd.__version__}")
print(f"numpy version: {np.__version__}")
print(f"sklearn version: {sklearn.__version__}")

# Define the data types for the columns
# Saves pandas from guessing the data types and using more memory
dtypes = {
    "age": np.int16,  # int8 is not enough to store the age
    "sex": "category",  # category is used for columns with few unique values
    "bmi": np.float32,
    "children": np.int16,
    "smoker": "category",
    "region": "category",
    "charges": np.float32,
}


def load_data(file_path: str) -> pd.DataFrame:
    """Load the data from the file path.

    Parameters
    ----------
    file_path: str :
        The path to the data file.
        To get more stable results use the absolute path.
        Or pathlib can be used to convert the relative path to absolute path.


    Returns
    -------
    pd.DataFrame
        The data loaded from the file path.

    Examples
    --------
    >>> load_data("data/insurance.csv")

    """
    print(f"Loading data from {file_path}")
    return pd.read_csv(file_path, dtype=dtypes)


def summary(data: pd.DataFrame) -> pd.DataFrame:
    """Concise summary of the data.
    Packed with metric like count, mean, std, min, max
    of each column.

    Parameters
    ----------
    data: pd.DataFrame :
        The data to summarize.


    Returns
    -------
    type
        The summary of the data.

    Examples
    --------
    >>> summary(data)
    """
    print("Generating summary of the data")
    return data.describe(include="all")


def check_missing(data: pd.DataFrame) -> pd.DataFrame:
    """Check for missing values in the data.

    Parameters
    ----------
    data: pd.DataFrame :
        The data to check for missing values.

    Returns
    -------
    type
        The missing values in the data.

    Examples
    --------
    >>> check_missing(data)

    """
    print("Checking for missing values in the data")
    return data.isnull().sum()


def check_duplicate(data: pd.DataFrame) -> pd.DataFrame:
    """Check for duplicate values in the data.

    Parameters
    ----------
    data: pd.DataFrame :
        The data to check for duplicate values.

    Returns
    -------
    type
        The duplicate values in the data.

    Examples
    --------
    >>> check_duplicate(data)

    """
    print("Checking for duplicate values in the data")
    return data.duplicated().sum()


def encode_data(data: pd.DataFrame, version) -> pd.DataFrame:
    """Encode the data.
    That is, convert the categorical data to numerical data.

    Parameters
    ----------
    data: pd.DataFrame :
        The data to encode.

    version: str :
        The version of the data to save.

    Returns
    -------
    type
        The encoded data. pd.DataFrame if the data is not saved to a file.
        parquet file if the data is saved to a file.

    Examples
    --------
    >>> encode_data(data)

    """
    label_encoder = LabelEncoder()
    data["sex"] = label_encoder.fit_transform(data["sex"])
    data["smoker"] = label_encoder.fit_transform(data["smoker"])
    data["region"] = label_encoder.fit_transform(data["region"])
    # make a transform directory if it does not exist
    if not os.path.exists("data/transform"):
        os.makedirs("data/transform")
    print("label encoding sex, smoker, and region columns")
    data.to_parquet(f"data/transform/insurance_{version}.parquet")  # more efficient
    # data.to_pickle(f"data/transform/insurance_{version}.pkl") # less efficient
    # data.to_csv(f"data/transform/insurance_{version}.csv") # less efficient
    return data.transpose()


def main():
    """Convert this to a command line tool with argparse.
    This function is the entry point for the command line tool.
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Perform data loading, data cleaning, and data saving."
    )
    # Add the arguments: command and file_path
    parser.add_argument(
        "command",
        choices=[
            "load_data",
            "summary",
            "check_missing",
            "check_duplicate",
            "encode_data",
        ],
    )
    parser.add_argument("--file_path", help="The path to the data file")
    parser.add_argument("--version", help="The version of the data to save")

    # Parse the arguments:
    args = parser.parse_args()

    # Check the command and call the appropriate function
    if args.command == "load_data":
        print(load_data(args.file_path))
    elif args.command == "summary":
        data = load_data(args.file_path)
        print(summary(data))
    elif args.command == "check_missing":
        data = load_data(args.file_path)
        print(check_missing(data))
    elif args.command == "encode_data":
        data = load_data(args.file_path)
        print(encode_data(data, args.version))
    elif args.command == "check_duplicate":
        data = load_data(args.file_path)
        print(check_duplicate(data))


if __name__ == "__main__":
    main()
