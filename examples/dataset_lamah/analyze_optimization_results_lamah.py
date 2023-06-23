import pandas as pd
import spotpy
import matplotlib.pyplot as plt

METHODS = ['sceua', 'mc', 'mcmc']

for method in METHODS:
    print(f'Extracting {method}')

    # Load the results
    results = spotpy.analyser.load_csv_results(f'AUGUR_Lamah_{method}', usecols=range(24))

    # Get the best parameter set
    spotpy.analyser.get_best_parameterset(results, maximize=False)

    # Plot parameter interaction
    spotpy.analyser.plot_parameterInteraction(results)
    plt.tight_layout()
    plt.show()

    # Plot posterior parameter distribution
    posterior = spotpy.analyser.get_posterior(results, percentage=10)
    spotpy.analyser.plot_parameterInteraction(posterior)
    plt.tight_layout()
    plt.show()
