from rasterstats import zonal_stats


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
