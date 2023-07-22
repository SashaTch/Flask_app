import pytest
from flask import url_for

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert response.data == b'username,password'
