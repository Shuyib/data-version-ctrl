"""Hyperparameter tuning for DecisionTreeRegressor and PolynomialFeatures + LinearRegression."""

import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split


def tune_decision_tree(
    X_train: pd.DataFrame, y_train: pd.Series, param_grid: dict
) -> GridSearchCV:
    """Tune DecisionTreeRegressor using GridSearchCV.

    Parameters:
    -----------
    X_train: pd.DataFrame

    y_train: pd.Series

    param_grid: dict

    Returns:
    --------
    GridSearchCV

    """
    model = DecisionTreeRegressor()
    grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    print("====================Best Decision Tree Hyperparameters==================")
    print(json.dumps(best_params, indent=2))
    print("===========================================================================")

    with open("model_output/rfc_best_params_decision_tree.json", "w") as outfile:
        json.dump(best_params, outfile)

    return grid_search


def tune_polynomial_linear_regression(
    X_train: pd.DataFrame, y_train: pd.Series, param_grid: dict
) -> GridSearchCV:
    """Tune PolynomialFeatures and LinearRegression using GridSearchCV.

    Parameters:
    -----------
    X_train: pd.DataFrame

    y_train: pd.Series

    param_grid: dict

    Returns:
    --------
    GridSearchCV
    """
    # Create pipeline with both transformers
    pipeline = Pipeline(
        [("poly", PolynomialFeatures()), ("linear", LinearRegression())]
    )

    # Adjust parameter grid to use poly__ prefix
    poly_param_grid = {f"poly__{key}": value for key, value in param_grid.items()}

    # Perform grid search
    grid_search = GridSearchCV(
        pipeline,
        poly_param_grid,
        cv=5,
        n_jobs=-1,
        verbose=2,
        scoring="neg_mean_squared_error",
    )
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

    print(
        "====================Best Polynomial Linear Regression Hyperparameters=================="
    )
    print(json.dumps(best_params, indent=2))
    print(
        "==========================================================================================="
    )

    # Save best parameters
    with open("model_output/hp_best_params_poly_linear.json", "w") as outfile:
        json.dump(best_params, outfile)

    return grid_search


def get_hp_tuning_results(grid_search: GridSearchCV, model_name: str = "") -> str:
    """Get the results of hyperparameter tuning in a Markdown table with regression metrics

    Parameters:
    -----------
    grid_search: GridSearchCV

    model_name: str

    Returns:
    --------
    str

    """
    # Get CV results
    cv_results = pd.DataFrame(grid_search.cv_results_)
    params_df = pd.json_normalize(cv_results["params"])

    # Calculate regression metrics
    mean_mse = -cv_results["mean_test_score"]  # Convert negative MSE back
    std_mse = cv_results["std_test_score"]
    mean_rmse = np.sqrt(mean_mse)

    # Create results DataFrame
    results = pd.DataFrame(
        {
            "Rank": cv_results["rank_test_score"],
            "Mean MSE": mean_mse.round(4),
            "Std MSE": std_mse.round(4),
            "Mean RMSE": mean_rmse.round(4),
            **params_df,
        }
    )

    # Sort and format
    results.sort_values("Mean MSE", ascending=True, inplace=True)

    # Generate markdown output only the results
    markdown = results.to_markdown(index=False)
    
    return markdown


def main():
    # Load the data
    X_train = pd.read_parquet("data/transform/validation/X_train.parquet")
    X_test = pd.read_parquet("data/transform/validation/X_test.parquet")
    y_train = pd.read_parquet("data/transform/validation/y_train.parquet")
    y_test = pd.read_parquet("data/transform/validation/y_test.parquet")
    X_val = pd.read_parquet("data/transform/validation/X_val.parquet")
    y_val = pd.read_parquet("data/transform/validation/y_val.parquet")

    # Load hyperparameter configurations
    with open("hp_config.json", "r") as config_file:
        hp_config = json.load(config_file)

    # Hyperparameter tuning for DecisionTreeRegressor
    print("Starting hyperparameter tuning for DecisionTreeRegressor...")
    dt_param_grid = hp_config.get("DecisionTreeRegressor", {})
    dt_grid_search = tune_decision_tree(X_train, y_train, dt_param_grid)

    # Hyperparameter tuning for PolynomialFeatures + LinearRegression
    print("Starting hyperparameter tuning for PolynomialFeatures + LinearRegression...")
    poly_param_grid = hp_config.get("PolynomialFeatures", {})
    poly_grid_search = tune_polynomial_linear_regression(
        X_train, y_train, poly_param_grid
    )

    # Save tuning results as markdown
    dt_markdown = get_hp_tuning_results(
        dt_grid_search, model_name="DecisionTreeRegressor"
    )
    with open("model_output/hp_tuning_results_decision_tree.md", "w") as dt_md_file:
        dt_md_file.write(dt_markdown)

    poly_markdown = get_hp_tuning_results(
        poly_grid_search, model_name="PolynomialFeatures + LinearRegression"
    )
    with open("model_output/hp_tuning_results_poly_linear.md", "w") as poly_md_file:
        poly_md_file.write(poly_markdown)

    # Save the best hyperparameters for DecisionTreeRegressor and PolynomialFeatures + LinearRegression
    dt_best_params = dt_grid_search.best_params_
    poly_best_params = poly_grid_search.best_params_

    # save the best hyperparameters to a JSON file
    # that can be used for model evaluation with scikit-learn models
    with open(
        "model_output/best_params_decision_tree.json", "w"
    ) as dt_best_params_file:
        json.dump(dt_best_params, dt_best_params_file)

    with open(
        "model_output/best_params_poly_linear.json", "w"
    ) as poly_best_params_file:
        json.dump(poly_best_params, poly_best_params_file)


if __name__ == "__main__":
    main()
