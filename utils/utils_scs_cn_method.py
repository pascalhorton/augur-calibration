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


def reclassify_slope_gradients(catchment):
    """
    Reclassify the slope gradient to match the options available on the AUGUR tool.

    Parameters
    ----------
    catchment: Pandas dataframe
        Dataframe containing a field 'slope_gradient'.

    Returns
    -------
    The dataframe with reclassified slope gradient values.
    """
    catchment.loc[catchment['slope_gradient'] <= 0.1, 'slope_gradient'] = 0.08
    catchment.loc[(catchment['slope_gradient'] > 0.1) &
                  (catchment['slope_gradient'] <= 0.5), 'slope_gradient'] = 0.3
    catchment.loc[catchment['slope_gradient'] > 0.5, 'slope_gradient'] = 0.7
