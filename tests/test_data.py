import pandas as pd

import augur.data as data
import pytest


def test_reclassify_slope_gradients():
    catchment = pd.DataFrame({'slope_gradient': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]})
    assert data.reclassify_slope_gradients(catchment).iloc[0, 0] == 0.08
    assert data.reclassify_slope_gradients(catchment).iloc[1, 0] == 0.08
    assert data.reclassify_slope_gradients(catchment).iloc[2, 0] == 0.3
    assert data.reclassify_slope_gradients(catchment).iloc[3, 0] == 0.3
    assert data.reclassify_slope_gradients(catchment).iloc[4, 0] == 0.3
    assert data.reclassify_slope_gradients(catchment).iloc[5, 0] == 0.3
    assert data.reclassify_slope_gradients(catchment).iloc[6, 0] == 0.7
    assert data.reclassify_slope_gradients(catchment).iloc[7, 0] == 0.7

