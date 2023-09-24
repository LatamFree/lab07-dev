import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from src.main import app

# Mock the Settings class to provide test values
class TestSettings:
    def __init__(self):
        self.REST_COUNTRIES_BASE_URL = "https://restcountries.com"
        self.WEATHER_BASE_URL = "https://weatherapi.com"
        self.WEATHERAPI_KEY = "a17f88dd2c9b48119f3134314232209"

@pytest.fixture
def test_client():
    client = TestClient(app)
    return client

@patch('src.config.get_settings', Mock(return_value=TestSettings()))
def test_get_south_america(test_client):
    response = test_client.get("/all")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert all(key in item for key in ("name", "cca2", "cca3", "currency", "capital", "flag_url"))

@patch('src.config.get_settings', Mock(return_value=TestSettings()))
def test_get_capital_weather(test_client):
    response = test_client.get("/countries/CL")
    assert response.status_code == 200
    data = response.json()
    
    assert all(key in data for key in ("name", "cca2", "cca3", "currency", "capital", "flag_url", "weather"))
  
    assert all(key in data["weather"] for key in ("location", "days"))
    for item in data["weather"]["days"]:
        assert all(key in item for key in ("date", "condition"))

@patch('src.config.get_settings', Mock(return_value=TestSettings()))
def test_get_south_america_error(test_client):
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404  
        mock_get.return_value = mock_response

        response = test_client.get("/all")
        assert response.status_code == 200  
        data = response.json()
        assert "message" in data 

@patch('src.config.get_settings', Mock(return_value=TestSettings()))
def test_get_capital_weather_error(test_client):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404 
        mock_get.return_value = mock_response

        response = test_client.get("/countries/CL") 
        assert response.status_code == 200  
        data = response.json()
        assert "message" in data

@patch('src.config.get_settings', Mock(return_value=TestSettings()))
def test_get_capital_weather_error2(test_client):
    with patch('requests.get') as mock_get:
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {
            "name": {"common": "Chile"},
            "capital": ["Santiago"],
            "currencies": {"CLP": {"name": "Peso Chileno"}},
            "flags": {"png": "https://example.com/cl-flag.png"},
            "cca2": "CL",
            "cca3": "CL"
        }

        mock_response = Mock()
        mock_response.status_code = 404 
        mock_get.side_effect = [mock, mock_response]

        response = test_client.get("/countries/CL") 
        assert response.status_code == 200  
        data = response.json()
        assert "message" in data