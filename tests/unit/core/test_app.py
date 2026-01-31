import pytest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
import pygame
from src.core.app import OverlayApp


class TestOverlayApp:
    @pytest.fixture
    def app(self):
        mock_window = Mock()
        mock_window.surface = None
        mock_window.is_running = True
        
        mock_provider = Mock()
        mock_font_provider = Mock()
        
        return OverlayApp(
            window=mock_window,
            provider=mock_provider,
            font_provider=mock_font_provider
        )

    def test_setup_initializes_components(self, app):
        app.setup()
        
        app.window.init.assert_called_once()
        app.provider.connect.assert_called_once()
        assert len(app.widgets) == 1
        assert app.state_machine.current_state is not None
        assert app.input_handler is not None

    def test_update_fetches_data(self, app):
        app.setup()
        mock_data = Mock()
        app.provider.get_data.return_value = mock_data
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_called_once_with(mock_data)

    def test_update_handles_provider_error(self, app):
        app.setup()
        app.provider.get_data.side_effect = Exception("Provider error")
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_not_called()

    def test_update_handles_no_data(self, app):
        app.setup()
        app.provider.get_data.return_value = None
        
        with patch.object(app.state_machine, 'update') as mock_update:
            app._update()
            mock_update.assert_not_called()

    def test_handle_input_delegates(self, app):
        app.setup()
        
        with patch.object(app.input_handler, 'handle_input') as mock_handle:
            app._handle_input()
            mock_handle.assert_called_once()

    def test_handle_input_safe_without_handler(self, app):
        app.input_handler = None
        app._handle_input()

    def test_draw_renders_to_surface(self, app):
        app.setup()
        app.window.surface = Mock()
        
        with patch.object(app.state_machine, 'draw') as mock_draw:
            with patch.object(app.window, 'clear') as mock_clear:
                with patch.object(app.window, 'update_display') as mock_update:
                    app._draw()
                    
                    mock_clear.assert_called_once()
                    mock_draw.assert_called_once_with(app.window.surface)
                    mock_update.assert_called_once()

    def test_draw_skips_if_no_surface(self, app):
        app.setup()
        app.window.surface = None
        
        with patch.object(app.state_machine, 'draw') as mock_draw:
            with patch.object(app.window, 'clear') as mock_clear:
                with patch.object(app.window, 'update_display') as mock_update:
                    app._draw()
                    
                    mock_clear.assert_called_once()
                    mock_draw.assert_not_called()
                    mock_update.assert_called_once()

    @patch('sys.exit')
    def test_run_loop_execution(self, mock_exit, app):
        # Setup property mock to return True then False
        type(app.window).is_running = PropertyMock(side_effect=[True, False])
        
        with patch.object(app, 'setup') as mock_setup:
            with patch.object(app, '_handle_input') as mock_input:
                with patch.object(app, '_update') as mock_update:
                    with patch.object(app, '_draw') as mock_draw:
                        with patch.object(app.window, 'close') as mock_close:
                            app.run()
                            
                            mock_setup.assert_called_once()
                            mock_input.assert_called_once()
                            mock_update.assert_called_once()
                            mock_draw.assert_called_once()
                            mock_close.assert_called_once()
                            mock_exit.assert_called_once()
