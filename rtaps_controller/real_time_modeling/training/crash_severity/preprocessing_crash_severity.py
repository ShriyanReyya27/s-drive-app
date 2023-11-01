import pandas as pd


unit = pd.read_csv('csv_files/north_carolina/nc20unit.csv')
person = pd.read_csv('csv_files/north_carolina/nc20per.csv')
crash = pd.read_csv('csv_files/north_carolina/nc20crash.csv')
road = pd.read_csv('csv_files/north_carolina/nc20road.csv')


#for unit, drop: OID_, PEDCONT1, PEDCONT2, DRV_INJ, DRV_REST, IMPACTSP, MOSTHARM, PHYSCOND, MANEUVER, CONTRIB1, CONTRIB2, CONTRIB3
unit = unit.drop(['OID_', 'PEDCONT1', 'PEDCONT2', 'DRV_INJ', 'DRV_REST', 'IMPACTSP', 'MOSTHARM', 'PHYSCOND', 'MANEUVER', 'CONTRIB1', 'CONTRIB2', 'CONTRIB3', 'ALCFLAG'], axis=1)

#for crash, drop: ALCFLAG, CRASH_DATE, ACCTYPE, MOSTHARM, PEDFLAG, RRX_NUM, REL_RD, REPORT, ROADCONT2
crash = crash.drop(['OID_', 'ALCFLAG', 'CRASH_DATE', 'ACCTYPE', 'MOSTHARM', 'PEDFLAG', 'RRX_NUM', 'REL_RD', 'REPORT', 'ROADCONT2'], axis=1)

#for road, drop: OID_
road = road.drop(['OID_'], axis=1)

#merge crash and unit on CASENO
crash_unit = pd.merge(crash, unit, on='CASENO')
print("merged")

#drop duplicates of CASENO
crash_unit = crash_unit.drop_duplicates(subset='CASENO')
print("dropped duplicates")

#only include PEDFLAG = 'N'
crash_unit = crash_unit[crash_unit['PEDFLAG'] == 'N']
print("pedflag")


#if the TIME column has a time, convert it into a number from 1 to 24
if(crash_unit['TIME'].dtype == 'object'):
    crash_unit['TIME'] = crash_unit['TIME'].str.split(':').str[0]
print("time")

#drop UNT_NBR, UNIT_TYP, VEHTYPE, WEATHER2, FRM_RD, TO_RD
crash_unit = crash_unit.drop(['UNT_NBR', 'UNIT_TYP', 'VEHTYPE', 'WEATHER2', 'FRM_RD', 'TO_RD'], axis=1)
print("dropped columns")

rd_conversions = ['', 'CL', 'I', 'LCL', 'MILE', 'ML', 'NC', 'PP', 'PVA', 'RP', 'RU', 'SL', 'SR', 'UNK', 'US']
class_conversions = ['', 'Urban Freeways', 'Urban Freeways Less than 4 Lanes', 'Urban 2 Lane Roads', 'Urban Multilane Divided Non-Freeway', 'Urban Multilane Undivided Non', 'Freeway', 'Rural Freeways', 'Rural Freeways Less than 4 Lanes', 'Rural 2-Lane Roads', 'Rural Multilane Divided Non-Freeway', 'Rural Multilane Undivided', 'Non-Freeway', 'Others']

#for each of the entries in FRMRD_CL and TORD_CL, convert it to the index of the list above
#loop through each entry

#loop through crash_unit using iterrows
for index, row in crash_unit.iterrows():
    print(index)
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

print("converted")

#drop pedflag column
crash_unit = crash_unit.drop('PEDFLAG', axis=1)
print("pedflag")

#save to csv
#crash_unit.to_csv('csv_files/modeling/nc19crash_unit.csv', index=False)

for col in road.columns:
    crash_unit[col] = None

#in the ROUTEID column in the crash_unit dataframe, call the rows that have the same ROUTEID in road.
#Then in the MILEPOST column in the crash_unit dataframe, find the BEGINMP and ENDMP in the road dataframe that surround the MILEPOST in the crash_unit dataframe.

for index, row in crash_unit.iterrows():
    print(index)
    road_row = road[road['RouteID'] == row['ROUTEID']]
    road_row = road_row[road_row['BeginMp'] <= row['MILEPOST']]
    road_row = road_row[road_row['EndMp'] >= row['MILEPOST']]

    #if there are no rows in road_row, then skip to the next iteration
    if road_row.shape[0] == 0:
        continue

    #for every column in the road_row dataframe, add the value to the crash_unit dataframe
    for col in road_row.columns:
        crash_unit.loc[index, col] = road_row[col].values[0]

df = crash_unit

#drop: DesignSpd, FcltyType, MunPopGroup, TrkRoute
df = df.drop(columns=['DesignSpd', 'FcltyType', 'MunPopGroup', 'TrkRoute'])


#Urban Freeways, Urban Freeways Less than 4 Lanes, Urban 2 Lane Roads, Urban Multilane Divided Non-Freeway, Urban Multilane Undivided Non-Freeway, Rural Freeways, Rural Freeways Less than 4 Lanes, Rural 2-Lane Roads, Rural Multilane Divided Non-Freeway, Rural Multilane Undivided Non-Freeway, Others
#replace the string objects in RodwyClass with integers that are the indices of the strings in the list
roadway_classes = ['Urban Freeways', 'Urban Freeways Less than 4 Lanes', 'Urban 2 Lane Roads', 'Urban Multilane Divided Non-Freeway', 'Urban Multilane Undivided Non-Freeway', 'Rural Freeways', 'Rural Freeways Less than 4 Lanes', 'Rural 2-Lane Roads', 'Rural Multilane Divided Non-Freeway', 'Rural Multilane Undivided Non-Freeway', 'Others']
shoulder_types = ['Curb-Con', 'Curb-Bit', 'Concrete', 'Bitum', 'Gravel', 'Grass']

#surface types: ‘Unpaved’,‘Bitum’, ‘JPCP’, ‘CRCP’, ‘AC_AC’, ‘AC_JCP’, ‘AC_CRCP’, ‘UJC_PCC’, ‘BPCC_PCC’,‘Other’
srfc_types = ['Unpaved', 'Bitum', 'JPCP', 'CRCP', 'AC_AC', 'AC_JCP', 'AC_CRCP', 'UJC_PCC', 'BPCC_PCC', 'Other'] 

#median types: ‘RPB’ Rigid Positive Barrier (Includes Jersey barriers), ‘SRPB’ Semi-Rigid Positive Barrier (A raised median with a sloped edge), ‘FPB’ Flexible Positive Barrier, ‘PM’ Paved Mountable, ‘Curb’ Curb (This code is used for legacy data; eventually unspecified, ‘Grass’ Grass (Includes cable guardrail), ‘Striped’ 
median_types = ['RPB', 'SRPB', 'FPB', 'PM', 'Curb', 'Grass', 'Striped']

#replace the string objects in RodwyClass with integers that are the indices of the strings in the list
for index, row in df.iterrows():
    print(index)
    if(row['RodwyClass'] not in roadway_classes):
        df.at[index, 'RodwyClass'] = 0
    else:
        df.at[index, 'RodwyClass'] = roadway_classes.index(row['RodwyClass'])
    if(row['LftShldrType'] not in shoulder_types):
        df.at[index, 'LftShldrType'] = 0
    else:
        df.at[index, 'LftShldrType'] = shoulder_types.index(row['LftShldrType'])
    if(row['RtShldrType'] not in shoulder_types):
        df.at[index, 'RtShldrType'] = 0
    else:
        df.at[index, 'RtShldrType'] = shoulder_types.index(row['RtShldrType'])

    if(row['SrfcType'] not in srfc_types):
        df.at[index, 'SrfcType'] = 0
    else:
        df.at[index, 'SrfcType'] = srfc_types.index(row['SrfcType'])
    if(row['MedianType'] not in median_types):
        df.at[index, 'MedianType'] = 0
    else:
        df.at[index, 'MedianType'] = median_types.index(row['MedianType'])

print(df.info())

df.to_csv('csv_files/modeling/nc20crash_severity_file_prelim.csv', index=False)

#‘Curb-Con’, ‘Curb-Bit’, ‘Concrete’, ‘Bitum’,‘Gravel’, ‘Grass’
#replace the string objects in LftShldrType with integers that are the indices of the strings in the list 

#merge the SPEEDLIM column with the SpeedLimit column
df['SpeedLimit'] = df['SpeedLimit'].fillna(df['SPDLIM'])

#drop the SPEEDLIM column
df = df.drop('SPDLIM', axis=1)

#drop: CASENO, MILEPOST, ROUTEID, NUM_UNIT, ROADCONT1, VISION, OID_, RouteID, MPLength, BeginMp, EndMp, DesignSpd, FcltyType
df = df.drop(columns=['CASENO', 'MILEPOST', 'ROUTEID', 'NUM_UNIT', 'ROADCONT1', 'VISION', 'RouteID', 'MPLength', 'BeginMp', 'EndMp'])

#drop LaneWidth, LftPvdShldrWidth, MedianWidth, RtPvdShldrWidth
#df = df.drop(columns=['LaneWidth', 'LftPvdShldrWidth', 'MedianWidth', 'RtPvdShldrWidth'])

df.to_csv('csv_files/modeling/nc20crash_severity_file.csv', index=False)