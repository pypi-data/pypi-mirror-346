"""Module for report generator component."""

import streamlit as st

from ..report.report import ReportGenerator
from .base import Component


class ReportUI(Component):
    """Provides UI for generating PDF reports."""

    def render(self) -> None:
        """
        Renders the UI for generating a PDF report of the dataset.
        """
        st.header("Generate PDF Report")

        if "df" not in st.session_state:
            st.warning("No dataset available. Please upload a dataset first.")
            return

        df = st.session_state.df

        if st.button("Generate PDF Report"):
            plot_cols = st.session_state.get("custom_plot_cols")
            heatmap_cols = st.session_state.get("custom_heatmap_cols")
            hist_cols = st.session_state.get("custom_hist_cols")

            pdf_buffer = ReportGenerator.create_pdf_report(df, plot_cols, heatmap_cols, hist_cols)
            st.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name="data_report.pdf",
                mime="application/pdf",
            )
