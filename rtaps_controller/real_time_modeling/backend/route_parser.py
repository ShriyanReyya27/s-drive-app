import pandas as pd

df = pd.read_csv('csv_files/north_carolina/nc20road.csv')

#add 'RI Class' column, 'RI Qualifier' column, 'RI Inventory' column, 'RI Number' column, 'RI County' column
#RI Class is the first character of route number
#RI Qualifier is the second character of route number
#RI Inventory is the third character of route number
#RI Number is the 5th through 8th characters of route number
#RI County is the 9th through 11th characters of route number

#loop through each row
for index, row in df.iterrows():
    #get route number
    route_number = str(row['RouteID'])
    #get RI Class
    RI_class = route_number[0]
    #get RI Qualifier
    RI_qualifier = route_number[1]
    #get RI Inventory
    RI_inventory = route_number[2]
    #get RI Number
    RI_number = route_number[4]+route_number[5]+route_number[6]+route_number[7]
    #get RI County
    RI_county = route_number[8]+route_number[9]+route_number[10]
    #add to df
    df.at[index, 'RI Class'] = RI_class
    df.at[index, 'RI Qualifier'] = RI_qualifier
    df.at[index, 'RI Inventory'] = RI_inventory
    df.at[index, 'RI Number'] = RI_number
    df.at[index, 'RI County'] = RI_county

print(df.head())

df.to_csv('csv_files/north_carolina/nc20road_route_data.csv', index=False)