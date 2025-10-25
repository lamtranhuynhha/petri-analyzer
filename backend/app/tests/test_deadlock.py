from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_deadlock_api():
    data = {
        "places": ["p1", "p2"],
        "transitions": ["t1"],
        "arcs": [["p1", "t1"], ["t1", "p2"]],
        "weights": [
            {"arc": ["p1", "t1"], "weight": 1},
            {"arc": ["t1", "p2"], "weight": 1}
        ],
        "initial_marking": {"p1": 1, "p2": 0}
    }

    response = client.post("/analyze/deadlock", json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    result = response.json()
    assert result["total_deadlocks"] == 1
