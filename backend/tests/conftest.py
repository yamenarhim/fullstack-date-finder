import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    """
    Create a TestClient instance.
    The 'with' context manager triggers the lifespan (startup/shutdown) events,
    which is important because we initialized the Cache in lifespan.
    """
    with TestClient(app) as c:
        yield c