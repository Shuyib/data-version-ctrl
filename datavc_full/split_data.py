"""
Creates the train and test data from the original data.

We also create a validation set from the training data. 

The data set will then be stored in data/train, data/test, and data/val.

How to run:
-----------
python split_data.py --data data/transform/insurance_000.parquet --strategy kfold --test_size 0.2 --n_splits 5
python split_data.py --data data/transform/insurance_000.parquet --strategy train_test_split --test_size 0.2

Or
make split_data if Makefile is available in your working directory.
"""

import os
import sys
import argparse
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

# package versions: python, pandas, sklearn
print("python:", sys.version)
print("pandas:", pd.__version__)
print("sklearn:", sklearn.__version__)


def main():
    """
    this function will split the data into train, test, and validation sets

    Parameters:
    -----------
    data: str
        Path to the input data file
    strategy: str
        Cross validation strategy
    test_size: float
        Test set size
    n_splits: int
        Number of folds for KFold
        Note: n_splits is only used when strategy is kfold

    Returns:
    --------
    None

    Example:
    --------
    python split_data.py --data data/transform/insurance_000.parquet --strategy kfold --test_size 0.2 --n_splits 5
    python split_data.py --data data/transform/insurance_000.parquet --strategy train_test_split --test_size 0.2
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Split data into train, test, and validation sets."
    )
    parser.add_argument(
        "--data", type=str, required=True, help="Path to the input data file"
    )
    parser.add_argument(
        "--strategy",
        choices=["train_test_split", "kfold"],
        default="train_test_split",
        help="Cross validation strategy",
    )
    parser.add_argument("--test_size", type=float, default=0.2, help="Test set size")
    parser.add_argument(
        "--n_splits", type=int, default=5, help="Number of folds for KFold"
    )
    args = parser.parse_args()

    # Load the cleaned data
    df3 = pd.read_parquet(args.data)

    # Define the independent and dependent variables
    X = df3.drop(columns=["charges"], axis=1)
    y = df3["charges"]

    # Define the output directory: train, test, and val
    output_dir = "data/transform/validation"
    os.makedirs(output_dir, exist_ok=True)

    if args.strategy == "train_test_split":
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=42
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=args.test_size, random_state=42
        )
    else:
        kf = KFold(n_splits=args.n_splits, random_state=42, shuffle=True)
        train_indices, test_indices = next(kf.split(X))
        X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
        y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=args.test_size, random_state=42
        )

    # Print the shapes of the data
    print("Train set shape:", X_train.shape)
    print("Test set shape:", X_test.shape)
    print("Validation set shape:", X_val.shape)

    # Save the dataframes in the output directory
    X_train.to_parquet(os.path.join(output_dir, "X_train.parquet"))
    y_train.to_frame().to_parquet(os.path.join(output_dir, "y_train.parquet"))
    X_test.to_parquet(os.path.join(output_dir, "X_test.parquet"))
    y_test.to_frame().to_parquet(os.path.join(output_dir, "y_test.parquet"))
    X_val.to_parquet(os.path.join(output_dir, "X_val.parquet"))
    y_val.to_frame().to_parquet(os.path.join(output_dir, "y_val.parquet"))


if __name__ == "__main__":
    main()
