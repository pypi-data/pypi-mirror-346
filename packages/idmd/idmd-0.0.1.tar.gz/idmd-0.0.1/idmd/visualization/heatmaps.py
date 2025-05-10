"""Module for heatmap generation."""

from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class HeatmapGenerator:
    """Generates correlation heatmaps."""

    @staticmethod
    def generate_correlation_heatmap(df: pd.DataFrame, columns: List[str]) -> plt.Figure:
        """
        Generates a correlation heatmap for the specified columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the heatmap.

        Returns:
            plt.Figure: The generated heatmap.
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        correlation_matrix = df[columns].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
        return fig
