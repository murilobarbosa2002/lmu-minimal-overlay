from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class IConfigManager(ABC):
    """Interface for configuration management."""

    @abstractmethod
    def load_config(self) -> None:
        """Loads configuration from disk."""
        pass

    @abstractmethod
    def save_config(self) -> None:
        """Saves current configuration to disk."""
        pass

    @abstractmethod
    def load_layout(self) -> None:
        """Loads layout from disk."""
        pass

    @abstractmethod
    def save_layout(self) -> None:
        """Saves current layout to disk."""
        pass

    @abstractmethod
    def get_config(self, key: str, default: Any = None) -> Any:
        """Retrieves a configuration value."""
        pass

    @abstractmethod
    def set_config(self, key: str, value: Any) -> None:
        """Sets a configuration value."""
        pass

    @abstractmethod
    def get_layout(self, key: str, default: Any = None) -> Any:
        """Retrieves a layout value."""
        pass

    @abstractmethod
    def set_layout(self, key: str, value: Any) -> None:
        """Sets a layout value."""
        pass
