"""Module for column manipulator component."""

import pandas as pd
import streamlit as st

from ..manipulation.columns import ColumnManipulatorLogic
from .base import Component


class ColumnManipulatorUI(Component):
    """Provides UI for column operations and transformations."""

    def render(self) -> None:
        """
        Renders column manipulation tools in the Streamlit interface.

        Provides options to swap, drop, and select columns.
        """
        st.header("Column Manipulation")

        if "df" not in st.session_state:
            st.warning("No dataset available. Please upload a dataset first.")
            return

        df = st.session_state.df

        self._render_column_swapper(df)
        self._render_column_dropper(df)
        self._render_column_selector(df)

    def _render_column_swapper(self, df: pd.DataFrame) -> None:
        """
        Renders the UI for swapping two columns.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
        """
        st.subheader("Swap Two Columns")
        col1, col2 = st.columns(2)

        with col1:
            col_a = st.selectbox("First Column", df.columns, key="swap_col1")
        with col2:
            col_b = st.selectbox("Second Column", df.columns, key="swap_col2")

        if st.button("Swap Columns"):
            if col_a != col_b:
                st.session_state.df = ColumnManipulatorLogic.swap_columns(df, col_a, col_b)
                st.success(f"Swapped columns: {col_a} ↔ {col_b}")
            else:
                st.warning("Please select two different columns.")

    def _render_column_dropper(self, df: pd.DataFrame) -> None:
        """
        Renders the UI for dropping a column.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
        """
        st.subheader("Drop a Column")
        drop_col = st.selectbox("Select Column to Remove", df.columns, key="drop_col")

        if st.button("Remove Column"):
            st.session_state.df = ColumnManipulatorLogic.drop_column(df, drop_col)
            st.success(f"Removed column: {drop_col}")

    def _render_column_selector(self, df: pd.DataFrame) -> None:
        """
        Renders the UI for selecting specific columns to keep.

        Args:
            df (pd.DataFrame): The DataFrame to modify.
        """
        st.subheader("Column Selection Filter")
        selected = st.multiselect("Select Columns to Keep", df.columns, default=list(df.columns), key="select_columns")

        if st.button("Apply Selection Filter"):
            st.session_state.df = ColumnManipulatorLogic.select_columns(df, selected)
            st.success("Updated the dataset with selected columns.")
