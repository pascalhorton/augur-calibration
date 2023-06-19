import pandas as pd
import matplotlib.pyplot as plt
import augur.core as agc

CATCHMENTS_FILE = r'D:\Projects\2022 AUGUR+\Analyses\LamaH catchments\Lamah_stats.csv'
DO_PLOT = True

<<<<<<< HEAD
cns = agc.get_default_cn_parameters()
=======
cns = get_default_cn_parameters()


def compute_hydrograph(catchment, soil_type, precipitation, cns, storm_duration=120):
    """
    Compute the hydrograph according to the SCS CN method.
    Adapted from the work of Omar Bellprat and Georg Heim

    Parameters
    ----------
    catchment: Pandas dataframe
        A Pandas dataframe containing the catchment properties. The fields needed are:
        'area' [km2], land cover percentages ('cover_farmland', 'cover_pasture',
        'cover_forest', 'cover_settlement', 'cover_bare', 'cover_cryo'),
        'length_watercourse' [m], mean slope gradient ('slope_gradient', [0 .. 1]).
    soil_type: str
        The soil type category. Options: 'A', 'B', 'C', 'D'
    precipitation: Pandas dataframe
        A Pandas dataframe containing the aggregated precipitation values [mm] for
        different return periods ('p10', 'p30', 'p100')
    cns: Pandas dataframe
        The curve number parameters
    storm_duration
        The duration of the storm (minutes). Default: 120

    Returns
    -------


    """
    # Parameterized rain covered area from Georg
    area_rain = 106.61 * math.pow(catchment['area'], -0.289)

    # Compute the factor from the land covers
    check_land_cover_total(catchment)
    cn_factor = compute_cn_factor(catchment, cns, soil_type)

    # Precipitation relevant to runoff
    dict_rr = {
        'yr10': 0.7 * area_rain / 100 * precipitation['p10'] * cn_factor / 100,
        'yr30': 0.7 * area_rain / 100 * precipitation['p30'] * cn_factor / 100,
        'yr100': 0.7 * area_rain / 100 * precipitation['p100'] * cn_factor / 100}
    rain_runoff = pd.DataFrame.from_dict(dict_rr)

    # Hietogram
    hf = [0.18, 0.46, 0.23, 0.13]

    # Time from start of rain to discharge peak [h]
    tp = (storm_duration / 2 + 0.6 * 0.02 * math.pow(catchment['length_watercourse'], 0.77) *
          math.pow(catchment['slope_gradient'], -.385)) / 60

    # Unit peakflow [m^3 / s]
    qp = 0.208 * catchment['area'] / tp
    q_qp = np.arange(0, 3.1, 0.1)
    q_uh = np.zeros(q_qp.shape)
    q_uh[q_qp <= 1] = q_qp[q_qp <= 1] * qp
    q_uh[q_qp > 1] = qp - ((q_qp[q_qp > 1] - 1) / 2 * qp)





>>>>>>> main





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

