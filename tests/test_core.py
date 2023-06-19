import numpy as np
import pandas as pd
import pytest

import augur.core as agc


def test_get_default_cn_parameters_shape():
    assert agc.get_default_cn_parameters().shape == (5, 4)


def test_get_default_cn_parameters_values():
    assert agc.get_default_cn_parameters().iloc[0, 0] == 67
    assert agc.get_default_cn_parameters().iloc[0, 3] == 86
    assert agc.get_default_cn_parameters().iloc[4, 3] == 25
    assert agc.get_default_cn_parameters().iloc[4, 0] == 8


def test_get_default_cn_parameters_index():
    assert agc.get_default_cn_parameters().index[0] == 'farmland'
    assert agc.get_default_cn_parameters().index[1] == 'pasture'
    assert agc.get_default_cn_parameters().index[2] == 'forest'
    assert agc.get_default_cn_parameters().index[3] == 'settlement'
    assert agc.get_default_cn_parameters().index[4] == 'debris'


def test_get_default_cn_parameters_columns():
    assert agc.get_default_cn_parameters().columns[0] == 'A'
    assert agc.get_default_cn_parameters().columns[1] == 'B'
    assert agc.get_default_cn_parameters().columns[2] == 'C'
    assert agc.get_default_cn_parameters().columns[3] == 'D'


def test_compute_cn_factor_from_classic_land_cover_types():
    cns = agc.get_default_cn_parameters()
    catchment = {'cover_farmland': 40, 'cover_pasture': 50, 'cover_forest': 5,
                 'cover_settlement': 5, 'cover_bare': 0, 'cover_cryo': 0}
    assert agc.compute_cn_factor(catchment, cns, 'A') == pytest.approx(60, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'B') == pytest.approx(73, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'C') == pytest.approx(82, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'D') == pytest.approx(85, abs=0.5)


def test_compute_cn_factor_from_classic_land_cover_types_other_values():
    cns = agc.get_default_cn_parameters()
    catchment = {'cover_farmland': 35, 'cover_pasture': 30, 'cover_forest': 15,
                 'cover_settlement': 20, 'cover_bare': 0, 'cover_cryo': 0}
    assert agc.compute_cn_factor(catchment, cns, 'A') == pytest.approx(62, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'B') == pytest.approx(75, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'C') == pytest.approx(83, abs=0.5)
    assert agc.compute_cn_factor(catchment, cns, 'D') == pytest.approx(86, abs=0.5)


def test_get_rain_area():
    assert agc.get_rain_area(100) == pytest.approx(28, abs=0.5)
    assert agc.get_rain_area(5) == pytest.approx(67, abs=0.5)
    assert agc.get_rain_area(250) == pytest.approx(22, abs=0.5)


def test_get_rain_area_with_invalid_input():
    with pytest.raises(ValueError):
        agc.get_rain_area(0)
    with pytest.raises(ValueError):
        agc.get_rain_area(-1)


def test_get_production():
    assert agc.get_production(38, 140, 61.9) == pytest.approx(23, abs=0.5)
    assert agc.get_production(38, 221, 61.9) == pytest.approx(36, abs=0.5)
    assert agc.get_production(38, 287, 61.9) == pytest.approx(47, abs=0.5)


def test_get_time_to_peak():
    assert agc.get_time_to_peak(5000, 0.08, 120) == pytest.approx(1.37, abs=0.01)
    assert agc.get_time_to_peak(5000, 0.23, 120) == pytest.approx(1.25, abs=0.01)
    assert agc.get_time_to_peak(3500, 0.78, 120) == pytest.approx(1.12, abs=0.01)


def test_get_time_to_peak_with_invalid_input():
    with pytest.raises(ValueError):
        agc.get_time_to_peak(0, 0.08, 120)
    with pytest.raises(ValueError):
        agc.get_time_to_peak(-1, 0.08, 120)
    with pytest.raises(ValueError):
        agc.get_time_to_peak(5000, -1, 120)
    with pytest.raises(ValueError):
        agc.get_time_to_peak(5000, 0.08, 0)
    with pytest.raises(ValueError):
        agc.get_time_to_peak(5000, 0.08, -1)


def test_get_unit_peakflow():
    assert agc.get_unit_peakflow(250, 1.1179) == pytest.approx(46.52, abs=0.01)
    assert agc.get_unit_peakflow(500, 1.2242) == pytest.approx(84.96, abs=0.01)


def test_get_unit_peakflow_with_invalid_input():
    with pytest.raises(ValueError):
        agc.get_unit_peakflow(0, 1.1179)
    with pytest.raises(ValueError):
        agc.get_unit_peakflow(-1, 1.1179)
    with pytest.raises(ValueError):
        agc.get_unit_peakflow(250, 0)
    with pytest.raises(ValueError):
        agc.get_unit_peakflow(250, -1)


def test_get_unit_hydrograph():
    t_uh, q_uh = agc.get_unit_hydrograph(84.96, 1.2242)

    assert q_uh[0] == pytest.approx(0, abs=0.01)
    assert q_uh[3] == pytest.approx(25.49, abs=0.01)
    assert q_uh[6] == pytest.approx(50.97, abs=0.01)
    assert q_uh[10] == pytest.approx(84.96, abs=0.01)
    assert q_uh[12] == pytest.approx(76.46, abs=0.01)
    assert q_uh[27] == pytest.approx(12.74, abs=0.01)

    assert t_uh[0] == pytest.approx(0, abs=0.01)
    assert t_uh[3] == pytest.approx(0.37, abs=0.01)
    assert t_uh[6] == pytest.approx(0.73, abs=0.01)
    assert t_uh[10] == pytest.approx(1.22, abs=0.01)
    assert t_uh[12] == pytest.approx(1.47, abs=0.01)
    assert t_uh[27] == pytest.approx(3.31, abs=0.01)


def test_get_unit_discharge():
    time_steps = np.arange(0, 5, 0.5)
    q_uh = agc.get_unit_discharge(time_steps, 84.96, 1.2242)

    assert q_uh[0] == 0
    assert 33 < q_uh[1] < 35
    assert 68 < q_uh[2] < 70
    assert 72 < q_uh[3] < 76
    assert 55 < q_uh[4] < 59
    assert q_uh[8] == 0


def test_get_hyetogram_with_4_time_steps():
    hyetogram = agc.get_hyetogram(4, 23.1)
    assert hyetogram[0] == pytest.approx(4.1, abs=0.1)
    assert hyetogram[1] == pytest.approx(10.6, abs=0.1)
    assert hyetogram[2] == pytest.approx(5.3, abs=0.1)
    assert hyetogram[3] == pytest.approx(3.0, abs=0.1)

    hyetogram = agc.get_hyetogram(4, 47.3)
    assert hyetogram[0] == pytest.approx(8.5, abs=0.1)
    assert hyetogram[1] == pytest.approx(21.8, abs=0.1)
    assert hyetogram[2] == pytest.approx(10.9, abs=0.1)
    assert hyetogram[3] == pytest.approx(6.1, abs=0.1)


def test_get_hyetogram_with_8_time_steps():
    hyetogram = agc.get_hyetogram(8, 23.1)
    assert hyetogram[0] == pytest.approx(4.1 / 2, abs=0.1)
    assert hyetogram[1] == pytest.approx(4.1 / 2, abs=0.1)
    assert hyetogram[2] == pytest.approx(10.6 / 2, abs=0.1)
    assert hyetogram[3] == pytest.approx(10.6 / 2, abs=0.1)
    assert hyetogram[4] == pytest.approx(5.3 / 2, abs=0.1)
    assert hyetogram[5] == pytest.approx(5.3 / 2, abs=0.1)
    assert hyetogram[6] == pytest.approx(3.0 / 2, abs=0.1)
    assert hyetogram[7] == pytest.approx(3.0 / 2, abs=0.1)

    hyetogram = agc.get_hyetogram(8, 47.3)
    assert hyetogram[0] == pytest.approx(8.5 / 2, abs=0.1)
    assert hyetogram[1] == pytest.approx(8.5 / 2, abs=0.1)
    assert hyetogram[2] == pytest.approx(21.8 / 2, abs=0.1)
    assert hyetogram[3] == pytest.approx(21.8 / 2, abs=0.1)
    assert hyetogram[4] == pytest.approx(10.9 / 2, abs=0.1)
    assert hyetogram[5] == pytest.approx(10.9 / 2, abs=0.1)
    assert hyetogram[6] == pytest.approx(6.1 / 2, abs=0.1)
    assert hyetogram[7] == pytest.approx(6.1 / 2, abs=0.1)


def test_get_hyetogram_constant_with_8_time_steps():
    hyetogram = agc.get_hyetogram(8, 23.1)
    assert hyetogram[0] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[1] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[2] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[3] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[4] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[5] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[6] == pytest.approx(23.1 / 8, abs=0.1)
    assert hyetogram[7] == pytest.approx(23.1 / 8, abs=0.1)


def test_peak_discharge():
    cns = agc.get_default_cn_parameters()
    catchment = pd.Series(
        {'area': 100, 'slope_gradient': 0.08, 'length_watercourse': 5000,
         'cover_farmland': 40, 'cover_forest': 5, 'cover_pasture': 50,
         'cover_settlement': 5, 'cover_bare': 0, 'cover_water': 0,
         'cover_cryo': 0, 'p10': 140, 'p30': 221, 'p100': 287})
    time, hydrograph = agc.compute_hydrograph(catchment, 'A', catchment, cns)

    peak_discharge = hydrograph.max(axis=0)

    # Compare with a 6% tolerance due to different ways of computing
    assert peak_discharge[0] == pytest.approx(170, rel=0.06)
    assert peak_discharge[1] == pytest.approx(268, rel=0.06)
    assert peak_discharge[2] == pytest.approx(348, rel=0.06)
