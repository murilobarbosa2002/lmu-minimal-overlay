import pytest
from unittest.mock import Mock, patch
from src.core.infrastructure.app_factory import AppFactory


class TestAppFactory:
    @patch("src.core.infrastructure.app_factory.ConfigManager")
    @patch("src.core.infrastructure.app_factory.WindowManager")
    @patch("src.core.infrastructure.app_factory.MockTelemetryProvider")
    @patch("src.core.infrastructure.app_factory.PygameFontProvider")
    @patch("src.core.infrastructure.app_factory.OverlayApp")
    def test_create_wires_dependencies(
        self, mock_app_class, mock_font, mock_provider, mock_window, mock_config
    ):
        mock_app_instance = Mock()
        mock_app_class.return_value = mock_app_instance

        result = AppFactory.create()

        assert result is mock_app_instance
        mock_app_class.assert_called_once()

        call_kwargs = mock_app_class.call_args[1]
        assert "window" in call_kwargs
        assert "provider" in call_kwargs
        assert "font_provider" in call_kwargs
        assert "config_manager" in call_kwargs

    @patch("src.core.infrastructure.app_factory.WidgetFactory")
    @patch("src.core.infrastructure.app_factory.WindowManager")
    @patch("src.core.infrastructure.app_factory.PygameFontProvider")
    @patch("src.core.infrastructure.app_factory.MockTelemetryProvider")
    @patch("src.core.infrastructure.app_factory.ConfigManager")
    def test_create_uses_di_container(
        self, mock_config, mock_provider, mock_font, mock_window, mock_factory
    ):
        mock_config_instance = Mock()
        mock_config_instance.get_config.return_value = {
            "title": "LMU Telemetry Overlay",
            "default_width": 1920,
            "default_height": 1080,
        }
        mock_config.return_value = mock_config_instance

        AppFactory.create()

        mock_provider.assert_called_once()
        mock_font.assert_called_once()
        mock_window.assert_called_once_with(
            title="LMU Telemetry Overlay", width=1920, height=1080
        )
        mock_factory.assert_called_once()
        mock_config.assert_called_once()
