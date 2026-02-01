import pytest
from unittest.mock import Mock, MagicMock, patch
import pygame
from src.core.app import OverlayApp
from src.core.domain.telemetry_data import TelemetryData

class TestDragDropIntegration:
    @pytest.fixture
    def app(self):
        # Mock dependencies
        mock_window = Mock()
        mock_window.surface = None
        mock_window.is_running = True
        mock_window.handle_events.return_value = [] # Default no events
        
        mock_provider = Mock()
        mock_provider.get_data.return_value = TelemetryData(
            speed=0.0, rpm=0, max_rpm=8000, gear=0,
            throttle_pct=0.0, brake_pct=0.0, clutch_pct=0.0,
            steering_angle=0.0, ffb_level=0.0, timestamp=0.0
        )
        mock_font_provider = Mock()
        mock_config_manager = Mock()
        mock_widget_factory = Mock()
        
        # Configure ConfigManager to return one widget
        mock_config_manager.get_layout.side_effect = lambda key, default=None: [
            {"type": "InputCard", "position_x": 100, "position_y": 100, "width": 300, "height": 100}
        ] if key == "widgets" else {}

        # Configure WidgetFactory to return a real-ish widget (or a mock that behaves like one)
        # We need a real DashboardCard to test DraggableBehavior integration, or at least a Widget with Draggable attached
        # But isolating logic is better. However, integration tests should use as much real code as possible.
        # Let's use real DashboardCard if possible, but mocking pygame might be hard.
        # So we will mock the factory to return a Mock widget that has the real DraggableBehavior logic? 
        # No, simpler: Mock the factory to return a Mock widget, but we manually attach draggable behavior or use a real DashboardCard 
        # and assume headless pygame works (which it usually does for logic).
        
        # Let's try inserting a real DashboardCard but mocking its dependencies
        from src.ui.widgets.input_card import InputCard
        
        # We need to mock InputCardRenderer inside InputCard or it will try to load images/fonts
        # We can do this by patching the import in test setup or mocking the _renderer attribute
        
        real_widget = InputCard(position_x=100, position_y=100)
        # Prevent renderer instantiation
        real_widget._renderer = Mock() 
        # Just in case
        real_widget.draw = Mock() 
        
        mock_widget_factory.create_widget.return_value = real_widget

        app = OverlayApp(
            window=mock_window,
            provider=mock_provider,
            font_provider=mock_font_provider,
            config_manager=mock_config_manager,
            widget_factory=mock_widget_factory
        )
        app.setup() # This puts it in RunningState
        return app

    def test_drag_and_drop_flow(self, app):
        # 1. Switch to EditState (F1)
        f1_event = MagicMock()
        f1_event.type = pygame.KEYDOWN
        f1_event.key = pygame.K_F1
        
        # We inject events via mock_window.handle_events
        app.window.handle_events.return_value = [f1_event]
        
        # Run one loop iteration to process F1
        app._handle_input()
        app._update()
        
        # Verify we are in EditState
        from src.core.application.states.edit_state import EditState
        assert isinstance(app.state_machine.current_state, EditState)
        
        # 2. Drag Widget
        # Widget is at 100, 100. Size 350x130 (default) or 300x100 (from config? factory override config)
        # Our real_widget was init with position_x=100, position_y=100.
        
        # Mouse Down at 110, 110 (inside widget)
        down_event = MagicMock()
        down_event.type = pygame.MOUSEBUTTONDOWN
        down_event.button = 1
        down_event.pos = (110, 110)
        
        # Mouse Motion to 160, 160 (+50, +50)
        motion_event = MagicMock()
        motion_event.type = pygame.MOUSEMOTION
        motion_event.pos = (160, 160)
        motion_event.buttons = (1, 0, 0) # Left button held
        
        # Mouse Up
        up_event = MagicMock()
        up_event.type = pygame.MOUSEBUTTONUP
        up_event.button = 1
        up_event.pos = (160, 160)
        
        # Inject sequence
        app.window.handle_events.return_value = [down_event, motion_event, up_event]
        
        app._handle_input()
        
        # 3. Verify Position Update
        # Initial: 100, 100
        # Drag start: 110, 110. Offset = 100-110 = -10, 100-110 = -10
        # Motion: 160, 160. New Pos = 160 + (-10) = 150.
        # So expected pos is 150, 150.
        
        widget = app.widgets[0]
        assert widget.position_x == 150
        assert widget.position_y == 150
        
        # 4. Save State
        app.save_state()
        
        # 5. Verify Config Manager called with new coords
        args = app.config_manager.set_layout.call_args_list
        # Find call for "widgets"
        widget_call = next(call for call in args if call[0][0] == "widgets")
        assert widget_call[0][1][0]["position_x"] == 150
        assert widget_call[0][1][0]["position_y"] == 150
