from django.urls import path
from .views import UserView, CreateUserView, GetUserView, CalculateAccidentProbabilityViewOnce

urlpatterns = [
    path('list-users', UserView.as_view()),
    path('create-user', CreateUserView.as_view()),
    path('get-user', GetUserView.as_view()),
    path('sdrive-query', CalculateAccidentProbabilityViewOnce.as_view())
]