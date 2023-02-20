import pandas as pd
import numpy as np


def get_default_curve_number_parameters():
    """
    Get the default curve number parameters.

    Returns
    -------
    A dataframe with the default curve number parameters.
    """

    cns = pd.DataFrame(np.array([[35, 40, 43, 46],
                                 [37, 37, 40, 82],
                                 [20, 48, 70, 100],
                                 [59, 73, 100, 60],
                                 [8, 10, 15, 25]]),
                       columns=['deep', 'sandy', 'superficial', 'clay'])
    cns.index = ['farmland', 'pasture', 'forest', 'settlement', 'debris']

    return cns
