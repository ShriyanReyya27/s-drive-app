import pandas as pd

df = pd.read_csv('csv_files/modeling/nc19crash_unit_road_cleaned.csv')

#split into alcohol and no alcohol
alcohol = df[df['ALCFLAG'] == 1]
no_alcohol = df[df['ALCFLAG'] == 0]

#subset no_alcohol with the same number of rows as alcohol
no_alcohol_same_shape = no_alcohol.sample(n=alcohol.shape[0])

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_total = pd.concat([alcohol, no_alcohol]).drop('ALCFLAG', axis=1)
y_total = pd.concat([alcohol, no_alcohol])['ALCFLAG']

#set up data for 4 types of models: 1) random sample of same size 2) undersample with near miss 3) oversample with smote 4) balanced random forest
#1) random sample of same size
X_random_sample = pd.concat([alcohol, no_alcohol_same_shape]).drop(columns=['ALCFLAG'])
y_random_sample = pd.concat([alcohol, no_alcohol_same_shape])['ALCFLAG']

X_random_sample_train, X_random_sample_test, y_random_sample_train, y_random_sample_test = train_test_split(X_random_sample, y_random_sample, test_size=0.30)

#2) undersample with near miss
from imblearn.under_sampling import NearMiss

nm = NearMiss(version=3)
X_undersampled, y_undersampled = nm.fit_resample(X_total, y_total)

X_undersampled_train, X_undersampled_test, y_undersampled_train, y_undersampled_test = train_test_split(X_undersampled, y_undersampled, test_size=0.30)

#3) oversample with smote
from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=2)
X_oversampled, y_oversampled = sm.fit_resample(X_total, y_total)

X_oversampled_train, X_oversampled_test, y_oversampled_train, y_oversampled_test = train_test_split(X_oversampled, y_oversampled, test_size=0.30)

#4) balanced random forest
X_total_train, X_total_test, y_total_train, y_total_test = train_test_split(X_total, y_total, test_size=0.30)

#all models
from imblearn.ensemble import BalancedRandomForestClassifier

rfc_random = RandomForestClassifier(n_estimators=100)
rfc_undersampled = RandomForestClassifier(n_estimators=100)
rfc_oversampled = RandomForestClassifier(n_estimators=100)
rfc_balanced = BalancedRandomForestClassifier(n_estimators=100)

rfc_random.fit(X_random_sample_train, y_random_sample_train)
rfc_undersampled.fit(X_undersampled_train, y_undersampled_train)
rfc_oversampled.fit(X_oversampled_train, y_oversampled_train)
rfc_balanced.fit(X_total_train, y_total_train)

print("random sample")
print(classification_report(y_random_sample_test, rfc_random.predict(X_random_sample_test)))

print("undersampled")
print(classification_report(y_undersampled_test, rfc_undersampled.predict(X_undersampled_test)))

print("oversampled")
print(classification_report(y_oversampled_test, rfc_oversampled.predict(X_oversampled_test)))

print("balanced")
print(classification_report(y_total_test, rfc_balanced.predict(X_total_test)))


