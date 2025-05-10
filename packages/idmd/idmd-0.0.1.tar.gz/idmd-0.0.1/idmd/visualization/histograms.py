"""Module for histogram generation."""

from typing import List

import matplotlib.pyplot as plt
import pandas as pd


class HistogramGenerator:
    """Generates histograms for numerical columns."""

    @staticmethod
    def generate_histograms(df: pd.DataFrame, columns: List[str]) -> plt.Figure:
        """
        Generates histograms for the specified columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            columns (List[str]): The columns to include in the histograms.

        Returns:
            plt.Figure: The generated histograms.
        """
        n_cols = 3
        n_rows = (len(columns) + n_cols - 1) // n_cols
        fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))

        axs = axs.flatten()

        for idx, col in enumerate(columns):
            axs[idx].hist(df[col].dropna(), bins=20, alpha=0.7, color="blue")
            axs[idx].set_title(f"Histogram of {col}")
            axs[idx].set_xlabel("Values")
            axs[idx].set_ylabel("Frequency")

        # Hide any empty subplots
        for i in range(len(columns), len(axs)):
            axs[i].axis("off")

        fig.tight_layout()
        return fig
