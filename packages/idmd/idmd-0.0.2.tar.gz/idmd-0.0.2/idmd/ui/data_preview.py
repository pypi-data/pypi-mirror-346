"""Module for data preview component."""

import streamlit as st

from .base import Component


class DataPreview(Component):
    """Component to display a preview of the dataset."""

    def render(self) -> None:
        """
        Renders the dataset preview in the Streamlit interface.

        Displays the first few rows of the dataset if it exists in the session state.
        """
        if "df" in st.session_state:
            df = st.session_state.df
            st.header("Dataset Preview")
            st.dataframe(df.head())
            st.session_state._refresh_preview = False

            col1, col2, _ = st.columns([1, 1, 2])

            with col1:
                if st.button("Refresh Preview"):
                    st.session_state._refresh_preview = True

            with col2:
                if st.button("Reset to Default Data"):
                    if "original_df" in st.session_state:
                        st.session_state.df = st.session_state.original_df.copy()
                        st.success("Data has been reset to original upload.")
                        st.session_state._refresh_preview = True
                    else:
                        st.warning("No original data found to reset.")
