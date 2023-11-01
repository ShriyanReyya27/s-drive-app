from django.db import models
import string
import random
import datetime

def generate_id():
    length = 20
    while True:
        user_id = ''.join(random.choices(string.ascii_uppercase, k=length))
        if User.objects.filter(user_id=user_id).count() == 0:
            break

    return user_id

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    user_name = models.CharField(max_length=50, default="", unique=True)
    user_id = models.CharField(max_length=20, default=generate_id, primary_key=True)
    session_key = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)   

class RouteAddress(models.Model):
    lat = models.FloatField(max_length=50, default=0.0)
    lng = models.FloatField(max_length=50, default=0.0)
    route = models.CharField(max_length=50, default=None, blank = True, null = True)
    city = models.CharField(max_length=50, default=None, blank = True, null = True)
    county = models.CharField(max_length=50, default=None, blank = True, null = True)
    establishment = models.CharField(max_length=50, default=None, blank = True, null = True)

class AccidentProbability(models.Model):
    lat = models.FloatField(max_length=50, default=0.0)
    lng = models.FloatField(max_length=50, default=0.0)
    accident_probability = models.FloatField(max_length=50, default=0.0)
    road_name = models.CharField(max_length=50, default="")