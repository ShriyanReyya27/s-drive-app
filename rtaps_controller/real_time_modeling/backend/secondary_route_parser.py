import pandas as pd
df = pd.read_csv('csv_files/north_carolina/nc20road_route_data_secondary.csv')

#create a column called Custom ID in df that is the last 7 digits of RouteID
for index, row in df.iterrows():
    #get route id
    route_id = str(row['RouteID'])
    #get last 7 digits
    route_id = route_id[-7:]
    #add to df
    df.at[index, 'Custom ID'] = route_id

#save to csv
df.to_csv('csv_files/north_carolina/nc20road_route_data_secondary_custom.csv', index=False)