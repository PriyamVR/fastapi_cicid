from fastapi.testclient import TestClient
from src.main import api, tickets



client = TestClient(api)

def setup_function():
    tickets.clear()

def test_root_welcome_message():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Message": "Welcome to the Ticket Booking System"}

def test_get_tickets_initially_empty():
    resp = client.get("/ticket")
    assert resp.status_code == 200
    assert resp.json() == []

def test_add_ticket_then_list_contains_it():
    payload = {
        "id": 1,
        "flight_name": "BG-101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Chattogram"
    }
    resp = client.post("/ticket", json=payload)
    assert resp.status_code == 200
    assert resp.json() == payload

    resp2 = client.get("/ticket")
    assert resp2.status_code == 200
    assert resp2.json() == [payload]

def test_update_existing_ticket():
    original = {
        "id": 1,
        "flight_name": "BG-101",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Chattogram"
    }
    client.post("/ticket", json=original)

    updated = {
        "id": 1,
        "flight_name": "BG-202",
        "flight_date": "2025-10-16",
        "flight_time": "09:00",
        "destination": "Dhaka"
    }
    resp = client.put("/ticket/1", json=updated)
    assert resp.status_code == 200
    assert resp.json() == updated

    resp2 = client.get("/ticket")
    assert resp2.status_code == 200
    assert resp2.json() == [updated]

def test_update_non_existing_ticket_returns_error():
    updated = {
        "id": 99,
        "flight_name": "XX-999",
        "flight_date": "2025-12-31",
        "flight_time": "23:59",
        "destination": "Nowhere"
    }
    resp = client.put("/ticket/99", json=updated)
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict) and body.get("error") == "Ticket Not Found"

def test_delete_existing_ticket():
    t = {
        "id": 5,
        "flight_name": "BG-555",
        "flight_date": "2025-11-01",
        "flight_time": "07:45",
        "destination": "Sylhet"
    }
    client.post("/ticket", json=t)

    resp = client.delete("/ticket/5")
    assert resp.status_code == 200
    assert resp.json() == t

    resp2 = client.get("/ticket")
    assert resp2.status_code == 200
    assert resp2.json() == []

def test_delete_non_existing_ticket_returns_error():
    resp = client.delete("/ticket/12345")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict) and body.get("error") == "Ticket not found, deletion failed"
