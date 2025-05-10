# Interactive Data Manipulator and Descriptor (IDMD)
## Overview

The **Interactive Data Manipulator and Descriptor (IDMD)** is a Python package designed for interactive data exploration, manipulation, visualization, and reporting. It provides a modular structure for handling datasets, making it easy to extend and maintain. (Scientific Python course at PPCU - project work)

![idmd chart](https://raw.githubusercontent.com/CsongorLaczko/idmd/4fc799ad815ab0c828b6be8fa24a2f06ebc0dbbc/images/idmd_chart.svg)

## Dependencies

The IDMD package requires the following main dependencies:
- matplotlib
- streamlit
- pandas

For specific version requirements, refer to the `requirements.txt` file. If you are developing or contributing to the project, additional tools for code quality, formatting, linting, and testing are listed in `requirements-dev.txt`.

---

## Package Structure

### `data` Module
Handles all data-related operations, such as file uploading, dataset generation, and exporting.

- **Submodules**:
  - `export.py`: Handles exporting datasets to CSV or other formats.
  - `generator.py`: Generates sample datasets with different distributions.
  - `uploader.py`: Handles file uploads and loading datasets.

---

### `manipulation` Module
Provides functionality for manipulating datasets.

- **Submodules**:
  - `columns.py`: Handles column-specific operations like swapping, dropping, and selecting columns.
  - `replace.py`: Handles value-specific operations like replacing values with mean, median, or other methods.

---

### `ui` Module
Contains components for rendering the Streamlit interface.

- **Submodules**:
  - `base.py`: Defines the abstract `Component` class for all UI components.
  - `columns_ui.py`: Provides UI for column manipulation.
  - `data_preview.py`: Displays a preview of the dataset.
  - `data_stats.py`: Displays dataset statistics and metadata.
  - `exporter_ui.py`: Provides UI for exporting data.
  - `generator_ui.py`: Provides UI for generating data.
  - `replace_ui.py`: Provides UI for replacing operations.
  - `uploader_ui.py`: Provides UI for file uploading.
  - `visualizer_ui.py`: Provides UI for visualizing data, including default and custom plots.

---

### `visualization` Module
Handles data visualization.

- **Submodules**:
  - `plots.py`: Generates various types of plots (e.g., line plots, bar plots).
  - `heatmaps.py`: Generates correlation heatmaps.
  - `histograms.py`: Generates histograms.
  - `visualizer.py`: Utility class for generating visualizations, including line plots, histograms, and heatmaps.

---

### `report` Module
Handles report generation.

- **Submodules**:
  - `report.py`: Generates PDF reports with data and visualizations.

---

### `app.py`
Orchestrates the integration of all components and runs the Streamlit application.

---

## Features

1. **Sample Dataset Generation**:
   - Generate datasets with different distributions (e.g., normal, uniform).
   - Easily create synthetic data for testing and exploration.

2. **Data Manipulation**:
   - Swap, drop, and select columns.
   - Replace missing values with mean, median, or other methods.
   - Normalize or remove outliers.

3. **Data Visualization**:
   - Generate interactive plots, histograms, and heatmaps.
   - Explore data visually with Streamlit's interactivity.

4. **Data Export**:
   - Export processed datasets to CSV format.

5. **Report Generation**:
   - Generate PDF reports with data summaries and visualizations.

---

## Example Usage

Run the example application using:

```bash
streamlit run example_app.py
```

You can also explore the interactive example notebook `example_app.ipynb` that demonstrates:
- Package installation
- Creating a complete dashboard application
- Running the app locally or on Google Colab
- Using all major components of the package

Opening the resulting website, should show a dashboard like this:
![Dashboard example without data](https://github.com/CsongorLaczko/idmd/blob/main/images/Dashboard_without_data.png?raw=true)

Loading or generating data should show a similar result:
![Dashboard example with data 1](https://github.com/CsongorLaczko/idmd/blob/main/images/Dashboard_with_data_1.png?raw=true)
![Dashboard example with data 2](https://github.com/CsongorLaczko/idmd/blob/main/images/Dashboard_with_data_2.png?raw=true)

---

## Links

- [Homepage](https://github.com/CsongorLaczko/idmd)
- [Documentation](https://idmd.readthedocs.io)
- [Repository](https://github.com/CsongorLaczko/idmd.git)
- [Issues](https://github.com/CsongorLaczko/idmd/issues)