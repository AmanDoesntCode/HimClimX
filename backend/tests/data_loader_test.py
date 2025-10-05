from datetime import date

import numpy as np

from app.services.data_loader import list_available_variables, monthly_region_series

from .conftest import skip_if_no_data

pytestmark = skip_if_no_data


def test_list_available_variables_nonempty():
    ids = list_available_variables()
    assert "tmp" in ids
    assert len(ids) >= 5


def test_monthly_series_tmp_w2000_shape():
    s = monthly_region_series("tmp", "W2000", (date(1990, 1, 1), date(1995, 12, 31)))
    assert len(s) == 72
    assert np.isfinite(s.iloc[:5].values.astype(float)).all()
