"""Module for data visualization."""

from typing import List

import pandas as pd

from .heatmaps import HeatmapGenerator
from .histograms import HistogramGenerator
from .plots import PlotGenerator


class DataVisualizer:
    """Utility class for generating visualizations."""

    @staticmethod
    def generate_line_plot(df: pd.DataFrame, columns: List[str]):
        """
        Generates a line plot using PlotGenerator.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the line plot.

        Returns:
            plt.Figure: The generated line plot.
        """
        return PlotGenerator.generate_line_plot(df, columns)

    @staticmethod
    def generate_bar_plot(df: pd.DataFrame, column: str):
        """
        Generates a bar plot using PlotGenerator.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The column to include in the bar plot.

        Returns:
            plt.Figure: The generated bar plot.
        """
        return PlotGenerator.generate_bar_plot(df, column)

    @staticmethod
    def generate_correlation_heatmap(df: pd.DataFrame, columns: List[str]):
        """
        Generates a correlation heatmap using HeatmapGenerator.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the heatmap.

        Returns:
            plt.Figure: The generated heatmap.
        """
        return HeatmapGenerator.generate_correlation_heatmap(df, columns)

    @staticmethod
    def generate_histograms(df: pd.DataFrame, columns: List[str]):
        """
        Generates histograms using HistogramGenerator.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the histograms.

        Returns:
            plt.Figure: The generated histograms.
        """
        return HistogramGenerator.generate_histograms(df, columns)

    @staticmethod
    def generate_overview(df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates an overview of the dataset, including data types and plottability.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.

        Returns:
            pd.DataFrame: A DataFrame containing the overview information.
        """
        return pd.DataFrame(
            {
                "Data Type": [df[col].dtype for col in df.columns],
                "Plottable": [pd.api.types.is_numeric_dtype(df[col]) for col in df.columns],
            },
            index=df.columns,
        ).T
