"""Module for data upload."""

import pandas as pd


class FileUploader:
    """Handles file upload and data initialization."""

    def __init__(self, file_types=None, default_file=None) -> None:
        """
        Initializes the FileUploader with allowed file types and a default file.

        Args:
            file_types (list, optional): List of allowed file types for upload. Defaults to ["csv", "xlsx"].
            default_file (str, optional): Path to a default file to load if no file is uploaded. Defaults to None.
        """
        self.file_types = file_types or ["csv", "xlsx"]
        self.default_file = default_file

    def is_new_file(self, file, session_state) -> bool:
        """
        Checks if the uploaded file is new.

        Args:
            file: The uploaded file.
            session_state (dict): The session state to track the uploaded file.

        Returns:
            bool: True if the file is new, False otherwise.
        """
        return session_state.get("uploaded_file_name") != file.name

    def process_upload(self, file, session_state) -> None:
        """
        Processes the uploaded file and initializes the dataset in the session state.

        Args:
            file: The uploaded file.
            session_state (dict): The session state to store the dataset.
        """
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        session_state["original_df"] = df.copy()
        session_state["df"] = df.copy()
        session_state["uploaded_file_name"] = file.name

    def load_default_file(self, session_state) -> None:
        """
        Loads the default file and initializes the dataset in the session state.

        Args:
            session_state (dict): The session state to store the dataset.
        """
        if not self.default_file:
            raise ValueError("No default file specified.")
        loader = pd.read_csv if self.default_file.endswith(".csv") else pd.read_excel
        df = loader(self.default_file)
        session_state["original_df"] = df.copy()
        session_state["df"] = df.copy()
