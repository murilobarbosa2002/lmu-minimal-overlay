import pytest
from unittest.mock import Mock, patch, call
import pygame
import sys
from src.ui.window import WindowManager

@patch('pygame.event.pump')
@patch('pygame.display.flip')
@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_initialization(mock_init, mock_set_mode, mock_flip, mock_pump):
    wm = WindowManager(title="Test", width=100, height=100)
    wm.clear = Mock() # Spy on clear

    wm.init()
    
    mock_init.assert_called_once()
    mock_set_mode.assert_called_once()
    assert wm.is_running is True
    
    # Check for robust startup sequence
    mock_pump.assert_called_once()
    assert wm.clear.call_count == 2
    assert mock_flip.call_count == 2

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

@patch('src.ui.window.time')
@patch('src.ui.window.pygame')
def test_window_init_windows_os(mock_pygame, mock_time):
    # Configure mock constants
    mock_pygame.SRCALPHA = 1
    mock_pygame.NOFRAME = 2
    mock_pygame.HIDDEN = 4
    mock_pygame.QUIT = 8
    
    # Configure mock methods
    mock_pygame.display.get_wm_info.return_value = {"window": 12345}
    
    # Mock pywin32 modules
    mock_win32gui = Mock()
    mock_win32con = Mock()
    mock_win32api = Mock()
    
    # Configure mock win32 constants (integers)
    mock_win32con.GWL_EXSTYLE = 1
    mock_win32con.WS_EX_LAYERED = 2
    mock_win32con.LWA_COLORKEY = 3
    mock_win32con.LWA_ALPHA = 4
    mock_win32con.HWND_TOPMOST = -1
    mock_win32con.SWP_NOMOVE = 2
    mock_win32con.SWP_NOSIZE = 1
    mock_win32con.SW_SHOW = 5
    mock_win32con.SWP_NOZORDER = 4
    mock_win32con.SWP_SHOWWINDOW = 64
    mock_win32con.SWP_FRAMECHANGED = 32
    mock_win32con.SWP_NOACTIVATE = 16
    
    # New style constants
    mock_win32con.WS_POPUP = 0x80000000
    mock_win32con.WS_VISIBLE = 0x10000000
    mock_win32con.GWL_STYLE = -16
    mock_win32con.WS_CAPTION = 0xC00000 # 12582912
    mock_win32con.WS_THICKFRAME = 0x40000 # 262144
    mock_win32con.WS_SYSMENU = 0x80000 # 524288

    # Configure GetWindowLong return value (simulating current style)
    # Return a style that HAS these bits so we can verify they are removed
    initial_style = mock_win32con.WS_CAPTION | mock_win32con.WS_THICKFRAME | mock_win32con.WS_SYSMENU
    mock_win32gui.GetWindowLong.side_effect = lambda hwnd, index: initial_style if index == mock_win32con.GWL_STYLE else 0
    
    with patch('sys.platform', 'win32'), \
         patch('sys.modules', {
             'win32gui': mock_win32gui,
             'win32con': mock_win32con,
             'win32api': mock_win32api
         }):
        
        wm = WindowManager()
        wm.init()
        
        # Verify pygame calls
        mock_pygame.init.assert_called_once()
        mock_pygame.display.set_mode.assert_called_once()
        mock_pygame.event.pump.assert_called_once()
        assert mock_pygame.display.flip.call_count == 2
        
        # Verify style stripping (GetWindowLong calls)
        # Should be called for GWL_STYLE (to strip) and GWL_EXSTYLE (to layer)
        # The logic in transparency handler calls GetWindowLong(GWL_STYLE) then SetWindowLong(GWL_STYLE)
        assert mock_win32gui.GetWindowLong.call_count >= 1
        
        # Verify SetWindowLong calls
        assert mock_win32gui.SetWindowLong.call_count >= 1
        
        # Verify sleep call
        mock_time.sleep.assert_called_once_with(0.1)
        
        
        # Verify SetWindowPos calls
        # 1. Force off-screen
        # 2. Apply transparency (TopMost + FrameChanged)
        # 3. Move to final pos
        # 4. Show window (Silent)
        
        flags_move = mock_win32con.SWP_NOZORDER | mock_win32con.SWP_NOSIZE | mock_win32con.SWP_SHOWWINDOW | mock_win32con.SWP_NOACTIVATE
        flags_transparency = mock_win32con.SWP_NOMOVE | mock_win32con.SWP_NOSIZE | mock_win32con.SWP_FRAMECHANGED
        flags_show = mock_win32con.SWP_NOMOVE | mock_win32con.SWP_NOSIZE | mock_win32con.SWP_SHOWWINDOW | mock_win32con.SWP_NOACTIVATE

        mock_win32gui.SetWindowPos.assert_has_calls([
            call(12345, 0, -32000, -32000, 0, 0, flags_move),
            call(12345, mock_win32con.HWND_TOPMOST, 0, 0, 0, 0, flags_transparency),
            call(12345, 0, 100, 100, 0, 0, flags_move),
            call(12345, 0, 0, 0, 0, 0, flags_show)
        ])
        
        # Verify ShowWindow is NOT called (replaced by SetWindowPos silent)
        mock_win32gui.ShowWindow.assert_not_called()

@patch('pygame.event.pump')
@patch('pygame.display.flip')
@patch('pygame.display.set_mode')
@patch('pygame.init')
def test_window_init_windows_os_import_error(mock_init, mock_set_mode, mock_flip, mock_pump):
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

def test_clear_screen_linux():
    # Detects platform as linux/other
    with patch('sys.platform', 'linux'):
        wm = WindowManager()
        wm._surface = Mock()
        wm.clear()
        wm._surface.fill.assert_called_once_with((0, 0, 0, 0))

def test_clear_screen_windows():
    with patch('sys.platform', 'win32'):
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

@patch('os.environ', {})
def test_set_position():
    wm = WindowManager()
    wm.set_position(100, 200)
    
    assert wm.window_position_x == 100
    assert wm.window_position_y == 200
    import os
    assert os.environ['SDL_VIDEO_WINDOW_POS'] == "100,200"

