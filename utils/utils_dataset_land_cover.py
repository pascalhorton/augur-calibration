from rasterstats import zonal_stats
import numpy as np


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
            catchment['cover_bare'] + catchment['cover_cryo']

    if total != 100:
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
