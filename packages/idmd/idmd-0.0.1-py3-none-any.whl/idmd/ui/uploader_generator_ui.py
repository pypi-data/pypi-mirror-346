import time

import pandas as pd
import streamlit as st

from ..data.generator import DatasetGenerator
from .base import Component


class FileGeneratorUI(Component):
    """Provides UI for data generation."""

    def __init__(self, position: int = 0) -> None:
        """
        Initializes the FileGeneratorUI component with a specific position.

        Args:
            position (int): The column position of the component. Defaults to 0.
        """
        super().__init__(position)

    def render(self) -> None:
        st.header("File Generation")

        selected_distribution = st.selectbox("Dataset Generation", options=["normal", "uniform", "random"])

        sample_count = st.number_input("Sample Size", min_value=1, step=1)
        column_count = st.number_input("Column Size", min_value=1, step=1)

        size = (sample_count, column_count)

        params: dict[str, int | float] = {}

        if selected_distribution == "normal":
            params["normal_mean"] = st.number_input("Mean")
            params["normal_sd"] = st.number_input("Standard Deviation", min_value=0)

        elif selected_distribution == "uniform":
            params["uni_lb"] = st.number_input("Lower Bound")
            params["uni_ub"] = st.number_input("Upper Bound")

        elif selected_distribution == "random":
            params["rnd_lb"] = st.number_input("Lower Bound", step=1)
            params["rnd_ub"] = st.number_input("Upper Bound", step=1)

        data: pd.DataFrame

        if st.button("Generate Dataset"):
            if selected_distribution == "normal":
                data = DatasetGenerator.generate_normal_distribution(size, params["normal_mean"], params["normal_sd"])
            elif selected_distribution == "uniform":
                data = DatasetGenerator.generate_uniform_distribution(size, params["uni_lb"], params["uni_ub"])
            elif selected_distribution == "random":
                data = DatasetGenerator.generate_random_integers(size, params["rnd_lb"], params["rnd_ub"])

            st.session_state["original_df"] = data.copy()
            st.session_state["df"] = data.copy()
            st.session_state["uploaded_file_name"] = f"{selected_distribution}_{time.time_ns()}.csv"
