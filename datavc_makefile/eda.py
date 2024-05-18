"""
In this file, we will write the code to perform exploratory data analysis on the dataset.

We will perform the following steps:
- Make a correlation matrix and visualize it in a heatmap
- Investigative plots on variables
- Graphical statistical modeling for the next steps
- Narrative on the findings

How to run the script:
----------------------
python eda.py --input data/transform/insurance_000.parquet --output output/eda_combined_plots.png

Or
make eda if Makefile is available in your working directory.

"""

import argparse
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# see versions of libraries
print(f"pandas version: {pd.__version__}")
print(f"numpy version: {np.__version__}")
print(f"matplotlib version: {plt.matplotlib.__version__}")
print(f"seaborn version: {sns.__version__}")


# use ggplot style for the plots
plt.style.use("ggplot")


# Define a function to combine the plots into one figure
def combine_plots() -> None:
    """
    This function combines the following plots into one figure:
    1. Correlation Matrix Heatmap
    2. Distribution of Charges for Smokers and Non-Smokers
    3. Number of Smokers and Non-Smokers

    Parameters:
    ----------
    None

    Returns:
    -------
    None

    Example:
    --------
    combine_plots()
    """
    # load the parquet file
    file_path = "data/transform/insurance_000.parquet"
    df2 = pd.read_parquet(file_path)

    # confirm if it was successfully loaded
    print("First 5 rows of the dataframe:")
    print(df2.head())
    print("\n \n")
    print("Last 5 rows of the dataframe:")
    print(df2.tail())
    print("\n \n")
    # check the shape of the dataframe
    print("Shape of the dataframe:")
    print(df2.shape)
    print("\n \n")
    # check the data types of the columns
    print("Data types of the columns:")
    print(df2.dtypes)
    print("\n \n")

    # Calculate the correlation matrix
    corr = df2.corr()

    # Create the subplots
    _, axes = plt.subplots(3, 2, figsize=(15, 18))

    # Plot 1: Correlation Matrix Heatmap
    ax1 = axes[0, 0]
    sns.heatmap(
        corr,
        mask=np.zeros_like(corr, dtype=np.bool_),
        cmap="coolwarm",
        square=True,
        annot=True,
        fmt=".2f",
        ax=ax1,
    )
    ax1.set_title("Correlation Matrix Heatmap of insurance dataset")
    ax1.text(
        0.4,
        -0.1,
        "Expecting high correlation between bmi and charges\n \
        but smoking and charges were more correlated",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax1.transAxes,
        fontsize=8,
    )

    # Plot 2: Distribution of Charges for Smokers and Non-Smokers
    ax2 = axes[0, 1]
    sns.boxplot(
        y="smoker",
        x="charges",
        data=df2.replace({"smoker": {1: "smoker", 0: "non-smoker"}}),
        ax=ax2,
        orient="h",
    )
    ax2.set_title("Distribution of Charges for Smokers and Non-Smokers")
    ax2.text(
        0.5,
        -0.1,
        "Smokers have higher charges compared to non-smokers",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax2.transAxes,
        fontsize=8,
    )

    # Plot 3: Number of Smokers and Non-Smokers by Gender
    ax3 = axes[1, 0]
    sns.countplot(
        x="smoker",
        hue="sex",
        data=df2.replace({"smoker": {1: "smoker", 0: "non-smoker"}}),
        ax=ax3,
    )
    ax3.set_title("Number of Smokers and Non-Smokers by Gender")
    ax3.set_xlabel("Smoker")
    ax3.set_ylabel("Count")
    ax3.legend(title="Gender", labels=["Female", "Male"])
    ax3.text(
        0.5,
        -0.1,
        "There are more non-smokers than smokers in the dataset \
            but more male smokers than female smokers",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax3.transAxes,
        fontsize=8,
    )

    # Plot 4: Bubble Plot: Age vs Charges by Smoking Status
    ax4 = axes[1, 1]
    sns.scatterplot(x="age", y="charges", hue="smoker", size="smoker", data=df2, ax=ax4)
    ax4.set_title("Bubble Plot: Age vs Charges by Smoking Status")
    ax4.set_xlabel("Age")
    ax4.set_ylabel("Charges")
    ax4.legend(title="Smoker", labels=["Non-Smoker", "Smoker"])
    ax4.text(
        0.5,
        -0.1,
        "The charges tend to increase with age and are higher for smokers compared to non-smokers.",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax4.transAxes,
        fontsize=8,
    )

    # Plot 5: Linear Regression: BMI vs Charges by Smoking Status
    ax5 = axes[2, 0]
    sns.regplot(
        x="bmi",
        y="charges",
        data=df2[df2["smoker"] == 1],
        ax=ax5,
        color="b",
        scatter_kws={"alpha": 0.6},
        line_kws={"color": "red"},
    )
    sns.regplot(
        x="bmi",
        y="charges",
        data=df2[df2["smoker"] == 0],
        ax=ax5,
        color="g",
        scatter_kws={"alpha": 0.6},
    )
    ax5.set_title("Linear Regression: BMI vs Charges by Smoking Status")
    ax5.set_xlabel("BMI")
    ax5.set_ylabel("Charges")
    ax5.text(
        0.5,
        -0.1,
        "There's a strong linear relationship between BMI and charges, \
         and the relationship is stronger for smokers compared to \
            non-smokers",
        horizontalalignment="center",
        verticalalignment="bottom",
        transform=ax5.transAxes,
        fontsize=8,
    )
    # Save the combined figure as a png file in output folder
    plt.savefig("output/eda_combined_plots.png")


def main():
    """
    Join the plots into one figure and save it as a png file
    """
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Combine plots into one figure")

    # Add arguments
    parser.add_argument("--input", type=str, help="Path to the input data file")
    parser.add_argument("--output", type=str, help="Path to the output figure file")

    # Parse the arguments
    args = parser.parse_args()

    # Load the data
    df2 = pd.read_parquet(args.input)  # noqa:W0612

    # Combine the plots
    combine_plots()

    # Save the combined figure
    plt.savefig(args.output)  # noqa:W0612


if __name__ == "__main__":
    main()
