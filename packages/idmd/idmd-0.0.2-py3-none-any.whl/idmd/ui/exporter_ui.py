"""Module for data exporter component."""

import streamlit as st

from ..data.exporter import DataExporter
from .base import Component


class DataExporterUI(Component):
    """Provides UI for exporting data."""

    def render(self) -> None:
        """
        Renders the data export functionality in the Streamlit interface.

        Displays a download button for the processed dataset if it exists in the session state.
        """
        st.header("Data Export")

        if not DataExporter.validate_data(st.session_state):
            st.warning("No dataset available for export.")
            return

        self._render_export_button()

    def _render_export_button(self) -> None:
        """
        Renders the download button for exporting the dataset.
        """
        export_df = st.session_state.df
        csv_data = DataExporter.export_to_csv(export_df)

        st.download_button(
            label="Download Processed Data",
            data=csv_data,
            file_name="processed_data.csv",
            mime="text/csv",
            key="export_button",
        )
