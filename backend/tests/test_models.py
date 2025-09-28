from datetime import date

from app.api.models import AnalyzeRequest, Region, TimeRange, Variable


def test_models_parse():
    v = Variable(id="tavg", name="Average Temperature", units="°C")
    r = Region(id="L1", name="Ladakh", bbox=(76.0, 32.0, 79.5, 35.2))
    tr = TimeRange(start=date(2023, 1, 1), end=date(2024, 12, 31))
    req = AnalyzeRequest(variable_id=v.id, region_id=r.id, time_range=tr)
    assert req.variable_id == "tavg"
