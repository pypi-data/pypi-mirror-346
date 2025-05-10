"""Module for data export."""

import pandas as pd


class DataExporter:
    """Handles data export functionality."""

    @staticmethod
    def export_to_csv(df: pd.DataFrame) -> str:
        """
        Converts a DataFrame to a CSV string.

        Args:
            df (pd.DataFrame): The DataFrame to export.

        Returns:
            str: The CSV string representation of the DataFrame.
        """
        return df.to_csv(index=False)

    @staticmethod
    def validate_data(session_state) -> bool:
        """
        Validates if the dataset exists in the session state.

        Args:
            session_state (dict): The session state to check.

        Returns:
            bool: True if the dataset exists, False otherwise.
        """
        return "df" in session_state
