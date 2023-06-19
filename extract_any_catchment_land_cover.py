import warnings
import geopandas as gpd
import pandas as pd
from pathlib import Path
import yaml
from shapely.errors import ShapelyDeprecationWarning

import augur.data as agd

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Paths
PATH_CATCHMENTS_SHP = Path(config['PATH_CATCHMENTS'])
PATH_WCOVER_FILES = Path(config['PATH_WCOVER_FILES'])
OUTPUT_DIR = Path(config['OUTPUT_DIR'])

shp_catchments = gpd.read_file(PATH_CATCHMENTS_SHP)

df = pd.DataFrame()

# Extract catchment properties.
for i, catchment in shp_catchments.iterrows():
    s = pd.DataFrame.from_dict(
        {'id': [catchment['Id']],
         'name': [catchment['catchment']],
         'cover_wc_forest': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'forest')],
         'cover_wc_farmland': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'farmland')],
         'cover_wc_pasture': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'pasture')],
         'cover_wc_settlement': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'settlement')],
         'cover_wc_bare': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'bare')],
         'cover_wc_cryo': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'cryo')],
         'cover_wc_water': [agd.get_land_cover(
             'worldcover', PATH_WCOVER_FILES, catchment.geometry, 'water')],
         })

    df = pd.concat([df, s], ignore_index=True)

df.to_csv(OUTPUT_DIR / 'stats_catchments.csv')

print('Done.')
