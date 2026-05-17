import pytest
import requests

BASE_URL = "http://localhost:8000"


@pytest.mark.smoke

def test_home_responde():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200


@pytest.mark.smoke

def test_healthcheck():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code in [200, 404]