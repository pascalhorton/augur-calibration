import numpy as np
import math


def get_value_return_periods(annual_max, ret_periods=None):
    """
    Get the discharge values for the provided return periods.

    Parameters
    ----------
    annual_max: Pandas serie
        Series of annual maxima.
    ret_periods: list
        List of the desired return periods.

    Returns
    -------
    A list of the discharge values for the given return periods. Default: [10, 20, 50]
    """
    if ret_periods is None:
        ret_periods = [10, 30, 100]
    y_means = annual_max.mean()
    y_std = annual_max.std()
    b = np.sqrt(6.0) / math.pi * y_std
    a = y_means - b * np.euler_gamma

    # Get precip values for different return periods
    F_rps = np.ones(len(ret_periods)) - (np.ones(len(ret_periods)) / ret_periods)
    u_rps = -np.log(-np.log(F_rps))

    prec_rps = b * u_rps + a

    return prec_rps
