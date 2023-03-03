from django.contrib import admin
from django.urls import path
from .views import view_index, view_sign_up_user

app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index'),
    path('sign_up_user/', view_sign_up_user, name='sign_up_user')
]
