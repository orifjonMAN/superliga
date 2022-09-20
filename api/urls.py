from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ClubListAPIView,
    PlayerListAPIView,
    MatchListAPIView,
    MatchDetailAPIView,
    MatchFinishAPIView,
    ResultListAPIView,
    UserRegisterAPIView,
    # ExampleView
    UserLoginAPIView
)

app_name = 'api'
urlpatterns = [
    path('clubs/', ClubListAPIView.as_view(), name='clubs'),
    path('players/', PlayerListAPIView.as_view(), name='players'),
    path('match/', MatchListAPIView.as_view(), name='match'),
    path('match/<str:pk>/', MatchDetailAPIView.as_view(), name='detail'),
    path('result/', MatchFinishAPIView.as_view(), name='result'),
    path('table/', ResultListAPIView.as_view(), name='table'),

    # account
    # path('register/', UserRegisterAPIView.as_view(), name='register'),
    # path('login/', UserLoginAPIView.as_view(), name='login')
]

