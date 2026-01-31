import pytest
from unittest.mock import patch, Mock


def test_main_module_exists():
    import src.main
    assert hasattr(src.main, 'AppFactory')
