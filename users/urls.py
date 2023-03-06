from django.urls import path
from .views import view_profile

app_name = 'users'

urlpatterns = [
    path('profile/',view_profile, name='profile' )
]