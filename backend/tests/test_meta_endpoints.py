from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_variables():
    r = client.get("/meta/variables")
    assert r.status_code == 200
    js = r.json()
    assert isinstance(js, list) and len(js) >= 1
    assert {"id", "name"} <= set(js[0].keys())


def test_get_regions():
    r = client.get("/meta/regions")
    assert r.status_code == 200
    js = r.json()
    assert isinstance(js, list) and len(js) >= 1
    assert {"id", "name"} <= set(js[0].keys())
