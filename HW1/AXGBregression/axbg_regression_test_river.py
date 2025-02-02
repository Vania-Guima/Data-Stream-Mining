# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 20:39:20 2021

@author: hmcarvalhovieira
"""
import pandas as pd

"""
Created on Wed Nov 17 18:28:41 2021

@author: hmcarvalhovieira
"""

from axgb_regression_river import AdaptiveXGBoostRegressor
from skmultiflow.data import RegressionGenerator
from skmultiflow.evaluation import EvaluatePrequential
from skmultiflow.data.file_stream import FileStream
import numpy as np
import pandas as pd

# Adaptive XGBoost regressor parameters
n_estimators = 15       # Number of members in the ensemble
learning_rate = 0.3     # Learning rate or eta
max_depth = 6           # Max depth for each tree in the ensemble
max_window_size = 100   # Max window size
min_window_size = 10    # set to activate the dynamic window strategy
detect_drift = False    # Enable/disable drift detection
threshold = 450         # Page-Hinkley threshold

AXGBp = AdaptiveXGBoostRegressor(update_strategy='push',
                                  n_estimators=n_estimators,
                                  learning_rate=learning_rate,
                                  max_depth=max_depth,
                                  max_window_size=max_window_size,
                                  min_window_size=min_window_size,
                                  detect_drift=detect_drift,
                                  threshold=threshold)
AXGBr = AdaptiveXGBoostRegressor(update_strategy='replace',
                                  n_estimators=n_estimators,
                                  learning_rate=learning_rate,
                                  max_depth=max_depth,
                                  max_window_size=max_window_size,
                                  min_window_size=min_window_size,
                                  detect_drift=detect_drift,
                                  threshold=threshold)


stream_1 = RegressionGenerator(n_samples=2000, n_features=15, n_informative=8, random_state=100)
stream_2 = RegressionGenerator(n_samples=3000, n_features=15, n_informative=10, random_state=1)
stream_3 = RegressionGenerator(n_samples=5000, n_features=15, n_informative=7, random_state=4)
stream = np.concatenate((stream_1, stream_2, stream_3), axis=None)

X_1, y_1 = stream_1.next_sample(2000)
X_2, y_2 = stream_2.next_sample(3000)
X_3, y_3 = stream_3.next_sample(5000)

X = np.concatenate((X_1, X_2, X_3))
y = np.concatenate((y_1, y_2, y_3))

df = pd.DataFrame(np.hstack((X,np.array([y]).T)))
df.to_csv("datasets/file_reg_generator.csv", index=False)
stream = FileStream('datasets/file_reg_generator.csv')


evaluator = EvaluatePrequential(pretrain_size=0,
                                max_samples=10000,
                                metrics=['mean_square_error', 'running_time'],
                                output_file='file_test',
                                show_plot=True)

evaluator.evaluate(stream=stream,
                   model=[AXGBp, AXGBr],
                   model_names=['AXGBp', 'AXGBr'])

#
# from river import datasets
# stream = datasets.AirlinePassengers()
#
# from river import synth
# stream = synth.FriedmanDrift(drift_type='lea',
#                              position=(2000, 6000, 9000),
#                              seed=1)
#
# #
# from river import evaluate
# from river import metrics
# metric = metrics.MAE() + metrics.RMSE()
# metric = metrics.MSE()
# evaluate.progressive_val_score(dataset=stream,
#                                model=[AXGBp, AXGBr],
#                                metric=metrics.MAE(),
#                                show_memory=True,
#                                show_time=True,
#                                print_every=1000,
#                                show_plot=True)


