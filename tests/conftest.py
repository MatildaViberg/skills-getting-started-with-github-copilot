import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture()
def client():
    """Test client for the FastAPI app"""
    client = TestClient(app_module.app)
    yield client


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test to avoid state leakage."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)
