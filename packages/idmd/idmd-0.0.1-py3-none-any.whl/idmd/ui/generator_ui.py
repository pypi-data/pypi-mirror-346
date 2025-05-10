"""Module for data generator component."""

import streamlit as st

from ..data.generator import DatasetGenerator
from .base import Component


class DataGeneratorUI(Component):
    """Provides UI for generating sample datasets."""

    def render(self) -> None:
        """
        Renders the dataset generator UI in the Streamlit interface.

        Allows users to generate datasets with different distributions.
        """
        st.header("Generate Sample Dataset")
        distribution = st.selectbox(
            "Select Distribution",
            ["Normal Distribution", "Uniform Distribution", "Random Integers"],
            key="distribution_selector",
        )

        size = st.number_input("Number of Samples", min_value=1, value=100, step=1, key="size_input")

        if distribution == "Normal Distribution":
            self._render_normal_distribution(size)
        elif distribution == "Uniform Distribution":
            self._render_uniform_distribution(size)
        elif distribution == "Random Integers":
            self._render_random_integers(size)

    def _render_normal_distribution(self, size: int) -> None:
        """
        Renders the UI for generating a normal distribution dataset.

        Args:
            size (int): Number of samples.
        """
        mean = st.number_input("Mean", value=0.0, step=0.1, key="normal_mean_input")
        std = st.number_input("Standard Deviation", value=1.0, step=0.1, key="normal_std_input")

        if st.button("Generate Normal Distribution"):
            df = DatasetGenerator.generate_normal_distribution(size=(size, 1), mean=mean, std=std)
            st.session_state.df = df
            st.success("Normal distribution dataset generated!")
            st.dataframe(df.head())

    def _render_uniform_distribution(self, size: int) -> None:
        """
        Renders the UI for generating a uniform distribution dataset.

        Args:
            size (int): Number of samples.
        """
        low = st.number_input("Lower Bound", value=0.0, step=0.1, key="uniform_low_input")
        high = st.number_input("Upper Bound", value=1.0, step=0.1, key="uniform_high_input")

        if st.button("Generate Uniform Distribution"):
            df = DatasetGenerator.generate_uniform_distribution(size=(size, 1), low=low, high=high)
            st.session_state.df = df
            st.success("Uniform distribution dataset generated!")
            st.dataframe(df.head())

    def _render_random_integers(self, size: int) -> None:
        """
        Renders the UI for generating a random integers dataset.

        Args:
            size (int): Number of samples.
        """
        low = st.number_input("Lower Bound", value=0, step=1, key="random_low_input")
        high = st.number_input("Upper Bound", value=100, step=1, key="random_high_input")

        if st.button("Generate Random Integers"):
            df = DatasetGenerator.generate_random_integers(size=(size, 1), low=low, high=high)
            st.session_state.df = df
            st.success("Random integers dataset generated!")
            st.dataframe(df.head())
