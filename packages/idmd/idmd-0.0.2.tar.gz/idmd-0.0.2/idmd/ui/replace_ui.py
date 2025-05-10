"""Module for value replacement component."""

import streamlit as st
from pandas import DataFrame

from ..manipulation.replace import ReplaceLogic
from .base import Component


class ReplaceUI(Component):
    """Provides UI for replacing values in a DataFrame."""

    def render(self) -> None:
        """
        Renders the UI for replacing values in a column of the dataset.
        """
        st.header("Replace Values in Column")

        if "df" not in st.session_state:
            st.warning("No dataset available. Please upload a dataset first.")
            return

        df: DataFrame = st.session_state.df

        replace_col: str = st.selectbox("Select Column to Modify", df.columns)
        values_to_replace: str = st.selectbox("Select Values to Replace", ["0", "np.nan", "outliers", "all"])
        replacement_method: str = st.selectbox("Replace With", ["median", "min", "max", "random", "np.nan"])

        if st.button("Apply Value Replacement"):
            if replace_col and values_to_replace and replacement_method:
                updated_df: DataFrame = ReplaceLogic.replace_values(
                    df, replace_col, values_to_replace, replacement_method
                )
                st.session_state.df = updated_df
                st.success(f"Values in '{replace_col}' replaced successfully.")
            else:
                st.warning("Please select a column, values to replace, and replacement method.")
