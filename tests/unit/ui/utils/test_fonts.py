import pytest
from unittest.mock import Mock, patch
from src.ui.utils.fonts import FontManager
import pygame

def test_get_font_loads_from_assets_success():
    FontManager._fonts = {}
    with patch('os.path.exists', return_value=True), \
         patch('pygame.font.Font') as mock_font_cls, \
         patch('pygame.font.get_init', return_value=True):
        
        mock_font_instance = Mock()
        mock_font_cls.return_value = mock_font_instance
        
        font = FontManager.get_font(20, bold=True)
        
        assert font == mock_font_instance
        mock_font_instance.render.assert_called() # Check validation call

def test_get_font_assets_fails_fallback_to_system():
    FontManager._fonts = {}
    # exists=True but Font() raises Exception
    with patch('os.path.exists', return_value=True), \
         patch('pygame.font.Font', side_effect=Exception("Corrupt file")), \
         patch('pygame.font.SysFont') as mock_sys_font, \
         patch('pygame.font.get_init', return_value=True):
        
        FontManager.get_font(20)
        
        mock_sys_font.assert_called_once()

def test_get_font_system_fails_fallback_to_default():
    FontManager._fonts = {}
    with patch('os.path.exists', return_value=False), \
         patch('pygame.font.SysFont', side_effect=Exception("No system font")), \
         patch('pygame.font.Font') as mock_font_cls, \
         patch('pygame.font.get_init', return_value=True):
        
        FontManager.get_font(20)
        
        # Should call Font(None, size)
        mock_font_cls.assert_called_with(None, 20)
        
def test_font_init_called_if_needed():
    FontManager._fonts = {}
    with patch('pygame.font.get_init', return_value=False), \
         patch('pygame.font.init') as mock_init, \
         patch('os.path.exists', return_value=False), \
         patch('pygame.font.SysFont'):
        
        FontManager.get_font(10)
        mock_init.assert_called_once()
