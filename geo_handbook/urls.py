from django.urls import path
from .views import view_index, view_about


app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index'),
    path('about/', view_about, name='about')
]