from utils.utils_dataset_land_cover import get_land_cover
from utils.utils_discharge import get_value_return_periods
import geopandas as gpd
import pandas as pd
from pathlib import Path
import warnings
import yaml
from shapely.errors import ShapelyDeprecationWarning

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# Paths
PATH_LAMAH = Path(config['PATH_LAMAH'])
PATH_TS_DISCHARGE = PATH_LAMAH / 'D_gauges' / '2_timeseries' / 'hourly'
PATH_TS_PRECIP = PATH_LAMAH / 'A_basins_total_upstrm' / '2_timeseries' / 'daily'
PATH_CATCHMENTS = PATH_LAMAH / 'A_basins_total_upstrm' / '3_shapefiles'
PATH_ATTRIBUTES = PATH_LAMAH / 'A_basins_total_upstrm' / '1_attributes'
PATH_GAUGE_ATTRIBUTES = PATH_LAMAH / 'D_gauges' / '1_attributes'
PATH_WCOVER = Path(config['PATH_WCOVER'])
OUTPUT_DIR = Path(config['OUTPUT_DIR']) / 'LamaH catchments'

catchments_shp_files = Path(PATH_CATCHMENTS) / 'Basins_A_wgs84.shp'
shp_catchments = gpd.read_file(catchments_shp_files)

cover_file = PATH_WCOVER / '_Lamah.vrt'

attributes_file = PATH_ATTRIBUTES / 'Catchment_attributes.csv'
stream_dist_file = PATH_ATTRIBUTES / 'Stream_dist.csv'
gauge_attributes_file = PATH_GAUGE_ATTRIBUTES / 'Gauge_attributes.csv'

df_attributes = pd.read_csv(attributes_file, sep=';')
df_gauge_attributes = pd.read_csv(gauge_attributes_file, sep=';')
df_stream_dist = pd.read_csv(stream_dist_file, sep=';')
df = pd.merge(df_attributes, df_gauge_attributes, on='ID')
df = pd.merge(df, df_stream_dist, on='ID')

# Only keep relevant attributes
df = df[['ID', 'area_calc', 'elev_mean', 'slope_mean', 'bedrk_dep', 'sand_fra',
         'silt_fra', 'clay_fra', 'grav_fra', 'oc_fra', 'name', 'river',
         'lon', 'lat', 'country', 'gaps_post', 'dist_hup']]

# Only keep catchments between 1 and 300 km2
df = df[df.area_calc > 1]
df = df[df.area_calc < 300]
df.reset_index(inplace=True, drop=True)

# Convert units
df['slope_mean'] = df['slope_mean'] / 1000

for row in df.iterrows():
    catchment = row[1]
    print(catchment['name'])

    # Compute rainfall return periods
    precip_file = PATH_TS_PRECIP / f'ID_{catchment.ID}.csv'
    precip = pd.read_csv(precip_file, sep=';', usecols=[0, 22])
    annual_max_p = precip.groupby(['YYYY']).max()
    p_rps = get_value_return_periods(annual_max_p['prec'], ret_periods=[10, 30, 100])
    df.at[row[0], 'p10'] = p_rps[0]
    df.at[row[0], 'p30'] = p_rps[1]
    df.at[row[0], 'p100'] = p_rps[2]

    # Compute discharge return periods
    discharge_file = PATH_TS_DISCHARGE / f'ID_{catchment.ID}.csv'
    discharge = pd.read_csv(discharge_file, sep=';', usecols=[0, 5])
    annual_max_p = discharge.groupby(['YYYY']).max()
    q_rps = get_value_return_periods(annual_max_p['qobs'], ret_periods=[10, 30, 100])
    df.at[row[0], 'q10'] = q_rps[0]
    df.at[row[0], 'q30'] = q_rps[1]
    df.at[row[0], 'q100'] = q_rps[2]

    # Compute land cover
    shp = shp_catchments.loc[shp_catchments['ID'] == catchment.ID]
    df.at[row[0], 'cover_forest'] = get_land_cover(
        'worldcover', cover_file, shp, 'forest'),
    df.at[row[0], 'cover_farmland'] = get_land_cover(
        'worldcover', cover_file, shp, 'farmland'),
    df.at[row[0], 'cover_pasture'] = get_land_cover(
        'worldcover', cover_file, shp, 'pasture'),
    df.at[row[0], 'cover_settlement'] = get_land_cover(
        'worldcover', cover_file, shp, 'settlement'),
    df.at[row[0], 'cover_bare'] = get_land_cover(
        'worldcover', cover_file, shp, 'bare'),
    df.at[row[0], 'cover_cryo'] = get_land_cover(
        'worldcover', cover_file, shp, 'cryo'),
    df.at[row[0], 'cover_water'] = get_land_cover(
        'worldcover', cover_file, shp, 'water'),


df.to_csv(OUTPUT_DIR / 'Lamah_stats.csv')
print('Done.')
