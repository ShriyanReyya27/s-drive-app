import pandas as pd

df20 = pd.read_csv('csv_files/modeling/nc20distracted_driving.csv')
df19 = pd.read_csv('csv_files/modeling/nc19distracted_driving.csv')
df18 = pd.read_csv('csv_files/modeling/nc18distracted_driving.csv')

df = pd.concat([df20, df19, df18])

#print(df.info())

#drop: Shape_Length, ThruLaneCount, MU_PCT, SU_PCT, AADT, UrbanPop, TerrainType, SrfcWidth, RtShldrWidth, RtPvdShldrWidth, ROW, CONTRIB2, CONTRIB3, LaneWidth, RouteClass, FuncClass, LftPvdShldrWidth, LftShldrWidth, MedianWidth
#df = df.drop(columns=['Shape_Length', 'ThruLaneCount', 'MU_PCT', 'SU_PCT', 'AADT', 'UrbanPop', 'TerrainType', 'SrfcWidth', 'RtShldrWidth', 'RtPvdShldrWidth', 'ROW', 'CONTRIB2', 'CONTRIB3', 'LaneWidth', 'RouteClass', 'FuncClass', 'LftPvdShldrWidth', 'LftShldrWidth', 'MedianWidth'])

df = df.drop(columns = ['LaneWidth', 'LftPvdShldrWidth', 'RtPvdShldrWidth', 'MedianWidth', 'CONTRIB2', 'CONTRIB3'])

#drop all null
df = df.dropna()

print(df.info())

distracted = df[df['DISTRACTED'] == 1]
not_distracted = df[df['DISTRACTED'] == 0]

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_total = pd.concat([distracted, not_distracted]).drop('DISTRACTED', axis=1)
y_total = pd.concat([distracted, not_distracted])['DISTRACTED']
print("split")

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=2)
X_oversampled, y_oversampled = sm.fit_resample(X_total, y_total)
print("oversampled")    

#print the valuecounts of DISTRACTED in y_oversampled
print(y_oversampled.value_counts())


X_oversampled_train, X_oversampled_test, y_oversampled_train, y_oversampled_test = train_test_split(X_oversampled, y_oversampled, test_size=0.30)
print("test_train_split")

rfc_oversampled = RandomForestClassifier(n_estimators=100)
rfc_oversampled.fit(X_oversampled_train, y_oversampled_train)
print("fit")

#print classification report
print(classification_report(y_oversampled_test, rfc_oversampled.predict(X_oversampled_test)))

#save model as pickle
import pickle

pickle.dump(rfc_oversampled, open('executables/north_carolina/models/distracted_driving_model.sav', 'wb'))

#save X_test
X_oversampled_test.to_csv('csv_files/modeling/distracted_driving_X_test.csv', index=False)
