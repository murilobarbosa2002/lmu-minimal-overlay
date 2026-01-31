import pytest
from unittest.mock import Mock, patch
import pygame
import sys
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

@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_init_windows_os(mock_init, mock_set_mode):
    # Mock pywin32 modules
    mock_win32gui = Mock()
    mock_win32con = Mock()
    mock_win32api = Mock()
    
        # Configure mock constants
    mock_win32con.GWL_EXSTYLE = 1
    mock_win32con.WS_EX_LAYERED = 2
    mock_win32con.LWA_COLORKEY = 3
    mock_win32con.LWA_ALPHA = 4
    
    # Configure GetWindowLong return value
    mock_win32gui.GetWindowLong.return_value = 0
    
    # Mock window info
    with patch('sys.platform', 'win32'), \
         patch('sys.modules', {
             'win32gui': mock_win32gui,
             'win32con': mock_win32con,
             'win32api': mock_win32api
         }), \
         patch('pygame.display.get_wm_info', return_value={"window": 12345}):
        
        wm = WindowManager()
        wm.init()
        
        # Verify pywin32 calls
        mock_win32gui.GetWindowLong.assert_called_once()
        mock_win32gui.SetWindowLong.assert_called_once()
        # Verify call with updated arguments
        mock_win32gui.SetLayeredWindowAttributes.assert_called_with(
            12345, 
            mock_win32api.RGB(255, 0, 128), 
            217, 
            7 # 3 | 4
        )

@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_init_windows_os_import_error(mock_init, mock_set_mode):
    with patch('sys.platform', 'win32'):
        with patch('pygame.display.get_wm_info', return_value={'window': 12345}):
            # Just ensure that if import fails, the code doesn't crash.
            # We rely on the fact that on Linux, importing win32gui fails safely within the try/except block
            wm = WindowManager()
            wm.init()
            assert wm.is_running is True

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
    wm._surface = Mock()
    wm.clear()
    
    wm._surface.fill.assert_called_once_with((255, 0, 128))

def test_clear_screen_no_surface():
    wm = WindowManager()
    wm._surface = None
    # Should not raise exception
    wm.clear()


def test_window_with_custom_transparency_handler():
    custom_handler = Mock()
    wm = WindowManager(transparency_handler=custom_handler)
    
    assert wm.transparency_handler is custom_handler


def test_surface_property_getter():
    wm = WindowManager()
    wm._surface = Mock()
    
    assert wm.surface is wm._surface

