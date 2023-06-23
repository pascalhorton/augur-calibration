import spotpy
import numpy as np

import augur.core as agc
import augur.data as agd


class SpotpySetup(object):
    def __init__(self, data, optimize_soil_type=False, reverse_score=False):
        """
        Initialize the spotpy setup.

        Parameters
        ----------
        data: pd.DataFrame
            The data to be used for the calibration.
        optimize_soil_type: bool
            Whether to optimize the soil type classification (A, B, C, D).
        reverse_score: bool
            Whether to reverse the score (e.g. for minimization).
        """
        self.data = data
        self.land_use_nb = 5
        self.optimize_soil_type = optimize_soil_type
        self.reverse_score = reverse_score

        # Define the parameters to be optimized
        self.params = []
        if self.optimize_soil_type:
            self.params = [
                spotpy.parameter.Uniform('thr_soil_depth', 0, 10),
                spotpy.parameter.Uniform('thr_sand_frac', 0, 1),
                spotpy.parameter.Uniform('thr_clay_frac', 0, 1),
            ]

        parameters_cn = []
        for soil in ['A', 'B', 'C', 'D']:
            for i_land in range(0, self.land_use_nb):
                param_name = f'{soil}{i_land + 1}'
                parameters_cn.append(
                    spotpy.parameter.Uniform(param_name, 0, 100, as_int=True)
                )

        self.params.extend(parameters_cn)

    def parameters(self):
        return spotpy.parameter.generate(self.params)

    def simulation(self, x):
        # Unpack the parameters
        cns_array = np.zeros((self.land_use_nb, 4))
        for i_soil, soil in enumerate(['A', 'B', 'C', 'D']):
            for i_land in range(0, self.land_use_nb):
                param_name = f'{soil}{i_land + 1}'
                cns_array[i_land, i_soil] = round(x[param_name])

        cns = agc.create_cn_parameters_from_array(cns_array)

        # Classify the soil types
        if self.optimize_soil_type:
            thr_soil_depth = x['thr_soil_depth']
            thr_sand_frac = x['thr_sand_frac']
            thr_clay_frac = x['thr_clay_frac']
            df = agd.classify_soil_type_augur_params(self.data, thr_soil_depth,
                                                     thr_sand_frac, thr_clay_frac)
        else:
            df = agd.classify_soil_type_augur(self.data)

        if len(df[df.soil_type == '']) > 0:
            raise ValueError(f'{len(df[df.soil_type == ""])} '
                             'soil types were not classified.')

        df.reset_index(inplace=True, drop=True)

        # Compute the peak discharge for each catchment
        sim = np.zeros((len(df), 3))

        for i, catch in df.iterrows():
            time, hydrograph = agc.compute_hydrograph(catch, catch['soil_type'],
                                                      catch, cns)
            peak_q = hydrograph.max(axis=0)
            sim[i, 0] = peak_q[0]
            sim[i, 1] = peak_q[1]
            sim[i, 2] = peak_q[2]

        return sim

    def evaluation(self):
        # Transform the data into a numpy array
        data = np.zeros((len(self.data), 3))
        data[:, 0] = self.data['q10']
        data[:, 1] = self.data['q30']
        data[:, 2] = self.data['q100']

        return data

    def objectivefunction(self, simulation, evaluation):
        # Compute the RMSE
        rmse = np.sqrt(np.mean((simulation - evaluation) ** 2, axis=0))

        if self.reverse_score:
            return -np.mean(rmse)

        return np.mean(rmse)
