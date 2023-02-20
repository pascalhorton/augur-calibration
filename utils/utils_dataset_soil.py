from rasterstats import zonal_stats


def get_soil_content(raster_file, polygon):
    """
    Extract the soil content from SoilGrid data.

    Parameters
    ----------
    raster_file: str
        Path to the SoilGrid file.
    polygon: geometry
        Polygon for which to extract the soil properties.

    Returns
    -------
    The soil content of clay/sand, for example, in percent.
    """
    return 100 * zonal_stats(polygon, raster_file, nodata=-999)[0]['mean'] / 1000


def get_soil_depth(raster_file, polygon):
    """
    Extract the soil depth from SoilGrid data.

    Parameters
    ----------
    raster_file: str
        Path to the SoilGrid file.
    polygon: geometry
        Polygon for which to extract the soil properties.

    Returns
    -------
    The soil depth in meters.
    """
    return zonal_stats(polygon, raster_file, nodata=-999)[0]['mean']
