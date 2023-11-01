import pandas as pd

df = pd.read_csv('csv_files/modeling/nc19crash_unit_road_cleaned.csv')

#split into alcohol and no alcohol
alcohol = df[df['ALCFLAG'] == 1]
no_alcohol = df[df['ALCFLAG'] == 0]

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_total = pd.concat([alcohol, no_alcohol]).drop('ALCFLAG', axis=1)
y_total = pd.concat([alcohol, no_alcohol])['ALCFLAG']
print("split")

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=2)
X_oversampled, y_oversampled = sm.fit_resample(X_total, y_total)
print("oversampled")

X_oversampled_train, X_oversampled_test, y_oversampled_train, y_oversampled_test = train_test_split(X_oversampled, y_oversampled, test_size=0.30)
print("test_train_split")

rfc_oversampled = RandomForestClassifier(n_estimators=100)
rfc_oversampled.fit(X_oversampled_train, y_oversampled_train)
print("fit")

import shap
import matplotlib.pyplot as plt

explainer = shap.TreeExplainer(rfc_oversampled)
print("explainer")
shap_values = explainer.shap_values(X_oversampled_test)
print("shap_values")

shap.summary_plot(shap_values[1], X_oversampled_test, show=False)
plt.savefig('summary_plot.png')

#shap.dependence_plot(shap_values[1], X_oversampled_test)