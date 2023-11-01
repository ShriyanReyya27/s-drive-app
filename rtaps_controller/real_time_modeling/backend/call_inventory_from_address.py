import pandas as pd
df = pd.read_csv('rtaps_controller/real_time_modeling/csv_files/nc20road_route_data_secondary_coded.csv')
lookup = pd.read_csv('rtaps_controller/real_time_modeling/csv_files/SRLookUp_coded2.csv')


#NEED TO GENERATE:
'''
LIGHT
TIME
WEATHER1
'''
'''
#encode: SrfcType, RtShldrType, LftShldrType, RodwyClass
class_conversions = ['', 'Urban Freeways', 'Urban Freeways Less than 4 Lanes', 'Urban 2 Lane Roads', 'Urban Multilane Divided Non-Freeway', 'Urban Multilane Undivided Non', 'Freeway', 'Rural Freeways', 'Rural Freeways Less than 4 Lanes', 'Rural 2-Lane Roads', 'Rural Multilane Divided Non-Freeway', 'Rural Multilane Undivided', 'Non-Freeway', 'Others']
srfc_types = ['Unpaved', 'Bitum', 'JPCP', 'CRCP', 'AC_AC', 'AC_JCP', 'AC_CRCP', 'UJC_PCC', 'BPCC_PCC', 'Other'] 
shoulder_types = ['Curb-Con', 'Curb-Bit', 'Concrete', 'Bitum', 'Gravel', 'Grass']

for index, row in df.iterrows():
    print(index)
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
    if(row['RodwyClass'] not in class_conversions):
        df.at[index, 'RodwyClass'] = 0
    else:
        df.at[index, 'RodwyClass'] = class_conversions.index(row['RodwyClass'])
'''
        
#only include the following columns:
'''
RodwyClass
RouteClass
FuncClass
LftShldrType
LftShldrWidth
ROW
RtShldrType
RtShldrWidth
SpeedLimit
SrfcType
SrfcWidth
TerrainType
UrbanPop
AADT
SU_PCT
MU_PCT
ThruLaneCount
Shape_Length
'''

'''
df = df[['RodwyClass', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount', 'Shape_Length', 'RI Class', 'RI Qualifier', 'RI Inventory', 'RI Number', 'RI County']]

#make Custom ID column
#this is just the RI number + RI county, but the county has to be padded on the left with 0s to make it 3 digits
df['Custom ID'] = df['RI Number'].astype(str) + df['RI County'].astype(str).str.zfill(3)

#save to csv
df.to_csv('rtaps_controller/modeling/csv_files/nc20road_route_data_secondary_coded.csv', index=False)
'''

#print(df.info())


#dictionary of road names and counties and lat long pairs


#road_county_lat_long = {('Iron Works Rd', 'ROCKINGHAM', 20, 20), ('W Bear Grass Rd', 'MARTIN', 40, 90)}
road_county_lat_long = {('Iron Works Rd', 'ROCKINGHAM', 20, 20)}


#return the row that has the same road name and county
def get_row(road_name, county_name):
    #loop through each row in lookup
    for index, row in lookup.iterrows():
        #if road name and county name match, return row
        if row['Road Name'] == road_name and row['County'] == county_name.upper():
            return row
        
    #if no match, return None
    return None
'''
from fuzzywuzzy import fuzz

#make all of the counties in lookup lowercase

def get_row2(road_name, county_name, lookup):
    #loop through each row in lookup

    #keep a record of the best match, this should have the index and the ratio
    best_match = []

    lookup = lookup[lookup['County'] == county_name.lower()]
    for index, row in lookup.iterrows():
        #if road name and county name match, return row
        if best_match == []:
            best_match = [index, fuzz.ratio(row['Road Name'].lower(), road_name.lower())]
        elif fuzz.ratio(row['Road Name'].lower(), road_name.lower()) > best_match[1]:
            best_match = [index, fuzz.ratio(row['Road Name'].lower(), road_name.lower())]

    if best_match == []:
        return None    
    
    row = lookup.iloc[best_match[0]]

    return row
'''

df_for_model = pd.DataFrame(columns=['LIGHT', 'TIME', 'WEATHER1', 'RodwyClass', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount', 'Shape_Length'])

import datetime
import pytz

#set timezone
tz = pytz.timezone('US/Eastern')

#set datetime format to military time
fmt = '%H:%M:%S'

datetime_obj = datetime.datetime.now(tz)
current_time = datetime_obj.strftime(fmt)

current_time = int(current_time.split(':')[0])

print("time", current_time)


#generate LIGHT from 1 to 6
'''
1 Daylight
2 Dusk
3 Dawn
4 Dark - Lighted Roadway
5 Dark - Roadway Not Lighted
6 Dark - Unknown Lighting
'''
#using time, set light
if current_time >= 6 and current_time <= 18:
    LIGHT = 1
elif current_time >= 18 and current_time <= 19:
    LIGHT = 2
elif current_time >= 5 and current_time <= 6:
    LIGHT = 3
elif current_time >= 19 and current_time <= 24:
    LIGHT = 4
elif current_time >= 0 and current_time <= 5:
    LIGHT = 5
else:
    LIGHT = 6

import numpy as np

WEATHER1 = 0

#generate WEATHER1 from OpenWeatherMap
#api key
# importing requests and json
import requests, json
# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Raleigh"
API_KEY = "5bddea4829530b00cba5e0f82ae2fea3"
# upadting the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
# HTTP request
response = requests.get(URL)
# checking the status code of the request
if response.status_code == 200:
   # getting data in the json format
    data = response.json()
   # getting the main dict block
    main = data['main']

   # weather report
    report = data['weather']
    weather = report[0]['description']

    weather_id = report[0]['id']

    #if the weather code is 2xx
    if weather_id >= 200 and weather_id <= 299:
        WEATHER1 = 3
    #if the weather code is 3xx
    elif weather_id >= 300 and weather_id <= 399:
        WEATHER1 = 3
    #if the weather code is 5xx but not 511
    elif weather_id >= 500 and weather_id <= 599 and weather_id != 511:
        WEATHER1 = 3
    #if the weather code is 6xx
    elif weather_id >= 600 and weather_id <= 699 and weather_id != 611 and weather_id != 612 and weather_id != 613 and weather_id != 615 and weather_id != 616:
        WEATHER1 = 4
    #if the weather code is 7xx
    elif weather_id == 511 or weather_id == 611 or weather_id == 612 or weather_id == 613 or weather_id == 615 or weather_id == 616 or weather_id == 771:
        WEATHER1 = 6
    elif weather_id == 711 or weather_id == 721 or weather_id == 741:
        WEATHER1 = 5
    elif weather_id == 731 or weather_id == 751 or weather_id == 761 or weather_id == 762:
        WEATHER1 = 8
    elif weather_id == 781:
        WEATHER1 = 7
    elif weather_id == 800:
        WEATHER1 = 1
    elif weather_id == 801 or weather_id == 802 or weather_id == 803 or weather_id == 804:
        WEATHER1 = 2

    print(f"Weather Report: {weather}")
    print(f"Weather ID: {weather_id}")
    print(f"WEATHER1: {WEATHER1}")
else:
   # showing the error message
   print("Error in the HTTP request")



for road_name, county_name, lat, long in road_county_lat_long:

    gen_row = get_row(road_name, county_name)

    print(gen_row)


    df_look_up = df[df["Custom ID"] == gen_row['Custom ID']]   

    #get the first row
    row = df_look_up.iloc[0]

    if row is None:
        continue

    if np.isnan(row['LftShldrWidth']):
        row['LftShldrWidth'] = 5

    if np.isnan(row['RtShldrWidth']):
        row['RtShldrWidth'] = 5

    if np.isnan(row['UrbanPop']):
        row['UrbanPop'] = 6

    if np.isnan(row['ROW']):
        row['ROW'] = 73

    if np.isnan(row['SrfcWidth']):
        row['SrfcWidth'] = 24
    
    print("row------------------------------------------------------")
    print(row)

    #add to df_for_model
    df_for_model = df_for_model._append(row)


df_for_model['LIGHT'] = LIGHT
df_for_model['TIME'] = current_time
df_for_model['WEATHER1'] = WEATHER1

print(df_for_model.info())


#import the pickle model
import pickle
pickle_in = open("rtaps_controller/real_time_modeling/models/crash_severity/severity3.sav", "rb")

model = pickle.load(pickle_in)

#predict
#drop irrelevant columns
df_for_model = df_for_model.drop(['RI Class', 'RI Qualifier', 'RI Inventory', 'RI Number', 'RI County', 'Custom ID'], axis=1)

print("predicting")
prediction_probability = model.predict_proba(df_for_model)
print("done predicting", prediction_probability)




'''
LIGHT -- generate from time
TIME -- get current time
WEATHER1 -- get from OpenWeatherMap
LftShldrWidth -- already there, if not then set to 5
ROW -- already there, if not then set to 73
RtShldrWidth -- already there, if not then set to 5
UrbanPop -- already there, if not then set to 6
'''

