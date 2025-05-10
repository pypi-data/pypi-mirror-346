"""Module for data statistics component."""

import io

import streamlit as st

from ..ui.base import Component


class DataStats(Component):
    """Displays dataset statistics and metadata"""

    def render(self) -> None:
        if "df" not in st.session_state:
            return

        df = st.session_state.df

        with st.expander("Dataset Statistics"):
            self._show_basic_stats(df)
            self._show_column_info(df)

    def _show_basic_stats(self, df) -> None:
        if st.checkbox("Show Summary Statistics", key="stats_checkbox"):
            st.write(df.describe())

    def _show_column_info(self, df) -> None:
        if st.checkbox("Show Column Metadata", key="colinfo_checkbox"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
