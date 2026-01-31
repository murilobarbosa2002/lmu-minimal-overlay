import pytest
from unittest.mock import Mock, patch
import pygame
from src.ui.window import WindowManager

@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_initialization(mock_init, mock_set_mode):
    wm = WindowManager(title="Test", width=100, height=100)
    wm.init()
    
    mock_init.assert_called_once()
    mock_set_mode.assert_called_once()
    assert wm.is_running is True

@patch('pygame.event.get')
def test_handle_events_quit(mock_get):
    wm = WindowManager()
    wm.is_running = True
    
    # Simulate QUIT event
    mock_event = Mock()
    mock_event.type = pygame.QUIT
    mock_get.return_value = [mock_event]
    
    events = wm.handle_events()
    
    assert wm.is_running is False
    assert len(events) == 1

def test_set_transparent_safe():
    # Should not raise error on Linux/Test env
    wm = WindowManager()
    wm.set_transparent(True)
    wm.set_transparent(False)

@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_init_windows_os(mock_init, mock_set_mode):
    with patch('os.name', 'nt'):
        wm = WindowManager()
        wm.init()
        # Should have NOFRAME flag
        args, _ = mock_set_mode.call_args
        flags = args[1]
        assert flags & pygame.NOFRAME

@patch('pygame.display.flip')
def test_update_display(mock_flip):
    wm = WindowManager()
    wm.clock = Mock()
    wm.update_display()
    
    mock_flip.assert_called_once()
    wm.clock.tick.assert_called_once_with(wm.fps)

@patch('pygame.quit')
def test_close(mock_quit):
    wm = WindowManager()
    wm.is_running = True
    wm.close()
    assert wm.is_running is False
    mock_quit.assert_called_once()

def test_clear_screen():
    wm = WindowManager()
    wm.surface = Mock()
    wm.clear()
    
    wm.surface.fill.assert_called_once_with((0, 0, 0, 0))

def test_clear_screen_no_surface():
    wm = WindowManager()
    wm.surface = None
    # Should not raise exception
    wm.clear()

def test_set_transparent_windows():
    with patch('os.name', 'nt'):
        wm = WindowManager()
        # Should execute safely (stub)
        wm.set_transparent(True)
