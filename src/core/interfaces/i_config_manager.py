from abc import ABC, abstractmethod
from typing import Any


class IConfigManager(ABC):

    @abstractmethod
    def load_config(self) -> None:
        pass

    @abstractmethod
    def save_config(self) -> None:
        pass

    @abstractmethod
    def load_layout(self) -> None:
        pass

    @abstractmethod
    def save_layout(self) -> None:
        pass

    @abstractmethod
    def get_config(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set_config(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_layout(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set_layout(self, key: str, value: Any) -> None:
        pass
