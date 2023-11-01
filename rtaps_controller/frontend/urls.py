from django.urls import path
from .views import index

urlpatterns = [
    path('home',index),
    path('createProfile', index),
    path('roadSafetyAnalyzer/<str:userName>', index),
    path('roadSafetyMap', index),
    path('roadSafetyMap/<str:userName>', index)
]