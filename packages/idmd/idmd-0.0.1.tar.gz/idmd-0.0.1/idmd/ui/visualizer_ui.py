"""Module for data visualizer component."""

from typing import List

import streamlit as st
from pandas import DataFrame

from ..visualization.visualizer import DataVisualizer
from .base import Component


class DataVisualizerUI(Component):
    """UI component for rendering data visualizations."""

    def render(self) -> None:
        """
        Renders the UI for visualizing data.
        """
        st.header("Data Visualizations")

        if "df" not in st.session_state:
            st.warning("No dataset available. Please upload a dataset first.")
            return

        df: DataFrame = st.session_state.df

        # Overview Section
        self._render_overview(df)

        # Visualization Options
        self._render_visualization_options(df)

    def _render_overview(self, df: DataFrame) -> None:
        """
        Renders the overview of the dataset.
        """
        st.subheader("Dataset Overview")
        overview: DataFrame = DataVisualizer.generate_overview(df)
        st.dataframe(overview)

    def _render_visualization_options(self, df: DataFrame) -> None:
        """
        Renders the visualization options, including default and custom plots.
        """
        st.subheader("Visualization Options")

        # Default Plots
        numeric_cols: List[str] = df.select_dtypes(include="number").columns.tolist()
        default_plot_cols: List[str] = numeric_cols[:10]

        if default_plot_cols:
            st.write("### Default Line Plot (First 10 Numeric Columns)")
            fig = DataVisualizer.generate_line_plot(df, default_plot_cols)
            st.pyplot(fig)

            st.write("### Default Correlation Heatmap (First 10 Numeric Columns)")
            fig = DataVisualizer.generate_correlation_heatmap(df, default_plot_cols)
            st.pyplot(fig)

            st.write("### Default Histograms (First 10 Numeric Columns)")
            fig = DataVisualizer.generate_histograms(df, default_plot_cols)
            st.pyplot(fig)

        # Custom Plots
        st.write("### Custom Visualization Builder")

        # Custom Line Plot
        selected_plot_cols: List[str] = st.multiselect("Select Columns for Line Plot", numeric_cols)
        if selected_plot_cols and st.button("Generate Line Plot"):
            fig = DataVisualizer.generate_line_plot(df, selected_plot_cols)
            st.pyplot(fig)

        # Custom Correlation Heatmap
        selected_heatmap_cols: List[str] = st.multiselect("Select Columns for Correlation Heatmap", numeric_cols)
        if selected_heatmap_cols and st.button("Generate Correlation Heatmap"):
            fig = DataVisualizer.generate_correlation_heatmap(df, selected_heatmap_cols)
            st.pyplot(fig)

        # Custom Histograms
        selected_hist_cols: List[str] = st.multiselect("Select Columns for Histograms", numeric_cols)
        if selected_hist_cols and st.button("Generate Histograms"):
            fig = DataVisualizer.generate_histograms(df, selected_hist_cols)
            st.pyplot(fig)
