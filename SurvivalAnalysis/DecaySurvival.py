from SurvivalAnalysis.ExponentialAFTFitter import ExponentialAFTFitter
import numpy as np
import os
import pandas as pd
from matplotlib import pyplot as plt
from lifelines.calibration import survival_probability_calibration
from lifelines.utils import k_fold_cross_validation
df = pd.read_excel("DecayData_LJ38.xlsx")
regressors = {'lambda_': "Mode + 0"}

eaftALL = ExponentialAFTFitter()
eaftALL.fit(df, duration_col='t', event_col='Status', regressors=regressors)
print("=================================================FULL SUMMARY=================================================\n")
eaftALL.print_summary(3)
#print(eaftALL.confidence_intervals_)
print("==============================================================================================================\n")
print("===========================END VALUES===========================\n")
keys = eaftALL.params_.loc['lambda_'].keys().tolist()
"""
keys.remove('Intercept')
intercept = eaftALL.params_.loc['lambda_']['Intercept']
intercept_lowerCI = eaftALL.confidence_intervals_.loc['lambda_']['95% lower-bound']['Intercept']
intercept_upperCI = eaftALL.confidence_intervals_.loc['lambda_']['95% upper-bound']['Intercept']
print("%30s: %12.2f +- %12.2f" % ("default", np.exp(intercept), (np.exp(intercept_upperCI) - np.exp(intercept_lowerCI))/2))
"""
for key in keys:
	mean_lifetime = np.exp(eaftALL.params_.loc['lambda_'][key])
	lowerCI = np.exp(eaftALL.confidence_intervals_.loc['lambda_']['95% lower-bound'][key])
	upperCI = np.exp(eaftALL.confidence_intervals_.loc['lambda_']['95% upper-bound'][key])
	CI_plusorminus = (upperCI - lowerCI)/2
	print("%30s %12.2f +- %12.2f" % (key.replace("Mode[T.","").replace("]",""), mean_lifetime, CI_plusorminus))
print("\n================================================================\n")

eaftALL.plot_partial_effects_on_outcome(["Mode"], df.Mode.unique(),  plot_baseline=False)
plt.show()
#survival_probability_calibration(eaftALL, df, 500000)
#scores = k_fold_cross_validation(eaftALL, df, 't', event_col='Status', k=7, scoring_method="log_likelihood", fitter_kwargs={'regressors': regressors})
#print(scores)
