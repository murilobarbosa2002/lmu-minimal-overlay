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
            "update_interval_ms": 16
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
