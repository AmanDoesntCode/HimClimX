from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_forecast_ok():
    payload = {"variable_id": "tavg", "region_id": "L1", "horizon_years": 3}
    r = client.post("/forecast", json=payload)
    assert r.status_code == 200
    js = r.json()
    assert "points" in js and len(js["points"]) == 3
    assert {"date", "yhat"} <= set(js["points"][0].keys())
