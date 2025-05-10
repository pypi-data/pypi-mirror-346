"""
Python package for data description, manipulation and visualization.
Contains the following modules: data, manipulation, report, ui, visualization, app.py.
These modules contain more submodules (except for app.py).
"""

from importlib.metadata import PackageNotFoundError, version

from .app import DataApp
from .ui.columns_ui import ColumnManipulatorUI
from .ui.data_preview import DataPreview
from .ui.data_stats import DataStats
from .ui.exporter_ui import DataExporterUI
from .ui.generator_ui import DataGeneratorUI
from .ui.replace_ui import ReplaceUI
from .ui.report_ui import ReportUI
from .ui.uploader_generator_ui import FileGeneratorUI
from .ui.uploader_ui import FileUploaderUI
from .ui.visualizer_ui import DataVisualizerUI

__all__ = [
    "DataApp",
    "FileUploaderUI",
    "FileGeneratorUI",
    "DataExporterUI",
    "DataGeneratorUI",
    "ColumnManipulatorUI",
    "DataStats",
    "DataPreview",
    "ReplaceUI",
    "ReportUI",
    "DataVisualizerUI",
]

try:
    __version__ = version("idmd")
except PackageNotFoundError:
    __version__ = "0.0"
