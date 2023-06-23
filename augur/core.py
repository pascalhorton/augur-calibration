import math
import pandas as pd
import numpy as np
import augur.data as agd


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


def create_cn_parameters_from_array(cns_array):
    """
    Create a dataframe with the curve number parameters from a numpy array.

    Parameters
    ----------
    cns_array: numpy array
        The curve number parameters.

    Returns
    -------
    A dataframe with the curve number parameters.
    """
    return pd.DataFrame(cns_array,
                        columns=['A', 'B', 'C', 'D'],
                        index=['farmland', 'pasture', 'forest', 'settlement', 'debris'],
                        dtype=np.int64)


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

    Notes
    -----
    Computation of the time to peak from the time of concentration:
    Tp = 0.5 * storm_duration + 0.6 * Tc

    From: Ratnayaka, D. D., Brandt, M. J., & Johnson, M. (2009). Water supply. Butterworth-Heinemann.
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

    return 0.278 * area / t_p


def get_unit_hydrograph(q_up, t_p):
    """
    Compute the unit hydrograph.

    Parameters
    ----------
    q_up: float
        The unit peakflow [m3/s].
    t_p: float
        The time to peak [h].

    Returns
    -------
    The unit hydrograph discharge [m3/s].
    The unit hydrograph time [h].
    """

    q_r = np.arange(0, 3.1, 0.1)
    t = q_r * t_p
    q = np.concatenate((q_r[q_r <= 1] * q_up, q_up - ((q_r[q_r > 1] - 1) / 2 * q_up)))

    return t, q


def get_unit_discharge(time_rain, q_up, t_p):
    """
    Compute the unit discharge for the given time steps.

    Parameters
    ----------
    time_rain: np.array
        The time steps [h].
    q_up: float
        The unit peakflow [m3/s].
    t_p: float
        The time to peak [h].

    Returns
    -------
    The unit discharge [m3/s].
    """
    q_r = time_rain / t_p  # Corresponding Q/Qp
    q = np.concatenate((q_r[q_r <= 1] * q_up, q_up - ((q_r[q_r > 1] - 1) / 2 * q_up)))
    q[q < 0] = 0

    return q


def get_hyetogram(timesteps_nb, rain_runoff, method='augur'):
    """
    Compute the hietogram.

    Parameters
    ----------
    timesteps_nb: int
        The number of timesteps [h].
    rain_runoff: float
        The rainfall for runoff [mm].
    method: str
        The method to compute the hyetogram. Can be 'augur' or 'constant'.

    Returns
    -------
    The hyetogram.
    """
    repartition = np.array([])
    if method == 'augur':
        # Check that the time steps have a length that is a multiple of 4
        if timesteps_nb % 4 != 0:
            raise ValueError("The time steps number must be a multiple of 4.")
        factor = timesteps_nb // 4
        # Copy each values the number of times it is needed (factor)
        repartition = np.repeat(np.array([0.18, 0.46, 0.23, 0.13]), factor) / factor

    elif method == 'constant':
        # Repeat the same value for each time step
        repartition = np.repeat(1 / timesteps_nb, timesteps_nb)

    else:
        raise ValueError("The method must be 'augur' or 'constant'.")

    return repartition * rain_runoff


def build_hydrograph_from_uh(time, q_uh, precip, precip_time_steps_nb, factor=0.9):
    """
    Compute the hydrograph from the unit hydrographs

    Parameters
    ----------
    time: np.array
        The time steps [h].
    q_uh: np.array
        The unit hydrograph discharge [m3/s].
    precip: float
        The precipitation for runoff [mm].
    precip_time_steps_nb: int
        The number of time steps for the precipitation [h].
    factor: float
        The factor to apply to the hydrograph.

    Returns
    -------
    The hydrograph [m3/s].
    """
    hyetogram = get_hyetogram(precip_time_steps_nb, precip)
    q_array = np.zeros((len(time), len(time)))
    for i_time in range(len(time)):
        for i_hyeto in range(len(hyetogram)):
            if i_time + i_hyeto > len(time) - 1:
                break
            q_array[i_time + i_hyeto, i_time] = q_uh[i_time] * hyetogram[i_hyeto]

    return np.sum(q_array, axis=1) * factor


def compute_hydrograph(catchment, soil_type, precipitation, cns, storm_duration=120):
    """
    Compute the hydrograph according to the SCS CN method.
    Adapted from the work of Omar Bellprat and Georg Heim

    Parameters
    ----------
    catchment: Pandas dataframe
        A Pandas dataframe containing the catchment properties. The fields needed are:
        'area' [km2], land cover percentages ('cover_farmland', 'cover_pasture',
        'cover_forest', 'cover_settlement', 'cover_bare', 'cover_cryo', 'cover_water'),
        'length_watercourse' [m], mean slope gradient ('slope_gradient', [0 .. 1]).
    soil_type: str
        The soil type category. Options: 'A', 'B', 'C', 'D'
    precipitation: Pandas dataframe
        A Pandas dataframe containing the aggregated precipitation values [mm] for
        different return periods ('p10', 'p30', 'p100')
    cns: Pandas dataframe
        The curve number parameters
    storm_duration
        The duration of the storm (minutes). Default: 120

    Returns
    -------
    The hydrographs [m3/s] for the different return periods.
    """
    # Parameterized rain covered area
    area_rain = get_rain_area(catchment['area'])

    # Compute the factor from the land covers
    agd.check_land_cover_total(catchment)
    cn_factor = compute_cn_factor(catchment, cns, soil_type)

    # Precipitation relevant to runoff
    rain_ret_period = {
        'yr10': get_production(area_rain, precipitation['p10'], cn_factor),
        'yr30': get_production(area_rain, precipitation['p30'], cn_factor),
        'yr100': get_production(area_rain, precipitation['p100'], cn_factor)}

    # Time from start of rain to maximum outflow [h]
    t_p = get_time_to_peak(catchment['length_watercourse'],
                           catchment['slope_gradient'],
                           storm_duration)

    # Unit peakflow [m^3 / s]
    q_up = get_unit_peakflow(catchment['area'], t_p)

    # Time
    time = np.arange(0, 5, 0.1)

    # Unit discharge
    q_uh = get_unit_discharge(time, q_up, t_p)

    # Precipitation time steps number
    precip_time_steps_nb = len(time[(time > 0) & (time <= storm_duration / 60)])

    # Hydrograph
    hydrograph = np.zeros((len(time), len(rain_ret_period)))
    for i_ret_period, k_ret_period in enumerate(rain_ret_period):
        precip = rain_ret_period[k_ret_period]
        hydrograph[:, i_ret_period] = build_hydrograph_from_uh(time, q_uh, precip,
                                                               precip_time_steps_nb)

    return time, hydrograph
