import glob
import yaml
from pathlib import Path
import geopandas as gpd
import pandas as pd

import augur.data as agd

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Paths
PATH_CATCHMENTS = Path(config['PATH_CH_CATCHMENTS'])
PATH_SOILDEPTH = Path(config['PATH_SOILDEPTH'])
PATH_SOILGRIDS = Path(config['PATH_SOILGRIDS'])
PATH_CCILC = Path(config['PATH_CCILC'])
PATH_WCOVER = Path(config['PATH_WCOVER'])
OUTPUT_DIR = Path(config['OUTPUT_DIR']) / 'Swiss catchments'

# Create a generator for the catchments
catchments_ch_files = glob.glob(str(PATH_CATCHMENTS) + '/*.shp', recursive=True)
catchments_ch = (gpd.read_file(file) for file in catchments_ch_files)  # generator

# Paths to global dataset files
clay_0_5_file = PATH_SOILGRIDS / 'clay_content_0-5.tif'
clay_5_15_file = PATH_SOILGRIDS / 'clay_content_5-15.tif'
sand_0_5_file = PATH_SOILGRIDS / 'sand_0-5.tif'
sand_5_15_file = PATH_SOILGRIDS / 'sand_5-15.tif'
depth_file = PATH_SOILDEPTH / 'BDRICM_M_250m_ll.tif'
cover_cci_file = PATH_CCILC / 'land_cover_classes.tif'
cover_wc_file = PATH_WCOVER / '_Switzerland.vrt'

df = pd.DataFrame()

# Extract catchment properties.
for catchment in catchments_ch:
    s = pd.DataFrame.from_dict(
        {'id': [catchment.values[0][0]],
         'clay_0_5': [agd.get_soil_content(clay_0_5_file, catchment)],
         'clay_5_15': [agd.get_soil_content(clay_5_15_file, catchment)],
         'sand_0_5': [agd.get_soil_content(sand_0_5_file, catchment)],
         'sand_5_15': [agd.get_soil_content(sand_5_15_file, catchment)],
         'depth': [agd.get_soil_depth(depth_file, catchment)],
         'cover_cci_forest': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'forest')],
         'cover_cci_farmland': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'farmland')],
         'cover_cci_pasture': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'pasture')],
         'cover_cci_settlement': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'settlement')],
         'cover_cci_bare': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'bare')],
         'cover_cci_cryo': [agd.get_land_cover(
             'cci', cover_cci_file, catchment, 'cryo')],
         'cover_cci_water': [agd.get_land_cover(
             'cci', cover_wc_file, catchment, 'water')],
         'cover_wc_forest': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'forest')],
         'cover_wc_farmland': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'farmland')],
         'cover_wc_pasture': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'pasture')],
         'cover_wc_settlement': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'settlement')],
         'cover_wc_bare': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'bare')],
         'cover_wc_cryo': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'cryo')],
         'cover_wc_water': [agd.get_land_cover(
             'worldcover', cover_wc_file, catchment, 'water')],
         })

    df = pd.concat([df, s], ignore_index=True)


df.to_csv(OUTPUT_DIR / 'stats.csv')
print('Done.')
