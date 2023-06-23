import pandas as pd
import spotpy
import augur.optim as ago

CATCHMENTS_FILE = r'D:\Projects\2022 AUGUR+\Analyses\LamaH catchments\Lamah_stats.csv'
DO_PLOT = False
OPTIMIZE_SOIL_TYPE = False
METHOD = 'sceua'  # sceua, mc, mcmc, rope
EXPERIMENT_ID = 2
N_SAMPLES = 5000

df = pd.read_csv(CATCHMENTS_FILE)
df.rename(columns={'area_calc': 'area',
                   'dist_hup': 'length_watercourse',
                   'slope_mean': 'slope_gradient',
                   'bedrk_dep': 'soil_depth',
                   }, inplace=True)

spot_setup = ago.SpotpySetup(df, OPTIMIZE_SOIL_TYPE)

if METHOD == 'sceua':
    sampler = spotpy.algorithms.sceua(spot_setup, dbformat='csv',
                                      dbname=f'AUGUR_Lamah_sceua_{EXPERIMENT_ID}')
    sampler.sample(N_SAMPLES)

elif METHOD == 'mc':
    sampler = spotpy.algorithms.mc(spot_setup, dbformat='csv',
                                   dbname=f'AUGUR_Lamah_mc_{EXPERIMENT_ID}')
    sampler.sample(N_SAMPLES)

elif METHOD == 'mcmc':
    sampler = spotpy.algorithms.mcmc(spot_setup, dbformat='csv',
                                     dbname=f'AUGUR_Lamah_mcmc_{EXPERIMENT_ID}')
    sampler.sample(N_SAMPLES)

elif METHOD == 'rope':
    sampler = spotpy.algorithms.rope(spot_setup, dbformat='csv',
                                     dbname=f'AUGUR_Lamah_rope_{EXPERIMENT_ID}')
    sampler.sample(N_SAMPLES)

else:
    raise ValueError(f'Unknown method: {METHOD}')

