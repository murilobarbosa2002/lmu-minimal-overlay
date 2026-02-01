from abc import ABC, abstractmethod
import pygame


class IWindowManager(ABC):
    @abstractmethod
    def init(self) -> None:
        pass

    @abstractmethod
    def set_position(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def update_display(self) -> None:
        pass

    @abstractmethod
    def handle_events(self) -> list[pygame.event.Event]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @property
    @abstractmethod
    def surface(self) -> pygame.Surface | None:
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        pass

    @is_running.setter
    @abstractmethod
    def is_running(self, value: bool) -> None:
        pass
