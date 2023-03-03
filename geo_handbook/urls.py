from django.contrib import admin
from django.urls import path
from .views import view_index


app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index')
]