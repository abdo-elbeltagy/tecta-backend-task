from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stock_api():
    response = client.get("/api/stats?ticker=MSFT&start=2023-01-01&end=2023-01-31")
    assert response.status_code == 200
    data = response.json()
    assert "high" in data
    assert "low" in data
    assert "average" in data
    assert "last_close" in data
