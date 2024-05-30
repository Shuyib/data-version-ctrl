"""
Here we will reload the datasets created in the previous step 
and evaluate the model.

We will perform the following steps:
- Load the datasets
- Instantiate several models
- Train the models
- Evaluate the models using the test set
- Visualize feature importance and decision boundaries
- Narrative on the findings
- Save the models

How to run:
-----------
python evaluate.py --criterion mse --min_samples_leaf 25 --max_leaf_nodes 4 --degree 2

Or
make evaluate_model if Makefile is available in your working directory.

Things to try:
--------------
- Use different metrics to evaluate the models.
- Try using RobustScaler to scale the data. They are less prone to outliers.
- Try different hyperparameters for the models. Especially for the decision tree model.
- Try different models and compare the results using dvc.
"""

import sys
import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error
from sklearn import tree
from sklearn.preprocessing import StandardScaler
import joblib
from joblib import dump


# see versions of libraries
print(f"python version: {sys.version}")
print(f"numpy version: {np.__version__}")
print(f"pandas version: {pd.__version__}")
print(f"seaborn version: {sns.__version__}")
print(f"matplotlib version: {plt.matplotlib.__version__}")
print(f"sklearn version: {sklearn.__version__}")
print(f"joblib version: {joblib.__version__}")

# Create the parser
parser = argparse.ArgumentParser(description="Train and evaluate regression models")

# Add the arguments
parser.add_argument(
    "--criterion",
    type=str,
    default="absolute_error",
    help="The function to measure the quality of a split for the decision tree",
)  # noqa C0301
parser.add_argument(
    "--min_samples_leaf",
    type=int,
    default=25,
    help="The minimum number of samples required to be at a leaf node for the decision tree",
)
parser.add_argument(
    "--max_leaf_nodes",
    type=int,
    default=4,
    help="Grow a tree with max_leaf_nodes in best-first fashion for the decision tree",
)
parser.add_argument(
    "--degree", type=int, default=2, help="The degree of the polynomial features"
)

# Parse the arguments
args = parser.parse_args()

# Load the data
X_train = pd.read_parquet("data/transform/validation/X_train.parquet")
X_test = pd.read_parquet("data/transform/validation/X_test.parquet")
y_train = pd.read_parquet("data/transform/validation/y_train.parquet")
y_test = pd.read_parquet("data/transform/validation/y_test.parquet")
X_val = pd.read_parquet("data/transform/validation/X_val.parquet")
y_val = pd.read_parquet("data/transform/validation/y_val.parquet")

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)


# Use the arguments in the models
tree_model = DecisionTreeRegressor(
    criterion=args.criterion,
    min_samples_leaf=args.min_samples_leaf,
    max_leaf_nodes=args.max_leaf_nodes,
).fit(X_train, y_train)
poly = PolynomialFeatures(degree=args.degree)

# score the polynomial features
X_train_poly = poly.fit_transform(X_train)
X_val_poly = poly.fit_transform(X_val)
linear_model_poly = LinearRegression().fit(X_train_poly, y_train)

# Fit the linear model with the normalized data
linear_model_scaled = LinearRegression().fit(X_train_scaled, y_train)

# Predict the charges
y_pred_linear_test = linear_model_scaled.predict(scaler.transform(X_test))
y_pred_tree_test = tree_model.predict(X_test)

# Scoring the models with .score
# the score is the R^2 value
print("\nEvaluating the models with the test, and validation set")
# use mae as the scoring metric for linear model
print("Linear model score:", mean_absolute_error(y_test, y_pred_linear_test))
print("Tree model score:", tree_model.score(X_test, y_test))
print(
    "Linear model score on validation set:",
    linear_model_scaled.score(X_val_scaled, y_val),
)
print("Tree model score on validation set:", tree_model.score(X_val, y_val))
print(
    "Linear model score with polynomial features on validation set:",
    linear_model_poly.score(X_val_poly, y_val),
)

# store the metrics in a dictionary
metrics = {
    "linear_model_mae": mean_absolute_error(y_test, y_pred_linear_test),
    "tree_model_score": tree_model.score(X_test, y_test),
    "linear_model_score_val": linear_model_scaled.score(X_val_scaled, y_val),
    "tree_model_score_val": tree_model.score(X_val, y_val),
    "linear_model_score_poly_val": linear_model_poly.score(X_val_poly, y_val),
}

# write the metrics to a JSON file
with open("model_output/metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f)


# Draw the decision tree
plt.figure(figsize=(12, 8))
tree.plot_tree(tree_model, feature_names=X_train.columns, filled=True)


# Save the models: linear_model_scaled and tree_model
dump(linear_model_scaled, "model_output/linear_model_scaled.joblib")
dump(tree_model, "model_output/tree_model.joblib")
plt.savefig("output/decision_tree.png")

# Narrative on the findings
# to be added
