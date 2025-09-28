from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_analyze_ok():
    payload = {
        "variable_id": "tavg",
        "region_id": "L1",
        "time_range": {"start": "2023-01-01", "end": "2024-12-31"},
        "options": ["trend", "quality"],
    }
    r = client.post("/analyze", json=payload)
    assert r.status_code == 200
    js = r.json()
    for key in ["mean", "std", "trend_per_decade", "count", "series_sample", "quality"]:
        assert key in js
