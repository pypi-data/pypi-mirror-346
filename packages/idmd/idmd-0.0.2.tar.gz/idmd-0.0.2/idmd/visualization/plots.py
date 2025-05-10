"""Module for plot generation."""

from typing import List

import matplotlib.pyplot as plt
import pandas as pd


class PlotGenerator:
    """Generates various types of plots."""

    @staticmethod
    def generate_line_plot(df: pd.DataFrame, columns: List[str]) -> plt.Figure:
        """
        Generates a line plot for the specified columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the line plot.

        Returns:
            plt.Figure: The generated line plot.
        """
        fig, ax = plt.subplots()
        df[columns].plot(ax=ax)
        ax.set_title("Line Plot")
        ax.set_xlabel("Index")
        ax.set_ylabel("Values")
        return fig

    @staticmethod
    def generate_bar_plot(df: pd.DataFrame, column: str) -> plt.Figure:
        """
        Generates a bar plot for the specified column.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The column to include in the bar plot.

        Returns:
            plt.Figure: The generated bar plot.
        """
        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind="bar", ax=ax)
        ax.set_title(f"Bar Plot of {column}")
        ax.set_xlabel("Categories")
        ax.set_ylabel("Frequency")
        return fig
