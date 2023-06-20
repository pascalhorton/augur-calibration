import pandas as pd
import spotpy
import augur.optim as ago

CATCHMENTS_FILE = r'D:\Projects\2022 AUGUR+\Analyses\LamaH catchments\Lamah_stats.csv'
DO_PLOT = False

df = pd.read_csv(CATCHMENTS_FILE)
df.rename(columns={'area_calc': 'area',
                   'dist_hup': 'length_watercourse',
                   'slope_mean': 'slope_gradient',
                   'bedrk_dep': 'soil_depth',
                   }, inplace=True)

spot_setup = ago.SpotpySetup(df)

# Select number of maximum repetitions and run spotpy
max_rep = 4000
sampler = spotpy.algorithms.sceua(spot_setup, dbname='AUGUR_Lamah', dbformat='csv')
sampler.sample(max_rep)

# Get the best parameter set
best = sampler.getdata().sort_values(by='like1', ascending=False).iloc[0]
best_params = best.iloc[1:-1].values

