import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest.fixture
def app():
    app = FastAPI()
    return app

@pytest.fixture
def client(app):
    return TestClient(app)
