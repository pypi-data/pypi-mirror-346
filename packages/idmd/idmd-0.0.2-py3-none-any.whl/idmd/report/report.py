"""Module for report generation."""

import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages


class ReportGenerator:
    """Handles the logic for generating PDF reports."""

    @staticmethod
    def create_pdf_report(df: pd.DataFrame, plot_cols=None, heatmap_cols=None, hist_cols=None) -> io.BytesIO:
        """
        Create a polished PDF report containing:
        - DataFrame preview
        - DataFrame statistics (rounded)
        - Line plot + correlation heatmap
        - Histograms in a compact grid

        Args:
            df (pd.DataFrame): The DataFrame to include in the report.
            plot_cols (list, optional): Columns to include in the line plot. Defaults to None.
            heatmap_cols (list, optional): Columns to include in the heatmap. Defaults to None.
            hist_cols (list, optional): Columns to include in the histograms. Defaults to None.

        Returns:
            io.BytesIO: A buffer containing the generated PDF report.
        """
        buffer = io.BytesIO()
        A4_inches = (8.27, 11.69)  # A4 size

        with PdfPages(buffer) as pdf:
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            plot_cols = plot_cols or numeric_cols[:10]
            heatmap_cols = heatmap_cols or numeric_cols[:10]
            hist_cols = hist_cols or numeric_cols[:10]

            # --- Page 1: Preview + Description ---
            fig = plt.figure(figsize=A4_inches)
            gs = gridspec.GridSpec(4, 1, height_ratios=[1.5, 0.5, 2, 2])

            # DataFrame Preview
            ax1 = fig.add_subplot(gs[0])
            ax1.axis("off")
            ax1.set_title("Dataframe Preview")
            table1 = ax1.table(cellText=df.head().values, colLabels=df.columns, loc="center")
            table1.auto_set_font_size(False)
            table1.set_fontsize(8)
            table1.scale(1, 1.5)

            # DataFrame Describe
            desc = df.describe().round(3)
            ax2 = fig.add_subplot(gs[2])
            ax2.axis("off")
            ax2.set_title("Dataframe Statistics")
            table2 = ax2.table(cellText=desc.values, colLabels=desc.columns, rowLabels=desc.index, loc="center")
            table2.auto_set_font_size(False)
            table2.set_fontsize(6)
            table2.scale(1, 1.5)

            fig.tight_layout(pad=1.0)
            pdf.savefig(fig)
            plt.close(fig)

            # --- Page 2: Line Plot + Correlation Heatmap ---
            fig = plt.figure(figsize=A4_inches)
            gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])

            ax1 = fig.add_subplot(gs[0])
            if plot_cols:
                df[plot_cols].plot(ax=ax1)
                ax1.set_title("Line Plot of Selected Columns", fontsize=12, fontweight="bold")
            ax1.set_xlabel("")
            ax1.set_ylabel("")

            ax2 = fig.add_subplot(gs[1])
            if heatmap_cols:
                sns.heatmap(df[heatmap_cols].corr(), annot=True, cmap="coolwarm", ax=ax2, cbar=True)
                ax2.set_title("Correlation Heatmap", fontsize=12, fontweight="bold")

            fig.tight_layout(pad=0.5)
            pdf.savefig(fig)
            plt.close(fig)

            # --- Page 3: All Histograms in one Figure (grid layout) ---
            n_cols = 3
            n_rows = (len(hist_cols) + n_cols - 1) // n_cols
            fig, axs = plt.subplots(n_rows, n_cols, figsize=A4_inches)

            axs = axs.flatten()

            for idx, col in enumerate(hist_cols):
                sns.histplot(df[col], kde=True, ax=axs[idx])
                axs[idx].set_title(f"Histogram of {col}", fontsize=10)
                axs[idx].set_xlabel("")
                axs[idx].set_ylabel("")

            # Hide any empty subplots
            for i in range(len(hist_cols), len(axs)):
                axs[i].axis("off")

            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

        buffer.seek(0)
        return buffer
