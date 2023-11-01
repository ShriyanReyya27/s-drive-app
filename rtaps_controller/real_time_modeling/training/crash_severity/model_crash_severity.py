import pandas as pd

df = pd.read_csv('rtaps_controller/real_time_modeling/csv_files/nc20crash_severity_file.csv')
df = df.drop(columns=['RtPvdShldrWidth', 'MedianWidth', 'LftPvdShldrWidth', 'LaneWidth', 'FRMRD_CL', 'LOC_TYPE', 'TORD_CL', 'RDSURF', 'RD_PAVE', 'RD_CONF', 'RD_CHAR', 'NBR_LANE', 'MedianType'])


print(df.info())   

df = df.dropna()

#drop all severity = 6
df = df[df['SEVERITY'] != 6]

#print value counts of SEVERITY
print(df['SEVERITY'].value_counts())

#oversample with smote
from imblearn.over_sampling import SMOTE

X = df.drop(columns=['SEVERITY'])
y = df['SEVERITY']

sm = SMOTE(random_state=42)

X_res, y_res = sm.fit_resample(X, y)

df = pd.concat([X_res, y_res], axis=1)

print(df['SEVERITY'].value_counts())


#drop: RtPvdShldrWidth, MedianWidth, LftPvdShldrWidth, LaneWidth


print(df['SEVERITY'].value_counts())


#save the columns to a txt file
with open('rtaps_controller/real_time_modeling/models/crash_severity/columns2.txt', 'w') as f:
    for col in df.columns:
        f.write(col + '\n')


#drop na
df = df.dropna()


#random forest classifier on SEVERITY

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.30)

print("training")
rfc = RandomForestClassifier(n_estimators=100)

rfc.fit(X_train, y_train)

print(classification_report(y_test, rfc.predict(X_test)))

#save model
import pickle

filename = 'rtaps_controller/real_time_modeling/models/crash_severity/severity3.sav'
pickle.dump(rfc, open(filename, 'wb'))

#shap values
import shap

#explainer = shap.TreeExplainer(rfc)
#shap_values = explainer.shap_values(X_test)

print("done")

import matplotlib.pyplot as plt

#shap.summary_plot(shap_values, X_test)


'''
#save figure
plt.savefig('nc20crash_severity_shap.png')
plt.clf()


shap.summary_plot(shap_values[0], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_0.png')
plt.clf()

shap.summary_plot(shap_values[1], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_1.png')
plt.clf()

shap.summary_plot(shap_values[2], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_2.png')
plt.clf()

shap.summary_plot(shap_values[3], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_3.png')
plt.clf()

shap.summary_plot(shap_values[4], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_4.png')
plt.clf()

shap.summary_plot(shap_values[5], X_test, show=False)

#save figure
plt.savefig('nc20crash_severity_shap_5.png')
plt.clf()
'''

