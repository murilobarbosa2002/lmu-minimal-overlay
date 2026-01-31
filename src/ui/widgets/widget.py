from abc import ABC, abstractmethod
import pygame
from src.core.domain.telemetry_data import TelemetryData

class Widget(ABC):
    """
    Abstract base class for all overlay widgets.
    
    Attributes:
        x (int): X position on screen
        y (int): Y position on screen
        width (int): Widget width
        height (int): Widget height
        rect (pygame.Rect): Collision and drawing rectangle
    """
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        
    def set_position(self, x: int, y: int) -> None:
        """Updates the widget position."""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
    def get_rect(self) -> pygame.Rect:
        """Returns the widget's rectangle."""
        return self.rect

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the widget on the given surface.
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        pass

    @abstractmethod
    def update(self, data: TelemetryData) -> None:
        """
        Updates the widget state based on telemetry data.
        
        Args:
            data (TelemetryData): Current telemetry snapshot
        """
        pass

    @abstractmethod
    def handle_input(self, event: pygame.event.Event) -> bool:
        """
        Handles user input events (e.g. clicks, drag).
        
        Args:
            event (pygame.event.Event): The pygame event
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        pass
