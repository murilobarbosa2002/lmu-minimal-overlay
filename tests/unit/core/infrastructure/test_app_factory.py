import pytest
from unittest.mock import Mock, patch
from src.core.infrastructure.app_factory import AppFactory


class TestAppFactory:
    @patch('src.core.infrastructure.app_factory.WindowManager')
    @patch('src.core.infrastructure.app_factory.MockTelemetryProvider')
    @patch('src.core.infrastructure.app_factory.PygameFontProvider')
    @patch('src.core.infrastructure.app_factory.OverlayApp')
    def test_create_wires_dependencies(self, mock_app_class, mock_font, mock_provider, mock_window):
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance
        
        result = AppFactory.create()
       
        
        assert result is mock_app_instance
        mock_app_class.assert_called_once()
        
        call_kwargs = mock_app_class.call_args[1]
        assert 'window' in call_kwargs
        assert 'provider' in call_kwargs
        assert 'font_provider' in call_kwargs

    @patch('src.core.infrastructure.app_factory.WindowManager')
    @patch('src.core.infrastructure.app_factory.MockTelemetryProvider')
    @patch('src.core.infrastructure.app_factory.PygameFontProvider')
    @patch('src.core.infrastructure.app_factory.OverlayApp')
    def test_create_uses_di_container(self, mock_app, mock_font, mock_provider, mock_window):
        AppFactory.create()
        
        mock_window.assert_called_once_with(title="LMU Telemetry Overlay", width=1920, height=1080)
        mock_provider.assert_called_once()
        mock_font.assert_called_once()
