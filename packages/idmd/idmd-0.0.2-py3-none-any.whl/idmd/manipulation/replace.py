"""Module for value replacement."""

import pandas as pd


class ReplaceLogic:
    """Handles the logic for replacing values in a DataFrame."""

    @staticmethod
    def replace_values(df: pd.DataFrame, column: str, values_to_replace: str, replacement_method: str) -> pd.DataFrame:
        """
        Replaces values in a specified column of the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            column (str): The column to modify.
            values_to_replace (str): The type of values to replace ("0", "np.nan", "outliers", "all").
            replacement_method (str): The method to replace values ("median", "min", "max", "random", "np.nan").

        Returns:
            pd.DataFrame: The modified DataFrame.
        """
        col_data = df[column]

        if values_to_replace == "0":
            if replacement_method == "median":
                col_data = col_data.replace(0, col_data[col_data != 0].median())
            elif replacement_method == "min":
                col_data = col_data.replace(0, col_data[col_data != 0].min())
            elif replacement_method == "max":
                col_data = col_data.replace(0, col_data[col_data != 0].max())
            elif replacement_method == "random":
                col_data = col_data.replace(0, col_data[col_data != 0].sample(n=1).values[0])
            elif replacement_method == "np.nan":
                col_data = col_data.replace(0, pd.NA)

        elif values_to_replace == "np.nan":
            if replacement_method == "median":
                col_data = col_data.fillna(col_data.dropna().median())
            elif replacement_method == "min":
                col_data = col_data.fillna(col_data.dropna().min())
            elif replacement_method == "max":
                col_data = col_data.fillna(col_data.dropna().max())
            elif replacement_method == "random":
                col_data = col_data.fillna(col_data.dropna().sample(n=1).values[0])

        elif values_to_replace == "outliers":
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers_mask = (col_data < lower) | (col_data > upper)

            if replacement_method == "median":
                col_data[outliers_mask] = col_data[~outliers_mask].median()
            elif replacement_method == "min":
                col_data[outliers_mask] = col_data[~outliers_mask].min()
            elif replacement_method == "max":
                col_data[outliers_mask] = col_data[~outliers_mask].max()
            elif replacement_method == "random":
                col_data[outliers_mask] = col_data[~outliers_mask].sample(n=1).values[0]
            elif replacement_method == "np.nan":
                col_data[outliers_mask] = pd.NA

        elif values_to_replace == "all":
            if replacement_method == "median":
                col_data = col_data.fillna(col_data.dropna().median())
            elif replacement_method == "min":
                col_data = col_data.fillna(col_data.dropna().min())
            elif replacement_method == "max":
                col_data = col_data.fillna(col_data.dropna().max())
            elif replacement_method == "random":
                col_data = col_data.fillna(col_data.dropna().sample(n=1).values[0])
            elif replacement_method == "np.nan":
                col_data = col_data.fillna(pd.NA)

        df[column] = col_data.astype(df[column].dtype, errors="ignore")
        return df
