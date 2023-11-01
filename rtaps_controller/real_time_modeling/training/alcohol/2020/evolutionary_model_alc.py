import pandas as pd

df = pd.read_csv('csv_files/modeling/nc20crash_unit_road_cleaned.csv')

#split into alcohol and no alcohol
alcohol = df[df['ALCFLAG'] == 1]
no_alcohol = df[df['ALCFLAG'] == 0]

#print info
print(alcohol.info())
print(no_alcohol.info())

#subset no_alcohol with the same number of rows as alcohol
no_alcohol2 = no_alcohol.sample(n=alcohol.shape[0])


#continuous variables: NBR_LANE	RD_CHAR	RD_CONF	RD_PAVE	RDSURF	TIME	TORD_CL	WEATHER1	RodwyClass	ALCFLAG	RouteClass	FuncClass	LftShldrType	LftShldrWidth	MedianType	ROW	RtShldrType	RtShldrWidth	SpeedLimit	SrfcType	SrfcWidth	TerrainType	UrbanPop	AADT	SU_PCT	MU_PCT	ThruLaneCount	Shape_Length
#categorical are: FRMRD_CL	LIGHT	LOC_TYPE	NBR_LANE	RD_CHAR	RD_CONF	RD_PAVE	RDSURF	TIME	TORD_CL	WEATHER1	RodwyClass	ALCFLAG	RouteClass	FuncClass	LftShldrType	LftShldrWidth	MedianType	ROW	RtShldrType	RtShldrWidth	SpeedLimit	SrfcType	SrfcWidth	TerrainType	UrbanPop	AADT	SU_PCT	MU_PCT	ThruLaneCount
#set the type of the cont variables to float64
cont_vb = ['NBR_LANE', 'RD_CHAR', 'RD_CONF', 'RD_PAVE', 'RDSURF', 'TIME', 'TORD_CL', 'WEATHER1', 'RodwyClass', 'ALCFLAG', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'MedianType', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount', 'Shape_Length']
for vb in cont_vb:
    alcohol[vb] = alcohol[vb].astype('float64')
    no_alcohol2[vb] = no_alcohol2[vb].astype('float64')

cat_vb = ['FRMRD_CL', 'LIGHT', 'LOC_TYPE', 'NBR_LANE', 'RD_CHAR', 'RD_CONF', 'RD_PAVE', 'RDSURF', 'TIME', 'TORD_CL', 'WEATHER1', 'RodwyClass', 'ALCFLAG', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'MedianType', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount']
for vb in cat_vb:
    alcohol[vb] = alcohol[vb].astype('category')
    no_alcohol2[vb] = no_alcohol2[vb].astype('category')

#train a model after combining the two, but train it again after with another subset. however, retain the features obtained from the first model so the model evolves
#model with random forest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

#start model
X = pd.concat([alcohol, no_alcohol2]).drop('ALCFLAG', axis=1)
y = pd.concat([alcohol, no_alcohol2])['ALCFLAG']

X2 = pd.concat([alcohol, no_alcohol]).drop('ALCFLAG', axis=1)
y2 = pd.concat([alcohol, no_alcohol])['ALCFLAG']

#use smote
from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=2)
X_resampled_sm, y_resampled_sm = sm.fit_resample(X, y)

X_smote_train, X_smote_test, y_smote_train, y_smote_test = train_test_split(X_resampled_sm, y_resampled_sm, test_size=0.30)

#model
rfc = RandomForestClassifier(n_estimators=100)

rfc.fit(X_smote_train, y_smote_train)

#store roc auc score
from sklearn.metrics import roc_auc_score
roc_auc_4 = roc_auc_score(y_smote_test, rfc.predict_proba(X_smote_test)[:,1])

#precision, recall, accuracy, f1
print("smote + random forest")
print(classification_report(y_smote_test, rfc.predict(X_smote_test)))

#use near miss to undersample
from imblearn.under_sampling import NearMiss

nm = NearMiss(version=3)
X_resampled_nm, y_resampled_nm = nm.fit_resample(X2, y2)

X_resampled_train, X_resampled_test, y_resampled_train, y_resampled_test = train_test_split(X_resampled_nm, y_resampled_nm, test_size=0.30)

X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.30)

#split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

#fit model
rfc = RandomForestClassifier(n_estimators=100)

rfc.fit(X_train, y_train)

#store roc auc score
from sklearn.metrics import roc_auc_score
roc_auc = roc_auc_score(y_test, rfc.predict_proba(X_test)[:,1])

print("random undersample + random forest")
print(classification_report(y_test, rfc.predict(X_test)))

#use BalancedRandomForestClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
brfc = BalancedRandomForestClassifier(n_estimators=150, random_state=2)

brfc.fit(X2_train, y2_train)

roc_auc2 = roc_auc_score(y2_test, brfc.predict_proba(X2_test)[:,1])

print("balanced random forest")
print(classification_report(y2_test, brfc.predict(X2_test)))

#fit model
rfc = RandomForestClassifier(n_estimators=150, random_state=2)

rfc.fit(X_resampled_train, y_resampled_train)

#store roc auc score
from sklearn.metrics import roc_auc_score
roc_auc3 = roc_auc_score(y_resampled_test, rfc.predict_proba(X_resampled_test)[:,1])

print("near miss + random forest")
print(classification_report(y_resampled_test, rfc.predict(X_resampled_test)))


#print both scores
print("random undersample + random forest", roc_auc)
print("balanced random forest", roc_auc2)
print("near miss + random forest", roc_auc3)
print("smote + random forest", roc_auc_4)

'''
from imblearn.under_sampling import NearMiss

nm = NearMiss(version=3)
X_resampled_nm, y_resampled_nm = nm.fit_resample(df.drop(columns=['ALCFLAG']), df['ALCFLAG'])

print(X_resampled_nm.info())
print(y_resampled_nm.info())

#model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X = X_resampled_nm
y = y_resampled_nm
'''

import shap

explainer = shap.TreeExplainer(rfc)
shap_values = explainer.shap_values(X_resampled_test)

#shap.summary_plot(shap_values[1], X_resampled_test)

#shap.dependence_plot('NBR_LANE', shap_values[1], X_resampled_test, interaction_index=None)

import matplotlib.pyplot as plt

'''
#for every column, save a dependence plot
for col in X_resampled_test.columns:
    for col2 in X_resampled_test.columns:
        if col != col2:
            shap.dependence_plot(col, shap_values[1], X_resampled_test, interaction_index=col2, show=False)
            plt.savefig(col + '_' + col2 + '.png')
            plt.clf()
'''
            
#plot the 
shap.dependence_plot('RodwyClass', shap_values[1], X_resampled_test, interaction_index=None)