import pytest
from app import app
from utils import calculate_internal_metric
from database import get_users


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Test 1: Home route returns 200
def test_home_status_code(client):
    response = client.get("/")
    assert response.status_code == 200


# Test 2: Home route returns JSON with expected message
def test_home_returns_json_message(client):
    response = client.get("/")
    data = response.get_json()
    assert data["message"] == "Internal Utility Service Running"


# Test 3: Home route JSON contains environment key
def test_home_contains_environment(client):
    response = client.get("/")
    data = response.get_json()
    assert "environment" in data


# Test 4: Users route returns 200
def test_users_status_code(client):
    response = client.get("/users")
    assert response.status_code == 200


# Test 5: Users route returns a list
def test_users_returns_list(client):
    response = client.get("/users")
    data = response.get_json()
    assert isinstance(data, list)


# Test 6: Users list is not empty
def test_users_list_not_empty(client):
    response = client.get("/users")
    data = response.get_json()
    assert len(data) > 0


# Test 7: calculate_internal_metric returns correct result
def test_calculate_internal_metric_basic():
    result = calculate_internal_metric(10, 2)
    assert result == 5.0


# Test 8: get_users returns list with at least one user having an 'id' key
def test_get_users_returns_valid_structure():
    users = get_users()
    assert isinstance(users, list)
    assert "id" in users[0]
