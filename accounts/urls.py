from django.urls import path
from .views import SignupView, Login, Logout

app_name = 'accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
