import pytest
import sys
from fastapi.testclient import TestClient
from api.main import app
sys.path.append('../')

client = TestClient(app)

def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Welcome To": "Smart Answer Evaluator"}

def test_predict():
    payload = {
        "ideal": "This is an ideal answer.",
        "student": "This is a student's answer."
    }
    response = client.post('/', json=payload)
    assert response.status_code == 200
    
    response_data = response.json()
    assert "proba" in response_data
    assert "idx" in response_data
