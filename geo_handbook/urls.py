from django.urls import path
from .views import (view_about, view_selected_region, view_application,
                    view_enter_details_company, view_settings_profile, view_index, view_sign_up_user,
                    view_sign_up_company    , view_card_layer, view_card, view_profile, view_rates)

app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index'),
    path('sign_up_user/', view_sign_up_user, name='sign_up_user'),
    path('sign_up_company/', view_sign_up_company, name='sign_up_company'),
    path('card_layer/', view_card_layer, name='card_layer'),
    path('about/', view_about, name='about'),
    path('selected_region/<int:city_id>/', view_selected_region, name='region'),
    path('card/<int:company_id>/', view_card, name='card'),
    path('application/', view_application, name='application'),
    path('enter_details_company/', view_enter_details_company, name='enter_details_company'),
    path('settings_profile/', view_settings_profile, name='settings_profile'),
    path('profile/', view_profile, name='profile'),
    path('rates/', view_rates, name='rates')
]
