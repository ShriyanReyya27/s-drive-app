import pandas as pd

df18 = pd.read_csv('csv_files/modeling/nc18distracted_driving.csv')
df19 = pd.read_csv('csv_files/modeling/nc19distracted_driving.csv')
df20 = pd.read_csv('csv_files/modeling/nc20distracted_driving.csv')

print(df19['PEDFLAG'].value_counts())
print(df20['PEDFLAG'].value_counts())

df = pd.concat([df20, df19, df18])

print(df['PEDFLAG'].value_counts())


df = df.drop(columns = ['LaneWidth', 'LftPvdShldrWidth', 'RtPvdShldrWidth', 'MedianWidth'])

df18 = df18.drop(columns = ['LaneWidth', 'LftPvdShldrWidth', 'RtPvdShldrWidth', 'MedianWidth'])
df18 = df18.dropna()
print(df['PEDFLAG'].value_counts())


df = df.dropna()

print(df['PEDFLAG'].value_counts())
#print(df.info())

#print(df18.info())


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_total = df.drop('PEDFLAG', axis=1)
y_total = df['PEDFLAG']

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=2)

X_oversampled, y_oversampled = sm.fit_resample(X_total, y_total)

print(y_oversampled.value_counts())

'''
'''
X_oversampled_train, X_oversampled_test, y_oversampled_train, y_oversampled_test = train_test_split(X_oversampled, y_oversampled, test_size=0.30)

rfc_oversampled = RandomForestClassifier(n_estimators=100)

rfc_oversampled.fit(X_oversampled_train, y_oversampled_train)

#make the number of ped and non ped in df18 the same
df18_ped = df18[df18['PEDFLAG'] == 1]
df18_not_ped = df18[df18['PEDFLAG'] == 0]

df18_not_ped = df18_not_ped.sample(n=len(df18_ped))

df18 = pd.concat([df18_ped, df18_not_ped])

y_test_18 = df18['PEDFLAG']
X_test_18 = df18.drop(columns=['PEDFLAG'])

print(classification_report(y_test_18, rfc_oversampled.predict(X_test_18)))
