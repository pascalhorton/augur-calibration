import math
import pandas as pd
import numpy as np
from rasterstats import zonal_stats


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

    return catchment


def get_soil_content(raster_file, polygon):
    """
    Extract the soil content from SoilGrid data.

    Parameters
    ----------
    raster_file: str|Path
        Path to the SoilGrid file.
    polygon: geometry
        Polygon for which to extract the soil properties.

    Returns
    -------
    The soil fraction of clay/sand, for example ([0 .. 1]).
    """
    return 100 * zonal_stats(polygon, raster_file, nodata=-999)[0]['mean'] / 1000


def get_soil_depth(raster_file, polygon):
    """
    Extract the soil depth from SoilGrid data.

    Parameters
    ----------
    raster_file: str|Path
        Path to the SoilGrid file.
    polygon: geometry
        Polygon for which to extract the soil properties.

    Returns
    -------
    The soil depth in meters.
    """
    return zonal_stats(polygon, raster_file, nodata=-999)[0]['mean']


def check_land_cover_total(catchment):
    """
    Check that the sum of land cover percentage sums to 100%.

    Parameters
    ----------
    catchment: Pandas dataframe
        Dataframe containing the land cover percentages
    """
    total = catchment['cover_farmland'] + catchment['cover_pasture'] + \
            catchment['cover_forest'] + catchment['cover_settlement'] + \
            catchment['cover_bare'] + catchment['cover_cryo'] + catchment['cover_water']

    if not math.isclose(total, 100):
        raise ValueError(f"The sum of land covers should be 100%. Here: {total}.")


def get_land_cover(dataset, raster_file, polygon, type):
    """
    Get the land cover percent from a given dataset and for a provided polygon.

    Parameters
    ----------
    dataset: str
        The dataset to extract the land cover from: cci or worldcover.
    raster_file: str|Path
        The path to the raster file of the selected dataset.
    polygon
        The polygon of interest.
    type
        The land cover type to compute. Options: farmland, pasture, forest, settlement,
        water, bare, cryo

    Returns
    -------
    The percentage of the land cover of interest.
    """
    if dataset == 'cci':
        if type == 'farmland':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_farmland})[0]['cover']
        if type == 'pasture':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_pasture})[0]['cover']
        if type == 'forest':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_forest})[0]['cover']
        if type == 'settlement':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_settlement})[0]['cover']
        if type == 'water':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_water})[0]['cover']
        if type == 'bare':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_bare})[0]['cover']
        if type == 'cryo':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_cci_cryo})[0]['cover']

        raise ValueError(f"Type {type} is not defined.")

    elif dataset == 'worldcover':
        if type == 'farmland':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_farmland})[0]['cover']
        if type == 'pasture':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_pasture})[0]['cover']
        if type == 'forest':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_forest})[0]['cover']
        if type == 'settlement':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_settlement})[0]['cover']
        if type == 'water':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_water})[0]['cover']
        if type == 'bare':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_bare})[0]['cover']
        if type == 'cryo':
            return 100 * zonal_stats(polygon, raster_file, nodata=0,
                                     add_stats={'cover': cover_wc_cryo})[0]['cover']

        raise ValueError(f"Type {type} is not defined.")

    raise ValueError(f"Dataset {dataset} is not defined.")


def cover_cci_farmland(x):
    """ Extract the percentage of farmland from CCI. """
    return np.ma.count(x[(x >= 10) & (x <= 30)]) / np.ma.count(x)


def cover_cci_pasture(x):
    """ Extract the percentage of pasture from CCI. """
    return (np.ma.count(x[x == 40]) + np.ma.count(
        x[(x >= 100) & (x <= 153)])) / np.ma.count(x)


def cover_cci_forest(x):
    """ Extract the percentage of forest from CCI. """
    return np.ma.count(x[(x >= 50) & (x <= 90)]) / np.ma.count(x)


def cover_cci_settlement(x):
    """ Extract the settlement of farmland from CCI. """
    return np.ma.count(x[x == 190]) / np.ma.count(x)


def cover_cci_water(x):
    """ Extract the percentage of water from CCI. """
    return (np.ma.count(x[(x >= 160) & (x <= 180)]) + np.ma.count(
        x[x == 210])) / np.ma.count(x)


def cover_cci_bare(x):
    """ Extract the percentage of bare ground from CCI. """
    return np.ma.count(x[(x >= 200) & (x <= 202)]) / np.ma.count(x)


def cover_cci_cryo(x):
    """ Extract the percentage of glaciers from CCI. """
    return np.ma.count(x[x == 220]) / np.ma.count(x)


def cover_wc_farmland(x):
    """ Extract the percentage of farmland from WorldCover. """
    return np.ma.count(x[x == 40]) / np.ma.count(x)


def cover_wc_pasture(x):
    """ Extract the percentage of pasture from WorldCover. """
    return (np.ma.count(x[(x >= 20) & (x <= 30)]) + np.ma.count(
        x[(x >= 90) & (x <= 100)])) / np.ma.count(x)


def cover_wc_forest(x):
    """ Extract the percentage of forest from WorldCover. """
    return np.ma.count(x[x == 10]) / np.ma.count(x)


def cover_wc_settlement(x):
    """ Extract the percentage of settlement from WorldCover. """
    return np.ma.count(x[x == 50]) / np.ma.count(x)


def cover_wc_water(x):
    """ Extract the percentage of water from WorldCover. """
    return np.ma.count(x[x == 80]) / np.ma.count(x)


def cover_wc_bare(x):
    """ Extract the percentage of bare ground from WorldCover. """
    return np.ma.count(x[x == 60]) / np.ma.count(x)


def cover_wc_cryo(x):
    """ Extract the percentage of glaciers from WorldCover. """
    return np.ma.count(x[x == 70]) / np.ma.count(x)


def get_value_return_periods(annual_max, ret_periods=None):
    """
    Get the discharge/precip values for the provided return periods.

    Parameters
    ----------
    annual_max: Pandas serie
        Series of annual maxima.
    ret_periods: list
        List of the desired return periods.

    Returns
    -------
    A list of the values for the given return periods. Default: [10, 30, 50]
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

    vals_rps = b * u_rps + a

    return vals_rps


def classify_soil_type_augur(df):
    """
    Classify the soil type based on the soil depth, sand and clay (AUGUR approach).

    Parameters
    ----------
    df: Pandas dataframe
        Dataframe containing the soil depth, sand and clay fractions.

    Returns
    -------
    Dataframe containing the soil type.

    Notes
    -----
    The soil type is defined as follows:
    - deep (>= 0.4m) -> A
    - sandy (< 0.4m) -> B
    - superficial (low clay) -> C
    - high clay content -> D
    """
    df['soil_type'] = ''
    df.loc[(df['soil_depth'] >= 0.4), 'soil_type'] = 'A'
    df.loc[(df['soil_depth'] < 0.4) &
           (df['sand_fra'] >= 0.5), 'soil_type'] = 'B'
    df.loc[(df['soil_depth'] < 0.4) &
           (df['sand_fra'] < 0.5), 'soil_type'] = 'C'
    df.loc[(df['clay_fra'] >= 0.4), 'soil_type'] = 'D'

    return df


def classify_soil_type_augur_params(df, thr_soil_depth, thr_sand_frac,
                                    thr_clay_frac):
    """
    Classify the soil type based on the soil depth, sand and clay (AUGUR approach).

    Parameters
    ----------
    df: Pandas dataframe
        Dataframe containing the soil depth, sand and clay fractions.
    thr_soil_depth: float
        Threshold for the soil depth (class A vs B and C).
    thr_sand_frac: float
        Threshold for the sand fraction (class B vs C).
    thr_clay_frac: float
        Threshold for the clay fraction (class D).

    Returns
    -------
    Dataframe containing the soil type.

    Notes
    -----
    The soil type is defined as follows:
    - deep (>= thr_soil_depth) -> A
    - sandy (< thr_soil_depth & >= thr_sand_frac) -> B
    - superficial (low clay) (< thr_soil_depth & < thr_sand_frac) -> C
    - high clay content (>= thr_clay_frac) -> D
    """
    df['soil_type'] = ''
    df.loc[(df['soil_depth'] >= thr_soil_depth), 'soil_type'] = 'A'
    df.loc[(df['soil_depth'] < thr_soil_depth) &
           (df['sand_fra'] >= thr_sand_frac), 'soil_type'] = 'B'
    df.loc[(df['soil_depth'] < thr_soil_depth) &
           (df['sand_fra'] < thr_sand_frac), 'soil_type'] = 'C'
    df.loc[(df['clay_fra'] >= thr_clay_frac), 'soil_type'] = 'D'

    return df


def classify_soil_type_usa(df):
    """
    Classify the soil type based on the soil depth, sand and clay (USA approach).
    Based on the U.S. Department of Agriculture thresholds

    Parameters
    ----------
    df: Pandas dataframe
        Dataframe containing the soil depth, sand and clay fractions.

    Returns
    -------
    Dataframe containing the soil type.
    """
    df['soil_type'] = ''
    df.loc[(df['soil_depth'] >= 0.5) &
           (df['clay_fra'] < 0.1), 'soil_type'] = 'A'
    df.loc[(df['soil_depth'] >= 0.5) &
           (df['clay_fra'] >= 0.1) &
           (df['clay_fra'] < 0.2), 'soil_type'] = 'B'
    df.loc[(df['soil_depth'] >= 0.5) &
           (df['sand_fra'] < 0.5) &
           (df['clay_fra'] >= 0.2) &
           (df['clay_fra'] < 0.4), 'soil_type'] = 'C'
    df.loc[(df['clay_fra'] >= 0.4) &
           (df['sand_fra'] < 0.5), 'soil_type'] = 'D'
    df.loc[(df['soil_depth'] < 0.5), 'soil_type'] = 'D'

    return df
