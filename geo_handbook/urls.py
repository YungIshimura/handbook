from django.urls import path
from .views import view_index, view_about, view_select, view_selected_region, view_card, view_application


app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index'),
    path('about/', view_about, name='about'),
    path('select/', view_select, name='select'),
    path('selected_region/', view_selected_region, name='region'),
    path('card/', view_card, name='card'),
    path('application/', view_application, name='application'),
]