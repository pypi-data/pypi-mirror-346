"""Module for column manipulation."""

from typing import List

import pandas as pd


class ColumnManipulatorLogic:
    """Handles the logic for column operations and transformations."""

    @staticmethod
    def swap_columns(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
        """
        Swap two columns in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            col1 (str): The first column to swap.
            col2 (str): The second column to swap.

        Returns:
            pd.DataFrame: The modified DataFrame with swapped columns.
        """
        df = df.copy()
        col_order = df.columns.tolist()
        idx1, idx2 = col_order.index(col1), col_order.index(col2)
        col_order[idx1], col_order[idx2] = col_order[idx2], col_order[idx1]
        df[col1], df[col2] = df[col2], df[col1]
        return df[col_order]

    @staticmethod
    def drop_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Drop a column from the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            column (str): The column to drop.

        Returns:
            pd.DataFrame: The modified DataFrame without the dropped column.
        """
        return df.drop(columns=[column])

    @staticmethod
    def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Select specific columns to keep in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
            columns (List[str]): The list of columns to keep.

        Returns:
            pd.DataFrame: The modified DataFrame with only the selected columns.
        """
        return df[columns]
