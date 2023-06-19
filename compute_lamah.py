import pandas as pd
import matplotlib.pyplot as plt
import augur.core as agc

CATCHMENTS_FILE = r'D:\Projects\2022 AUGUR+\Analyses\LamaH catchments\Lamah_stats.csv'
DO_PLOT = True

cns = agc.get_default_cn_parameters()





#THR_DEPTH = 1
#THR_CLAY = 0.3

df = pd.read_csv(CATCHMENTS_FILE)

df.rename(columns={'area_calc': 'area',
                   'dist_hup': 'length_watercourse',
                   'slope_mean': 'slope_gradient',
                   'bedrk_dep': 'soil_depth',
                   }, inplace=True)


# Soil properties
#pc_deep = 100 * len(df[df['bedrk_dep'] > THR_DEPTH]) / len(df)
#print(f'{pc_deep:.2f}% are considered deep soil')
#pc_clay = 100 * len(df[df['clay_fra'] > THR_CLAY]) / len(df)
#print(f'{pc_clay:.2f}% are considered high clay content')

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



# Defined soil types in AUGUR:
# - deep (> 0.4m)
# - sandy (< 0.4m)
# - superficial (low clay)
# - high clay content

# df.loc[(df['soil_depth'] >= 0.4), 'soil_type'] = 'deep'
# df.loc[(df['soil_depth'] < 0.4) & (df['sand_fra'] >= 0.5), 'soil_type'] = 'deep'
# df.loc[(df['soil_depth'] < 0.4) & (df['sand_fra'] < 0.5), 'soil_type'] = 'superficial'
# df.loc[(df['clay_fra'] >= 0.4), 'soil_type'] = 'clay'

df = df[df.soil_type != '']

for row in df.iterrows():
    catchment = row[1]
    time, hydrograph = agc.compute_hydrograph(catchment, catchment['soil_type'],
                                              catchment, cns)

    # Plot the hydrograph
    if DO_PLOT:
        plt.plot(time, hydrograph)
        plt.xlabel('Time [h]')
        plt.ylabel('Discharge [m$^3$/s]')
        plt.tight_layout()
        plt.show()

    # Get the peak discharge
    peak_discharge = hydrograph.max(axis=0)

    q10_diff = (peak_discharge[0] - catchment.loc['q10']) / catchment.loc['q10']
    q30_diff = (peak_discharge[1] - catchment.loc['q30']) / catchment.loc['q30']
    q100_diff = (peak_discharge[2] - catchment.loc['q100']) / catchment.loc['q100']



    print(f'Peak discharge for {catchment["name"]}: {peak_discharge}')

