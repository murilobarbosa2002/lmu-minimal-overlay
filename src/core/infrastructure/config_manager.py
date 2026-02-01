import json
import os
import threading
from typing import Any, Dict, Optional
from src.core.interfaces.i_config_manager import IConfigManager

class ConfigManager(IConfigManager):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConfigManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._config_file = "config.json"
        self._layout_file = "layout.json"
        
        self._config_data: Dict[str, Any] = {}
        self._layout_data: Dict[str, Any] = {}
        
        self._file_lock = threading.Lock()
        
        
        self._default_config = {
            "version": "1.0.0",
            "update_interval_ms": 16,
            
            "window": {
                "title": "LMU Telemetry Overlay",
                "default_width": 1920,
                "default_height": 1080
            },
            
            "theme": {
                "dashboard_card": {
                    "bg_color": [10, 20, 30, 242],
                    "bg_color_dragging": [25, 35, 50, 180],
                    "text_color": [255, 255, 255],
                    "gear_color": [255, 200, 0],
                    "border_radius": 24,
                    "border_color": [255, 255, 255, 30],
                    "mask_color": [255, 255, 255],
                    "lateral_padding": 20,
                    "width": 350,
                    "height": 130
                },
                
                "steering_indicator": {
                    "radius": 45,
                    "color_rim": [30, 30, 30],
                    "color_marker": [255, 200, 0],
                    "color_center": [50, 50, 50],
                    "tick_start": 30,
                    "tick_end": 150,
                    "tick_step": 10
                },
                
                "bar": {
                    "width": 18,
                    "height": 70,
                    "bg_color": [40, 40, 40],
                    "border_radius": 3,
                    "centerline_color": [100, 100, 100],
                    "padding": 5,
                    "font_size_value": 16,
                    "font_size_label": 14
                },
                
                "indicator_bars": {
                    "spacing": 12,
                    "throttle_color": [0, 255, 0],
                    "brake_color": [255, 0, 0],
                    "ffb_color": [255, 165, 0]
                },
                
                "edit_mode": {
                    "selection_color": [0, 255, 255],
                    "selection_border_width": 2,
                    "selection_border_radius": 8,
                    "padding_min": 8,
                    "padding_max": 12
                }
            },
            
            "defaults": {
                "telemetry": {
                    "speed": 0.0,
                    "rpm": 0,
                    "max_rpm": 8000,
                    "gear": 0,
                    "throttle_pct": 0.0,
                    "brake_pct": 0.0,
                    "clutch_pct": 0.0,
                    "steering_angle": 0.0,
                    "ffb_level": 0.0,
                    "unit": "km/h"
                }
            },
            
            "colors": {
                "ffb_normal": [0, 255, 0],
                "ffb_warning": [255, 255, 0],
                "ffb_clipping": [255, 0, 0]
            },
            
            "thresholds": {
                "ffb_warning": 0.8,
                "ffb_clipping": 0.95
            },
            
            "performance": {
                "fps_target": 60
            }
        }
        
        self._default_layout = {
            "window": {
                "x": 100,
                "y": 100,
                "width": 1920,
                "height": 200,
                "always_on_top": True
            },
            "widgets": []
        }
        
        self._initialized = True
        self.load_config()
        self.load_layout()

    def load_config(self) -> None:
        with self._file_lock:
            if not os.path.exists(self._config_file):
                self._config_data = self._default_config.copy()
                self._save_json(self._config_file, self._config_data)
            else:
                try:
                    with open(self._config_file, 'r') as f:
                        self._config_data = json.load(f)
                except (json.JSONDecodeError, IOError):
                    self._config_data = self._default_config.copy()

    def save_config(self) -> None:
        with self._file_lock:
            self._save_json(self._config_file, self._config_data)

    def load_layout(self) -> None:
        with self._file_lock:
            if not os.path.exists(self._layout_file):
                self._layout_data = self._default_layout.copy()
                self._save_json(self._layout_file, self._layout_data)
            else:
                try:
                    with open(self._layout_file, 'r') as f:
                        self._layout_data = json.load(f)
                except (json.JSONDecodeError, IOError):
                    self._layout_data = self._default_layout.copy()

    def save_layout(self) -> None:
        with self._file_lock:
            self._save_json(self._layout_file, self._layout_data)

    def get_config(self, key: str, default: Any = None) -> Any:
        return self._config_data.get(key, default)

    def set_config(self, key: str, value: Any) -> None:
        self._config_data[key] = value
        self.save_config()

    def get_layout(self, key: str, default: Any = None) -> Any:
        return self._layout_data.get(key, default)

    def set_layout(self, key: str, value: Any) -> None:
        self._layout_data[key] = value
        self.save_layout()

    def _save_json(self, filename: str, data: Dict[str, Any]) -> None:
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError:
            pass
    
    def get_theme(self, widget_name: str) -> Dict[str, Any]:
        theme = self._config_data.get("theme", {})
        return theme.get(widget_name, {})
    
    def get_defaults(self, category: str) -> Dict[str, Any]:
        defaults = self._config_data.get("defaults", {})
        return defaults.get(category, {})
