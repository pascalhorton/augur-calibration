import math
import pandas as pd
import numpy as np


def get_default_cn_parameters(version='redcross'):
    """
    Get the default curve number parameters.

    Parameters
    ----------
    version: str
        Selection of the parameter sets: 'redcross' or 'augur'

    Returns
    -------
    A dataframe with the default curve number parameters.
    """

    cns = None
    land_covers = ['farmland', 'pasture', 'forest', 'settlement', 'debris']

    if version == 'redcross':
        cns = pd.DataFrame(np.array([[67, 76, 83, 86],
                                     [54, 70, 80, 84],
                                     [35, 61, 74, 80],
                                     [85, 90, 92, 94],
                                     [8, 10, 15, 25]]),
                           columns=['A', 'B', 'C', 'D'])
        cns.index = land_covers

    elif version == 'augur':
        cns = pd.DataFrame(np.array([[35, 40, 43, 46],
                                     [37, 37, 40, 82],
                                     [20, 48, 70, 100],
                                     [59, 73, 100, 60],
                                     [8, 10, 15, 25]]),
                           columns=['A', 'B', 'C', 'D'])
        cns.index = land_covers

    else:
        raise ValueError(f"Unknown CN version: {version}.")

    return cns


def compute_cn_factor(catchment, cns, soil_type):
    """
    Compute the curve number factor by combining the different land covers for a given
    soil type.

    Parameters
    ----------
    catchment: Pandas dataframe
        Dataframe containing the land cover percentages.
    cns: Pandas dataframe
        Dataframe containing the curve number values for all land covers and soil types.
    soil_type: str
        The soil type category.

    Returns
    -------
    The curve number factor for the different land covers for a given soil type.
    """
    cn = catchment['cover_farmland'] / 100 * cns.at['farmland', soil_type] + \
         catchment['cover_pasture'] / 100 * cns.at['pasture', soil_type] + \
         catchment['cover_forest'] / 100 * cns.at['forest', soil_type] + \
         catchment['cover_settlement'] / 100 * cns.at['settlement', soil_type] + \
         (catchment['cover_bare'] + catchment['cover_cryo']) / 100 * \
         cns.at['debris', soil_type]

    return cn


def get_rain_area(area, a=106.61, x=-0.289):
    """
    Compute the rainfall area.

    Parameters
    ----------
    area: float
        The catchment area [km2].
    a: float
        A multiplicative parameter a.
    x: float
        An exponent parameter x.

    Returns
    -------
    The rainfall area [%].
    """
    if area <= 0:
        raise ValueError("The catchment area cannot be null or negative.")

    return a * math.pow(area, x)


def get_production(area_rain, precipitation, cn_factor, a=0.7):
    """
    Compute the precipitation relevant for runoff.

    Parameters
    ----------
    area_rain: float
        The rainfall area [%].
    precipitation: float
        The precipitation [mm].
    cn_factor: float
        The curve number factor.
    a: float
        A multiplicative parameter a.

    Returns
    -------
    The precipitation for runoff [mm].
    """
    return a * area_rain / 100 * precipitation * cn_factor / 100


def get_time_to_peak(watercourse_length, slope_gradient, storm_duration):
    """
    Compute the time to peak.

    Parameters
    ----------
    watercourse_length: float
        The watercourse length [m].
    slope_gradient
        The slope gradient [%].
    storm_duration
        The storm duration [min].

    Returns
    -------
    The time to peak [h].
    """
    if watercourse_length <= 0:
        raise ValueError("The watercourse length cannot be null or negative.")
    if slope_gradient < 0:
        raise ValueError("The slope gradient cannot be negative.")
    if storm_duration <= 0:
        raise ValueError("The storm duration cannot be null or negative.")

    return (storm_duration / 2 + 0.6 * 0.02 * math.pow(watercourse_length, 0.77) *
            math.pow(slope_gradient, -.385)) / 60


def get_unit_peakflow(area, t_p):
    """
    Compute the unit peakflow.

    Parameters
    ----------
    area: float
        The catchment area [km2].
    t_p: float
        The time to peak [h].

    Returns
    -------
    The unit peakflow [m3/s].
    """
    if area <= 0:
        raise ValueError("The area be null or negative.")
    if t_p <= 0:
        raise ValueError("The time to peak cannot be null or negative.")

    return 0.208 * area / t_p


def get_unit_hydrograph(q_up):
    """
    Compute the unit hydrograph.

    Parameters
    ----------
    q_up: float
        The unit peakflow [m3/s].

    Returns
    -------
    The unit hydrograph [m3/s].
    """

    q_r = np.arange(0, 3.1, 0.1)
    return np.concatenate((q_r[q_r <= 1] * q_up, q_up - ((q_r[q_r > 1] - 1) / 2 * q_up)))
