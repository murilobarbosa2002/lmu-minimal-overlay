import pytest
from unittest.mock import Mock, patch
from src.core.app import OverlayApp
from src.core.application.states.running_state import RunningState

class TestOverlayApp:
    @pytest.fixture
    def app(self):
        with patch('src.core.app.WindowManager') as mock_wm, \
             patch('src.core.app.MockTelemetryProvider') as mock_provider, \
             patch('src.core.app.StateMachine') as mock_sm, \
             patch('src.core.app.Speedometer') as mock_speedo, \
             patch('src.core.app.RunningState'), \
             patch('src.core.app.EditState'), \
             patch('src.core.app.InputHandler') as mock_input:
            
            app = OverlayApp()
            app.window = mock_wm.return_value
            app.provider = mock_provider.return_value
            app.state_machine = mock_sm.return_value
            app.input_handler = mock_input.return_value
            return app

    def test_setup_initializes_components(self, app):
        app.setup()
        app.window.init.assert_called_once()
        assert len(app.widgets) == 1
        app.state_machine.change_state.assert_called_once()
        assert app.input_handler is not None

    def test_update_fetches_data(self, app):
        mock_data = Mock()
        app.provider.get_data.return_value = mock_data
        
        app._update()
        
        app.provider.get_data.assert_called_once()
        app.state_machine.update.assert_called_with(mock_data)

    def test_update_handles_provider_error(self, app):
        app.provider.get_data.side_effect = Exception("Connection lost")
        
        # Should not raise exception
        app._update()
        
        app.state_machine.update.assert_not_called()

    def test_update_handles_no_data(self, app):
        app.provider.get_data.return_value = None
        
        app._update()
        
        app.state_machine.update.assert_not_called()

    def test_handle_input_delegates(self, app):
        # Setup mock input handler manually if needed, or rely on fixture
        app.input_handler = Mock()
        
        app._handle_input()
        
        app.input_handler.handle_input.assert_called_once()

    def test_handle_input_safe_without_handler(self, app):
        app.input_handler = None
        # Should run without error
        app._handle_input()

    def test_draw_renders_to_surface(self, app):
        mock_surface = Mock()
        app.window.surface = mock_surface
        
        app._draw()
        
        app.window.clear.assert_called_once()
        app.state_machine.draw.assert_called_with(mock_surface)
        app.window.update_display.assert_called_once()

    def test_draw_skips_if_no_surface(self, app):
        app.window.surface = None
        
        app._draw()
        
        app.window.clear.assert_called_once()
        app.state_machine.draw.assert_not_called()
        app.window.update_display.assert_called_once()

    def test_run_loop(self, app):
        # Mock window running sequence: True -> False
        type(app.window).is_running = PropertyMock(side_effect=[True, False])
        
        with patch.object(app, 'setup') as mock_setup, \
             patch.object(app, '_handle_input') as mock_input, \
             patch.object(app, '_update') as mock_update, \
             patch.object(app, '_draw') as mock_draw, \
             patch('sys.exit') as mock_exit:
            
            app.run()
            
            mock_setup.assert_called_once()
            mock_input.assert_called_once()
            mock_update.assert_called_once()
            mock_draw.assert_called_once()
            app.window.close.assert_called_once()
            mock_exit.assert_called_once()

from unittest.mock import PropertyMock
