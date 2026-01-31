import pytest
from unittest.mock import patch, Mock
import runpy
import sys

def test_main_execution():
    """Test that main.py initializes and runs OverlayApp"""
    with patch('src.core.app.OverlayApp') as mock_app_cls:
        mock_app_instance = Mock()
        mock_app_cls.return_value = mock_app_instance
        
        # We can't easily test the if __name__ == "__main__" block via import
        # so we will use runpy to execute it as a script
        
        with patch.object(sys, 'argv', ['src.main']):
            runpy.run_module('src.main', run_name='__main__')
        
        mock_app_cls.assert_called_once()
        mock_app_instance.run.assert_called_once()
