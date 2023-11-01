import pandas as pd


unit = pd.read_csv('csv_files/north_carolina/nc20unit.csv')
person = pd.read_csv('csv_files/north_carolina/nc20per.csv')
crash = pd.read_csv('csv_files/north_carolina/nc20crash.csv')
road = pd.read_csv('csv_files/north_carolina/nc20road.csv')


#for unit, drop: OID_, PEDCONT1, PEDCONT2, DRV_INJ, DRV_REST, IMPACTSP, MOSTHARM, PHYSCOND, MANEUVER, CONTRIB1, CONTRIB2, CONTRIB3
unit = unit.drop(['OID_', 'PEDCONT1', 'PEDCONT2', 'DRV_INJ', 'DRV_REST', 'IMPACTSP', 'MOSTHARM', 'PHYSCOND', 'MANEUVER', 'CONTRIB1', 'CONTRIB2', 'CONTRIB3'], axis=1)

#for crash, drop: ALCFLAG, CRASH_DATE, SEVERITY, ACCTYPE, MOSTHARM, PEDFLAG, RRX_NUM, REL_RD, REPORT, ROADCONT2
crash = crash.drop(['OID_', 'ALCFLAG', 'CRASH_DATE', 'SEVERITY', 'ACCTYPE', 'MOSTHARM', 'PEDFLAG', 'RRX_NUM', 'REL_RD', 'REPORT', 'ROADCONT2'], axis=1)

#for road, drop: OID_
road = road.drop(['OID_'], axis=1)


#print info for each
print(unit.info())
print(crash.info())
print(road.info())

#merge crash and unit on CASENO
crash_unit = pd.merge(crash, unit, on='CASENO')

#only include PEDFLAG = 'N'
crash_unit = crash_unit[crash_unit['PEDFLAG'] == 'N']

print(crash_unit.info())

#if the TIME column has a time, convert it into a number from 1 to 24
if(crash_unit['TIME'].dtype == 'object'):
    crash_unit['TIME'] = crash_unit['TIME'].str.split(':').str[0]

#drop UNT_NBR, UNIT_TYP, VEHTYPE, WEATHER2, FRM_RD, TO_RD
crash_unit = crash_unit.drop(['UNT_NBR', 'UNIT_TYP', 'VEHTYPE', 'WEATHER2', 'FRM_RD', 'TO_RD'], axis=1)


rd_conversions = ['', 'CL', 'I', 'LCL', 'MILE', 'ML', 'NC', 'PP', 'PVA', 'RP', 'RU', 'SL', 'SR', 'UNK', 'US']
class_conversions = ['', 'Urban Freeways', 'Urban Freeways Less than 4 Lanes', 'Urban 2 Lane Roads', 'Urban Multilane Divided Non-Freeway', 'Urban Multilane Undivided Non', 'Freeway', 'Rural Freeways', 'Rural Freeways Less than 4 Lanes', 'Rural 2-Lane Roads', 'Rural Multilane Divided Non-Freeway', 'Rural Multilane Undivided', 'Non-Freeway', 'Others']

#for each of the entries in FRMRD_CL and TORD_CL, convert it to the index of the list above
#loop through each entry

#loop through crash_unit using iterrows
for index, row in crash_unit.iterrows():
    #if the entry is not in the list above, set it to 0
    if(row['TORD_CL'] not in rd_conversions):
        crash_unit.at[index, 'TORD_CL'] = 0
    else:
        #else, set it to the index of the list
        crash_unit.at[index, 'TORD_CL'] = rd_conversions.index(row['TORD_CL'])
    if(row['FRMRD_CL'] not in rd_conversions):
        crash_unit.at[index, 'FRMRD_CL'] = 0
    else:
        crash_unit.at[index, 'FRMRD_CL'] = rd_conversions.index(row['FRMRD_CL'])
    if(row['RodwyClass'] not in class_conversions):
        crash_unit.at[index, 'RodwyClass'] = 0
    else:
        crash_unit.at[index, 'RodwyClass'] = class_conversions.index(row['RodwyClass'])


print(crash_unit.info())

#change 'Y' in ALCFLAG to 1 and 'N' to 0
crash_unit['ALCFLAG'] = crash_unit['ALCFLAG'].replace('Y', 1)
crash_unit['ALCFLAG'] = crash_unit['ALCFLAG'].replace('N', 0)

#drop pedflag column
crash_unit = crash_unit.drop('PEDFLAG', axis=1)

#add all the road columns to crash_unit
for col in road.columns:
    crash_unit[col] = None

#in the ROUTEID column in the crash_unit dataframe, call the rows that have the same ROUTEID in road.
#Then in the MILEPOST column in the crash_unit dataframe, find the BEGINMP and ENDMP in the road dataframe that surround the MILEPOST in the crash_unit dataframe.

for index, row in crash_unit.iterrows():
    road_row = road[road['RouteID'] == row['ROUTEID']]
    road_row = road_row[road_row['BeginMp'] <= row['MILEPOST']]
    road_row = road_row[road_row['EndMp'] >= row['MILEPOST']]

    #if there are no rows in road_row, then skip to the next iteration
    if road_row.shape[0] == 0:
        continue

    #for every column in the road_row dataframe, add the value to the crash_unit dataframe
    for col in road_row.columns:
        crash_unit.loc[index, col] = road_row[col].values[0]


#save to csv
crash_unit.to_csv('csv_files/modeling/nc20crash_unit.csv', index=False)


df = pd.read_csv('csv_files/modeling/nc20crash_unit.csv')

#remove all duplicates of the CASENO column
df = df.drop_duplicates(subset=['CASENO'])

#add the road columns to the df
road = pd.read_csv('csv_files/north_carolina/nc20road.csv')
for col in road.columns:
    df[col] = None

#in the ROUTEID column in the df dataframe, call the rows that have the same ROUTEID in road.
#Then in the MILEPOST column in the df dataframe, find the BEGINMP and ENDMP in the road dataframe that surround the MILEPOST in the df dataframe.

for index, row in df.iterrows():
    print(index)
    road_row = road[road['RouteID'] == row['ROUTEID']]
    road_row = road_row[road_row['BeginMp'] <= row['MILEPOST']]
    road_row = road_row[road_row['EndMp'] >= row['MILEPOST']]

    #if there are no rows in road_row, then skip to the next iteration
    if road_row.shape[0] == 0:
        continue

    #for every column in the road_row dataframe, add the value to the df dataframe
    for col in road_row.columns:
        df.loc[index, col] = road_row[col].values[0]

#save to csv
df.to_csv('csv_files/modeling/nc20crash_unit_road.csv', index=False)
