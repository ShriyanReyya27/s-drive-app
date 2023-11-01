from django.shortcuts import render
from rest_framework import generics, status
from .models import User
from .models import AccidentProbability
from .serializers import UserSerializer, CreateUserSerializer, RouteAddressSerializer, AccidentProbabilitySerializer
from rest_framework.views import APIView, View
from rest_framework.response import Response


# Create your views here.
class UserView(generics.ListAPIView):
    queryset = User.objects.all()  
    serializer_class = UserSerializer

class GetUserView(APIView):
    serializer_class = UserSerializer
    lookup_url_kwarg = 'userName'
    def get(self, request, format=None):
        userName = request.GET.get(self.lookup_url_kwarg)    
        if userName != None:
            userSet = User.objects.filter(user_name=userName)
            if userSet.exists():
                data = UserSerializer(userSet[0]).data
                return(Response(data, status=status.HTTP_200_OK))
            return Response({'Bad Request': 'Room with userName:'+ self.lookup_url_kwarg +'not found'}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'Bad Request': 'URL parameter userName not found'}, status=status.HTTP_400_BAD_REQUEST) 
    
class CreateUserView(APIView):
    serializer_class = CreateUserSerializer
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        print(self.request.session.session_key)
        if serializer.is_valid():
            print(request.data)
            first_name = serializer.data.get('first_name')
            last_name = serializer.data.get('last_name')
            user_name = serializer.data.get('user_name')
            session_key = self.request.session.session_key
            
            queryset = User.objects.filter(session_key=session_key)
            if queryset.exists():
                user = queryset[0]
                user.first_name = first_name
                user.last_name = last_name
                user.user_name = user_name
                user.save(update_fields=['first_name', 'last_name', 'user_name'])
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                user = User(first_name=first_name, last_name=last_name, user_name=user_name, session_key=session_key)
                user.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid Data...'}, status=status.HTTP_400_BAD_REQUEST)        


import pandas as pd
df = pd.read_csv('api/nc20road_route_data_secondary_coded.csv')
lookup = pd.read_csv('api/SRLookUp_coded2.csv')

import datetime
import pytz

#set timezone
tz = pytz.timezone('US/Eastern')

#set datetime format to military time
fmt = '%H:%M:%S'

datetime_obj = datetime.datetime.now(tz)
current_time = datetime_obj.strftime(fmt)

current_time = int(current_time.split(':')[0])

def setLight(current_time):
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
    return LIGHT

LIGHT = setLight(current_time)

import pickle
pickle_in = open("api/severity3.sav", "rb")

model = pickle.load(pickle_in)

import requests, json
def setWeather(city):
    WEATHER1 = 1
    # base URL
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = city
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
        
        return WEATHER1

#return the row that has the same road name and county
def get_row(road_name, county_name):
    #loop through each row in lookup
    for index, row in lookup.iterrows():
        #if road name and county name match, return row
        if row['Road Name'] == road_name and row['County'] == county_name.upper():
            return row
        
    #if no match, return empty row
    row = pd.Series()
    return row

import numpy as np

def fill_nulls(row):
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

    return row

class CalculateAccidentProbabilityView(APIView):
    serializer_class = RouteAddressSerializer
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():

            routeAddressList = serializer.data
            print("ROUTE ADDRESS LIST------------------",routeAddressList)


            list_of_route_addresses = []
            df_for_model = pd.DataFrame(columns=['LIGHT', 'TIME', 'WEATHER1', 'RodwyClass', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount', 'Shape_Length', 'Lat', 'Lng'])


            for routeAddress in list_of_route_addresses:
                #first check if this has a route or an establishment
                #if there is a route, then the road name is the route
                #if there is an establishment, then split by '&' and the first part is the road name

                if routeAddress.get('route') == "":
                    road_name = routeAddress.establishment.split('&')[0]
                    #trim the trailing whitespace
                    road_name = road_name.rstrip()
                else:
                    road_name = routeAddress.get('route')

                county_name = routeAddress.get('county')

                gen_row = get_row(road_name, county_name)
                empty = pd.Series()

                if gen_row == empty:
                    continue

                lat = routeAddress.get('lat')
                lng = routeAddress.get('lng')

                

                df_look_up = df[df["Custom ID"] == gen_row['Custom ID']]
                #get the first row
                row = df_look_up.iloc[0]
                row = fill_nulls(row)

                row['Lat'] = lat
                row['Lng'] = lng
                
                df_for_model = df_for_model._append(row)

            df_for_model['LIGHT'] = LIGHT
            df_for_model['TIME'] = current_time
            df_for_model['WEATHER1'] = setWeather(routeAddressList[0].get('city'))

            latlng = df_for_model[['Lat', 'Lng']]
            df_for_model = df_for_model.drop(['RI Class', 'RI Qualifier', 'RI Inventory', 'RI Number', 'RI County', 'Custom ID'], axis=1)
            
            prediction_probabilities = model.predict_proba(df_for_model)

            for index, prediction_probability in enumerate(prediction_probabilities):
                latlng[index]['accident_probability'] = prediction_probability[0]
        

            accident_probability = AccidentProbability()

            accident_probability.lat = lat
            accident_probability.lng = lng
            accident_probability.accident_probability = 0.5

         
        return Response(AccidentProbabilitySerializer(accident_probability).data, status=status.HTTP_200_OK)
    
class CalculateAccidentProbabilityViewOriginal(APIView):
    serializer_class = RouteAddressSerializer
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():

            routeAddressList = serializer.data
            print("ROUTE ADDRESS LIST------------------",routeAddressList)           


            lat = serializer.data.get('lat')
            lng = serializer.data.get('lng')
            route = serializer.data.get('route')
            city = serializer.data.get('city')
            county = serializer.data.get('county')
            establishment = serializer.data.get('establishment')
        

            accident_probability = AccidentProbability()

            accident_probability.lat = lat
            accident_probability.lng = lng
            accident_probability.accident_probability = 0.5

         
        return Response(AccidentProbabilitySerializer(accident_probability).data, status=status.HTTP_200_OK)


class CalculateAccidentProbabilityViewOnce(APIView):
    serializer_class = RouteAddressSerializer
    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        print("is valid: ", serializer.is_valid())
        print("errors: ", serializer.errors)
        ap = AccidentProbability()
        if serializer.is_valid():

            routeAddress = serializer.data

            df_for_model = pd.DataFrame(columns=['LIGHT', 'TIME', 'WEATHER1', 'RodwyClass', 'RouteClass', 'FuncClass', 'LftShldrType', 'LftShldrWidth', 'ROW', 'RtShldrType', 'RtShldrWidth', 'SpeedLimit', 'SrfcType', 'SrfcWidth', 'TerrainType', 'UrbanPop', 'AADT', 'SU_PCT', 'MU_PCT', 'ThruLaneCount', 'Shape_Length', 'Lat', 'Lng'])
            
            if routeAddress.get('route') == "":
                    road_name = routeAddress.get('establishment').split('&')[0]
                    #trim the trailing whitespace
                    road_name = road_name.rstrip()
            else:
                road_name = routeAddress.get('route')

            
            county_name = routeAddress.get('county').split(' ')[0]

            lat = routeAddress.get('lat')
            lng = routeAddress.get('lng')

            print("road name", road_name)
            print("county name", county_name)
            print("lat", lat)
            print("lng", lng)

            gen_row = get_row(road_name, county_name) 
            if gen_row.empty == False:

                df_look_up = df[df["Custom ID"] == gen_row['Custom ID']]
                #get the first row
                row = df_look_up.iloc[0]
                row = fill_nulls(row)

                row['Lat'] = lat
                row['Lng'] = lng
                
                df_for_model = df_for_model._append(row)

                df_for_model['LIGHT'] = LIGHT
                df_for_model['TIME'] = current_time
                df_for_model['WEATHER1'] = setWeather(routeAddress.get('city'))

                #set and drop relevant data
                latlng = df_for_model[['Lat', 'Lng']]
                df_for_model = df_for_model.drop(['RI Class', 'RI Qualifier', 'RI Inventory', 'RI Number', 'RI County', 'Custom ID', 'Lat', 'Lng'], axis=1)
                
                #predict
                prediction_probability = model.predict_proba(df_for_model)
                algo_proba = prediction_probability[0][4]
                print(algo_proba)

                
                print("server side algo proba: ", algo_proba)

            else:
                algo_proba = 0
            
            #assign to object and serialize 
            ap.lat = routeAddress.get('lat')
            ap.lng = routeAddress.get('lng')
            ap.accident_probability = round(algo_proba, 2)
            ap.road_name = road_name
         
        return Response(AccidentProbabilitySerializer(ap).data, status=status.HTTP_200_OK)