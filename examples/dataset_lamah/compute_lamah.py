import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import augur.core as agc
import augur.data as agd

CATCHMENTS_FILE = r'D:\Projects\2022 AUGUR+\Analyses\LamaH catchments\Lamah_stats.csv'
PLOT_HYDROGRAPHS = False
PARAMETER_SET = 3  # 1, 2 or 3

if PARAMETER_SET == 1:
    # Original AUGUR values
    param_set = 'Original parameters'
    cns = agc.get_default_cn_parameters('redcross')

elif PARAMETER_SET == 2:
    # AUGUR values (optimized by Omar)
    param_set = 'AUGUR parameters'
    cns = agc.get_default_cn_parameters('augur')

elif PARAMETER_SET == 3:
    # Optimized using SCE-UA
    param_set = 'Optimized parameters'
    cns = pd.DataFrame(np.array([
        [10, 85, 28, 93],
        [19, 75, 65, 50],
        [40, 52, 40, 13],
        [15, 32, 88, 58],
        [23, 38, 21, 75]
    ]), columns=['A', 'B', 'C', 'D'])
    cns.index = ['farmland', 'pasture', 'forest', 'settlement', 'debris']

else:
    raise ValueError('Invalid parameter set')

# Read the catchment data
df = pd.read_csv(CATCHMENTS_FILE)

df.rename(columns={'area_calc': 'area',
                   'dist_hup': 'length_watercourse',
                   'slope_mean': 'slope_gradient',
                   'bedrk_dep': 'soil_depth',
                   }, inplace=True)

# Soil types
df = agd.classify_soil_type_augur(df)

df = df[df.soil_type != '']
df.reset_index(inplace=True, drop=True)

rel_diffs = np.zeros((len(df), 3))
diffs = np.zeros((len(df), 3))

for i, catchment in df.iterrows():
    time, hydrograph = agc.compute_hydrograph(catchment, catchment['soil_type'],
                                              catchment, cns)

    # Plot the hydrograph
    if PLOT_HYDROGRAPHS:
        plt.plot(time, hydrograph)
        plt.xlabel('Time [h]')
        plt.ylabel('Discharge [m$^3$/s]')
        plt.tight_layout()
        plt.show()

    # Get the peak discharge
    peak_q = hydrograph.max(axis=0)

    rel_diffs[i, 0] = 100 * (peak_q[0] - catchment.loc['q10']) / catchment.loc['q10']
    rel_diffs[i, 1] = 100 * (peak_q[1] - catchment.loc['q30']) / catchment.loc['q30']
    rel_diffs[i, 2] = 100 * (peak_q[2] - catchment.loc['q100']) / catchment.loc['q100']
    diffs[i, 0] = peak_q[0] - catchment.loc['q10']
    diffs[i, 1] = peak_q[1] - catchment.loc['q30']
    diffs[i, 2] = peak_q[2] - catchment.loc['q100']

    print(f'Peak discharge for {catchment["name"]}: {peak_q}')


# Total RMSE
rmse = np.sqrt(np.mean(diffs**2, axis=0))
print(f'RMSE: {rmse}')

# Plot the relative differences as boxplots
plt.figure()
plt.boxplot(rel_diffs)
plt.xticks([1, 2, 3], ['q10', 'q30', 'q100'])
plt.ylabel('Relative difference [%]')
plt.ylim([-100,500])
plt.grid(axis='y')
plt.title(param_set)
plt.tight_layout()
plt.savefig(f'lamah_{param_set}.png', dpi=300)
plt.show()

