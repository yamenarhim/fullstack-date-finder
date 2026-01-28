from fastapi.testclient import TestClient

def test_get_weekday_endpoint(client: TestClient):
    response = client.get("/api/v1/dates/weekday", params={"year": 2025, "month": 1, "day": 15})
    assert response.status_code == 200
    data = response.json()
    assert data["weekday_name"] == "Wednesday"
    assert data["weekday_number"] == 2

def test_get_weekday_validation_error(client: TestClient):
    # Test invalid month (13)
    response = client.get("/api/v1/dates/weekday", params={"year": 2025, "month": 13})
    assert response.status_code == 422  # Validation Error

def test_get_weekday_invalid_date_logic(client: TestClient):
    # Test Feb 30th (Valid types, but invalid calendar date)
    response = client.get("/api/v1/dates/weekday", params={"year": 2025, "month": 2, "day": 30})
    assert response.status_code == 400
    assert "day is out of range" in response.json()["detail"]

def test_mid_saturdays_endpoint(client: TestClient):
    response = client.get(
        "/api/v1/dates/mid-saturdays", 
        params={"start_date": "2026-01-01", "end_date": "2026-12-31"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["saturday_count"] == 1
    assert data["start_date"] == "2026-01-01"

def test_mid_saturdays_date_order_error(client: TestClient):
    # End date before start date
    response = client.get(
        "/api/v1/dates/mid-saturdays", 
        params={"start_date": "2026-12-31", "end_date": "2026-01-01"}
    )
    # This returns 422 because our Pydantic validator catches it
    assert response.status_code == 422