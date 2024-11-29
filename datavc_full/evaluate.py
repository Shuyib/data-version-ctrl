"""
Here we will reload the datasets created in the previous step 
and evaluate the model.

We will perform the following steps:
- Load the datasets
- Instantiate several models with optimized hyperparameters
- Train the models
- Evaluate the models using the test set
- Visualize feature importance and decision boundaries
- Narrative on the findings
- Save the models

How to run:
-----------
python evaluate.py

Or
make evaluate_model if Makefile is available in your working directory.

Things to try:
--------------
- Use different metrics to evaluate the models.
- Review the conditions to do multiple linear regression. Have we met them?
- Try using RobustScaler to scale the data. They are less prone to outliers.
- Try different hyperparameters for the models. Especially for the decision tree model.
- Try different models and compare the results using dvc.
"""

import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import joblib
import mlem
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn import tree
from joblib import dump
from mlem.api import save


# Display library versions
print(f"python version: {sys.version}")
print(f"numpy version: {np.__version__}")
print(f"pandas version: {pd.__version__}")
print(f"seaborn version: {sns.__version__}")
print(f"matplotlib version: {plt.matplotlib.__version__}")
print(f"sklearn version: {sklearn.__version__}")
print(f"joblib version: {joblib.__version__}")
print(f"mlem version: {mlem.__version__}")

# Load the best hyperparameters for DecisionTreeRegressor
with open("model_output/rfc_best_params_decision_tree.json", "r") as dt_file:
    dt_params = json.load(dt_file)

# Load the best hyperparameters for PolynomialFeatures + LinearRegression
with open("model_output/hp_best_params_poly_linear.json", "r") as poly_file:
    poly_linear_params = json.load(poly_file)

# Parse hyperparameters
dt_criterion = dt_params.get("criterion", "absolute_error")
dt_min_samples_leaf = dt_params.get("min_samples_leaf", 25)
dt_max_leaf_nodes = dt_params.get("max_leaf_nodes", 4)
dt_random_state = dt_params.get("random_state", 1993)

poly_degree = poly_linear_params.get("poly__degree", 2)
poly_interaction_only = poly_linear_params.get("poly__interaction_only", False)

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

# Instantiate and train the DecisionTreeRegressor with best hyperparameters
tree_model = DecisionTreeRegressor(
    criterion=dt_criterion,
    min_samples_leaf=dt_min_samples_leaf,
    max_leaf_nodes=dt_max_leaf_nodes,
    random_state=dt_random_state,
).fit(X_train, y_train)

# Instantiate and train the PolynomialFeatures + LinearRegression with best hyperparameters
poly = PolynomialFeatures(degree=poly_degree, interaction_only=poly_interaction_only)
X_train_poly = poly.fit_transform(X_train)
X_val_poly = poly.transform(X_val)
linear_model_poly = LinearRegression().fit(X_train_poly, y_train)

# Fit the linear model with the normalized data
linear_model_scaled = LinearRegression().fit(X_train_scaled, y_train)

# Predict the charges
y_pred_linear_test = linear_model_scaled.predict(scaler.transform(X_test))
y_pred_tree_test = tree_model.predict(X_test)
y_pred_poly_test = linear_model_poly.predict(poly.transform(X_test))

# Scoring the models with appropriate metrics
print("\nEvaluating the models with the test and validation sets")
print("Linear model MAE:", mean_absolute_error(y_test, y_pred_linear_test))
print("Tree model R² score:", tree_model.score(X_test, y_test))
print(
    "Linear model R² score on validation set:",
    linear_model_scaled.score(X_val_scaled, y_val),
)
print("Tree model R² score on validation set:", tree_model.score(X_val, y_val))
print(
    "Polynomial Linear Regression R² score on validation set:",
    linear_model_poly.score(X_val_poly, y_val),
)

# Store the metrics in a dictionary
metrics = {
    "linear_model_mae": mean_absolute_error(y_test, y_pred_linear_test),
    "tree_model_score": tree_model.score(X_test, y_test),
    "linear_model_score_val": linear_model_scaled.score(X_val_scaled, y_val),
    "tree_model_score_val": tree_model.score(X_val, y_val),
    "linear_model_score_poly_val": linear_model_poly.score(X_val_poly, y_val),
}

# Write the metrics to a JSON file
with open("metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

# Show a small sample of the predictions and actual values
print("\nSample of the predictions and actual values for the linear model")
print(
    pd.DataFrame(
        {"Prediction": np.ravel(y_pred_linear_test), "Actual": np.ravel(y_test)}
    ).head(5)
)

print("\nSample of the predictions and actual values for the tree model")
print(
    pd.DataFrame(
        {"Prediction": np.ravel(y_pred_tree_test), "Actual": np.ravel(y_test)}
    ).head(5)
)

print("\nSample of the predictions and actual values for the polynomial linear model")
print(
    pd.DataFrame(
        {"Prediction": np.ravel(y_pred_poly_test), "Actual": np.ravel(y_test)}
    ).head(5)
)

# Store the datasets for the predictions as markdown
df_linear = pd.DataFrame(
    {"Prediction": np.ravel(y_pred_linear_test), "Actual": np.ravel(y_test)}
)
with open("model_output/predictions_linear_model.md", "w") as f:
    f.write(df_linear.to_markdown(index=False))

df_tree = pd.DataFrame(
    {"Prediction": np.ravel(y_pred_tree_test), "Actual": np.ravel(y_test)}
)
with open("model_output/predictions_tree_model.md", "w") as f:
    f.write(df_tree.to_markdown(index=False))

df_poly_linear = pd.DataFrame(
    {"Prediction": np.ravel(y_pred_poly_test), "Actual": np.ravel(y_test)}
)
with open("model_output/predictions_poly_linear_model.md", "w") as f:
    f.write(df_poly_linear.to_markdown(index=False))

# Residual plot for tree model
plt.figure(figsize=(12, 8))
sns.residplot(x=y_pred_tree_test, y=y_test, lowess=True)
plt.title("Residual Plot for Tree Model")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.tight_layout()
plt.savefig("model_output/residual_plot_tree_model.png")

# Residual plot for linear model
plt.figure(figsize=(12, 8))
sns.residplot(x=y_pred_linear_test, y=y_test, lowess=True)
plt.title("Residual Plot for Linear Model")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.tight_layout()
plt.savefig("model_output/residual_plot_linear_model.png")

# Residual plot for polynomial linear model
plt.figure(figsize=(12, 8))
sns.residplot(x=y_pred_poly_test, y=y_test, lowess=True)
plt.title("Residual Plot for Polynomial Linear Model")
plt.xlabel("Predicted Values")
plt.ylabel("Residuals")
plt.tight_layout()
plt.savefig("model_output/residual_plot_poly_linear_model.png")

# Draw the decision tree and save the image
plt.figure(figsize=(20, 10))
tree.plot_tree(tree_model, feature_names=X_train.columns, filled=True, fontsize=10)
plt.title("Decision Tree")
plt.tight_layout()
plt.savefig("model_output/decision_tree.png")

# Visualize the feature importance
plt.figure(figsize=(12, 8))
importance = pd.Series(tree_model.feature_importances_, index=X_train.columns)
importance.nlargest(10).plot(kind="barh")
plt.title("Feature Importance for Decision Tree")
plt.tight_layout()
plt.savefig("model_output/feature_importance_tree.png")

# Save the models using MLEM
save(linear_model_scaled, 'model/linear_model_scaled.mlem')
save(tree_model, 'model/tree_model.mlem')
save(linear_model_poly, 'model/polynomial_linear_model.mlem')

# Narrative on the findings
# to be added
