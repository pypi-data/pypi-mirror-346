"""Module for orchestrating component integration."""

from typing import Dict, List, Optional, Tuple

import streamlit as st
from idmd.ui.base import Component
from streamlit.commands.page_config import Layout


class DataApp:
    """Orchestrates component integration and layout for a Streamlit application."""

    def __init__(self, title: str = "Interactive Data Manipulator and Descriptor", layout: Layout = "wide") -> None:
        """
        Initializes the DataApp with a title and layout.

        Args:
            title (str): The title of the application. Defaults to "Interactive Data Manipulator and Descriptor".
            layout (str): The layout of the application. Can be "centered" or "wide". Defaults to "wide".
        """
        st.set_page_config(layout=layout, page_title=title)
        self.title: str = title
        self.title_color: Optional[str] = None
        self.components: List[Component] = []
        self.column_names: Dict[int, Tuple[str, Optional[str]]] = {}

    def set_title_color(self, color: str) -> "DataApp":
        """
        Sets a color for the application title.

        Args:
            color (str): The color to set for the title (e.g., "red", "#FF5733").

        Returns:
            DataApp: The current instance of the DataApp, allowing method chaining.
        """
        self.title_color = color
        return self

    def add_component(self, component: Component) -> "DataApp":
        """
        Registers a component to the application.

        Args:
            component (Component): The component to add. The component must have a
                `position` attribute and a `render` method.

        Returns:
            DataApp: The current instance of the DataApp, allowing method chaining.
        """
        self.components.append(component)
        return self

    def set_column_name(self, column_index: int, name: str, color: Optional[str] = None) -> "DataApp":
        """
        Sets a name and optional color for a specific column.

        Args:
            column_index (int): The index of the column.
            name (str): The name to set for the column.
            color (Optional[str]): The color to set for the column name (e.g., "blue", "#123456"). Defaults to None.

        Returns:
            DataApp: The current instance of the DataApp, allowing method chaining.
        """
        self.column_names[column_index] = (name, color)
        return self

    def run(self) -> None:
        """
        Executes the application rendering process.

        This method sets the title of the application and renders all registered components.
        """
        if self.title_color:
            st.markdown(f"<h1 style='color:{self.title_color};'>{self.title}</h1>", unsafe_allow_html=True)
        else:
            st.title(self.title)
        st.divider()
        self._render_components()

    def _render_components(self) -> None:
        """
        Renders all registered components in their respective positions.

        Components are grouped by their `position` attribute, and columns are dynamically created
        based on the number of unique positions.
        """
        positions = sorted(set(c.position for c in self.components))
        num_columns = len(positions)

        columns = st.columns(num_columns)

        for i, position in enumerate(positions):
            with columns[i]:
                # Render column name if it exists
                if position in self.column_names:
                    name, color = self.column_names[position]
                    if color:
                        st.markdown(f"<h1 style='color:{color};'>{name}</h1>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"# {name}")

                # Render components in this column
                for comp in self._components_by_position(position):
                    comp.render()

    def _components_by_position(self, position: int) -> List[Component]:
        """
        Filters components by their position.

        Args:
            position (int): The position to filter components by.

        Returns:
            List[Component]: A list of components that match the given position.
        """
        return [c for c in self.components if c.position == position]
