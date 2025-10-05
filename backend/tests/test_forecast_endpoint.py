from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_forecast_tmp_w2000_3y():
    payload = {"variable_id": "tmp", "region_id": "W2000", "horizon_years": 3}
    r = client.post("/forecast", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    pts = data["points"]
    # Prophet returns monthly; allow 35-37 to avoid edge off-by-one with month starts
    assert 35 <= len(pts) <= 37
    one = pts[0]
    for k in ["date", "yhat", "yhat_lower", "yhat_upper"]:
        assert k in one
