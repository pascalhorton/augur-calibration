import pandas as pd

import augur.core as core
import pytest


def test_get_default_cn_parameters_shape():
    assert core.get_default_cn_parameters().shape == (5, 4)


def test_get_default_cn_parameters_values():
    assert core.get_default_cn_parameters().iloc[0, 0] == 67
    assert core.get_default_cn_parameters().iloc[0, 3] == 86
    assert core.get_default_cn_parameters().iloc[4, 3] == 25
    assert core.get_default_cn_parameters().iloc[4, 0] == 8


def test_get_default_cn_parameters_index():
    assert core.get_default_cn_parameters().index[0] == 'farmland'
    assert core.get_default_cn_parameters().index[1] == 'pasture'
    assert core.get_default_cn_parameters().index[2] == 'forest'
    assert core.get_default_cn_parameters().index[3] == 'settlement'
    assert core.get_default_cn_parameters().index[4] == 'debris'


def test_get_default_cn_parameters_columns():
    assert core.get_default_cn_parameters().columns[0] == 'A'
    assert core.get_default_cn_parameters().columns[1] == 'B'
    assert core.get_default_cn_parameters().columns[2] == 'C'
    assert core.get_default_cn_parameters().columns[3] == 'D'


def test_compute_cn_factor_from_classic_land_cover_types():
    cns = core.get_default_cn_parameters()
    catchment = {'cover_farmland': 40, 'cover_pasture': 50, 'cover_forest': 5,
                 'cover_settlement': 5, 'cover_bare': 0, 'cover_cryo': 0}
    assert core.compute_cn_factor(catchment, cns, 'A') == pytest.approx(60, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'B') == pytest.approx(73, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'C') == pytest.approx(82, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'D') == pytest.approx(85, abs=0.5)


def test_compute_cn_factor_from_classic_land_cover_types_other_values():
    cns = core.get_default_cn_parameters()
    catchment = {'cover_farmland': 35, 'cover_pasture': 30, 'cover_forest': 15,
                 'cover_settlement': 20, 'cover_bare': 0, 'cover_cryo': 0}
    assert core.compute_cn_factor(catchment, cns, 'A') == pytest.approx(62, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'B') == pytest.approx(75, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'C') == pytest.approx(83, abs=0.5)
    assert core.compute_cn_factor(catchment, cns, 'D') == pytest.approx(86, abs=0.5)


def test_get_rain_area():
    assert core.get_rain_area(100) == pytest.approx(28, abs=0.5)
    assert core.get_rain_area(5) == pytest.approx(67, abs=0.5)
    assert core.get_rain_area(250) == pytest.approx(22, abs=0.5)


def test_get_rain_area_with_invalid_input():
    with pytest.raises(ValueError):
        core.get_rain_area(0)
    with pytest.raises(ValueError):
        core.get_rain_area(-1)


def test_get_production():
    assert core.get_production(38, 140, 61.9) == pytest.approx(23, abs=0.5)
    assert core.get_production(38, 221, 61.9) == pytest.approx(36, abs=0.5)
    assert core.get_production(38, 287, 61.9) == pytest.approx(47, abs=0.5)


def test_get_time_to_peak():
    assert core.get_time_to_peak(5000, 0.08, 120) == pytest.approx(1.37, abs=0.01)
    assert core.get_time_to_peak(5000, 0.23, 120) == pytest.approx(1.25, abs=0.01)
    assert core.get_time_to_peak(3500, 0.78, 120) == pytest.approx(1.12, abs=0.01)


def test_get_time_to_peak_with_invalid_input():
    with pytest.raises(ValueError):
        core.get_time_to_peak(0, 0.08, 120)
    with pytest.raises(ValueError):
        core.get_time_to_peak(-1, 0.08, 120)
    with pytest.raises(ValueError):
        core.get_time_to_peak(5000, -1, 120)
    with pytest.raises(ValueError):
        core.get_time_to_peak(5000, 0.08, 0)
    with pytest.raises(ValueError):
        core.get_time_to_peak(5000, 0.08, -1)


def test_get_unit_peakflow():
    assert core.get_unit_peakflow(250, 1.1179) == pytest.approx(46.52, abs=0.01)
    assert core.get_unit_peakflow(500, 1.2242) == pytest.approx(84.96, abs=0.01)


def test_get_unit_peakflow_with_invalid_input():
    with pytest.raises(ValueError):
        core.get_unit_peakflow(0, 1.1179)
    with pytest.raises(ValueError):
        core.get_unit_peakflow(-1, 1.1179)
    with pytest.raises(ValueError):
        core.get_unit_peakflow(250, 0)
    with pytest.raises(ValueError):
        core.get_unit_peakflow(250, -1)


def test_get_unit_hydrograph():
    q_uh = core.get_unit_hydrograph(84.96)
    assert q_uh[0] == pytest.approx(0, abs=0.01)
    assert q_uh[3] == pytest.approx(25.49, abs=0.01)
    assert q_uh[6] == pytest.approx(50.97, abs=0.01)
    assert q_uh[10] == pytest.approx(84.96, abs=0.01)
    assert q_uh[12] == pytest.approx(76.46, abs=0.01)
    assert q_uh[27] == pytest.approx(12.74, abs=0.01)
