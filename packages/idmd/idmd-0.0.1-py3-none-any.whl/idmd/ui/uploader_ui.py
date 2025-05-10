"""Module for file uploader component."""

import streamlit as st

from ..data.uploader import FileUploader
from .base import Component


class FileUploaderUI(Component):
    """Provides UI for file uploading."""

    def __init__(self, position: int = 0, file_types=None, default_file=None) -> None:
        """
        Initializes the FileUploaderUI component with a specific position, file types, and a default file.

        Args:
            position (int): The column position of the component. Defaults to 0.
            file_types (list, optional): List of allowed file types for upload. Defaults to ["csv", "xlsx"].
            default_file (str, optional): Path to a default file to load if no file is uploaded. Defaults to None.
        """
        super().__init__(position)
        self.uploader = FileUploader(file_types=file_types, default_file=default_file)

    def render(self) -> None:
        """
        Renders the file uploader in the Streamlit interface.

        Handles file uploads and initializes the dataset in the session state.
        """
        st.header("File Upload")
        uploaded_file = st.file_uploader(
            "Upload a CSV or Excel file", type=self.uploader.file_types, key="file_uploader"
        )

        if uploaded_file and self.uploader.is_new_file(uploaded_file, st.session_state):
            self.uploader.process_upload(uploaded_file, st.session_state)

        if self.uploader.default_file and not st.session_state.get("df"):
            try:
                self.uploader.load_default_file(st.session_state)
            except ValueError as e:
                st.error(str(e))
