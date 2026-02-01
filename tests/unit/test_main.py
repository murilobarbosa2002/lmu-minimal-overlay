import pytest
from unittest.mock import patch, Mock
import runpy
import sys


def test_main_module_exists():
    import src.main

    assert hasattr(src.main, "AppFactory")


def test_main_execution():
    """Verify main block execution using runpy"""
    # Clean up sys.modules to avoid RuntimeWarning from runpy
    if "src.main" in sys.modules:
        del sys.modules["src.main"]

    with patch("src.core.infrastructure.app_factory.AppFactory.create") as mock_create:
        mock_app = Mock()
        mock_create.return_value = mock_app

        # Run the module
        runpy.run_module("src.main", run_name="__main__")

        mock_create.assert_called_once()
        mock_app.run.assert_called_once()
