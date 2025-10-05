from conftest import skip_if_no_data
from fastapi.testclient import TestClient

from app.main import app

pytestmark = skip_if_no_data
client = TestClient(app)


def test_meta_variables_has_tmp():
    r = client.get("/meta/variables")
    assert r.status_code == 200
    items = r.json()
    ids = {v["id"] for v in items}
    assert "tmp" in ids and len(items) >= 5


def test_meta_regions_nonempty():
    r = client.get("/meta/regions")
    assert r.status_code == 200
    regions = r.json()
    assert isinstance(regions, list) and len(regions) >= 1
