import pandas as pd

X_test = pd.read_csv('csv_files/modeling/distracted_driving_X_test.csv')

#subset X_test to 1/10th of the data
X_test = X_test.sample(frac=0.1, random_state=1)

import pickle
model = pickle.load(open('executables/north_carolina/models/distracted_driving_model.sav', 'rb'))

import shap
import matplotlib.pyplot as plt

explainer = shap.TreeExplainer(model)
print("explainer")

shap_values = explainer.shap_values(X_test)
print("shape values")

shap.summary_plot(shap_values[1], X_test)

