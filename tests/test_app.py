import pytest
import sys
sys.path.append('../') 
from flask import url_for
from app.main import app
import io

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_img_page(client):
    response = client.get('/img')
    assert response.status_code == 200


def test_manual_page(client):
    response = client.get('/manual')
    assert response.status_code == 200
  

def test_help_page(client):
    response = client.get('/help')
    assert response.status_code == 200


def test_train_page(client):
    response = client.get('/training')
    assert response.status_code == 200


def test_evaluate_answer_image_no_file(client):
    response = client.post('/result/', data={
        'max-marks': '10',
        'checking-type': 'type'
    })
    assert response.status_code == 400


def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200


def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
