from fastapi.testclient import TestClient

from app.main import app

from .conftest import skip_if_no_data

pytestmark = skip_if_no_data
client = TestClient(app)


def test_forecast_tmp_w2000_3y():
    payload = {"variable_id": "tmp", "region_id": "W2000", "horizon_years": 3}
    r = client.post("/forecast", json=payload)
    assert r.status_code == 200, r.text
    pts = r.json()["points"]
    assert 35 <= len(pts) <= 37
    one = pts[0]
    for k in ["date", "yhat", "yhat_lower", "yhat_upper"]:
        assert k in one
