from rest_framework import serializers
from .models import User
from .models import RouteAddress
from .models import AccidentProbability

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'user_name','session_key', 'created_at']

#Serializer for the user request from the UI
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name']        

class RouteAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAddress
        fields = ['lat', 'lng', 'route', 'city', 'county', 'establishment']

class AccidentProbabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccidentProbability
        fields = ['lat', 'lng', 'accident_probability', 'road_name']