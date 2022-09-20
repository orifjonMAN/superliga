from django.urls import path
from .views import (StandingsView,
                    MatchView,
                    SetResultView,
                    FinishedMatchView,
                    ClubPlayers,
                    TopScorer,
                    SetGoals,
                    MatchDetail,
                    )
app_name='clubs'
urlpatterns = [
    path('s/', StandingsView.as_view(), name='standing'),
    path('m/', MatchView.as_view(), name='matches'),
    path('f/', FinishedMatchView.as_view(), name='finished'),
    path('set_result/<str:pk>/', SetResultView.as_view(), name='set_result'),
    path('p/<str:pk>/', ClubPlayers.as_view(), name='players'),
    path('t/', TopScorer.as_view(), name='top'),
    path('g/<str:pk>/', SetGoals.as_view(), name='goals'),
    path('d/<str:pk>', MatchDetail.as_view(), name='detail'),
]
