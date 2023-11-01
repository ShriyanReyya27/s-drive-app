#loop through every line in county_codes.txt
import pandas as pd
df = pd.read_csv('csv_files/north_carolina/nc20road_route_data_secondary.csv')
lookup = pd.read_csv('csv_files/north_carolina/SRLookUp_coded2.csv')

#DO NOT MODIFY SRLOOKUP CODED 2----------------------------------------------------------

county_codes = open('congressional_app/county_codes.txt', 'r')
county_code_dict = {}

for line in county_codes:
    #split line into list
    line_list = line.split()
    #get county code
    county_code = str(line_list[0])

    #get county name
    for i in range(1, len(line_list)):
        if i == 1:
            county_name = line_list[i].lower()
        else:
            county_name = county_name + ' ' + line_list[i].lower()
    
    #add to dictionary
    county_code_dict[county_name] = county_code

#print every entry and key
for key, value in county_code_dict.items():
    print(key, value)


#add column called county code in lookup
#loop through each row and add county code
for index, row in lookup.iterrows():
    #get county name
    county_name = row['County']

    #format county name with capital first letter
    county_name = county_name.lower()

    #get county code
    county_code = str(county_code_dict[county_name])
    #add to df
    #make sure that it is 3 digits when being added
    road_number = str(row['Road Number'])
    id = road_number + county_code

    
    lookup.at[index, 'custom id'] = id
    print(lookup.at[index, 'custom id'])
    

#save to csv
lookup.to_csv('csv_files/north_carolina/SRLookUp_coded4.csv', index=False)
