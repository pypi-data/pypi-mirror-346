"""Module for All UI components."""

from abc import ABC, abstractmethod


class Component(ABC):
    """Abstract base class for all UI components."""

    def __init__(self, position: int = 0) -> None:
        """
        Initializes the component with a default position.

        Args:
            position (int): The column position of the component. Defaults to 0.
        """
        self.position = position

    @abstractmethod
    def render(self) -> None:
        """Render the component in the Streamlit interface."""
        raise NotImplementedError
