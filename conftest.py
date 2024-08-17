import pytest
import sys
import os

@pytest.fixture(autouse=True)
def add_project_root_to_sys_path():
    # Add the root directory of the project to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    yield
    # Optionally, clean up by removing the path after the test
    sys.path.pop(0)
