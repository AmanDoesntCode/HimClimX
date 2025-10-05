from fastapi.testclient import TestClient

from app.main import app

from .conftest import skip_if_no_data

pytestmark = skip_if_no_data
client = TestClient(app)


def test_analyze_tmp_w2000_1990_1995():
    payload = {
        "variable_id": "tmp",
        "region_id": "W2000",
        "time_range": {"start": "1990-01-01", "end": "1995-12-31"},
        "options": ["trend", "quality"],
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["count"] == 72
    assert isinstance(data["mean"], (int, float))
    assert "overall" in data["quality"]
