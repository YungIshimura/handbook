from django.urls import path
from .views import (view_about, view_select, view_selected_region, view_application,
                    view_enter_details_company, view_settings_profile, view_index, view_sign_up_user,
                    view_sign_up_company, view_select_city, view_search, view_card_layer, company_update,
                    update_branch, delete_branch, add_branch, delete_employee_company, add_employee_company,
                    update_employee_company, delete_employee_branch, update_employee_branch, add_employee_branch,
                    view_card, view_profile, view_rates)

app_name = 'geo_handbook'

urlpatterns = [
    path('', view_index, name='index'),
    path('sign_up_user/', view_sign_up_user, name='sign_up_user'),
    path('sign_up_company/', view_sign_up_company, name='sign_up_company'),
    path('select_city/', view_select_city, name='select_city'),
    path('search/', view_search, name='search'),
    path('card_layer/', view_card_layer, name='card_layer'),
    path('about/', view_about, name='about'),
    path('select/', view_select, name='select'),
    path('selected_region/', view_selected_region, name='region'),
    path('card/<int:company_id>/', view_card, name='card'),
    path('application/', view_application, name='application'),
    path('enter_details_company/', view_enter_details_company, name='enter_details_company'),
    path('settings_profile/', view_settings_profile, name='settings_profile'),
    path('profile/', view_profile, name='profile'),
    path('rates/', view_rates, name='rates'),

    path('company/edit/<int:pk>/', company_update, name='edit_company'),
    path('branches/edit/<int:pk>/', update_branch, name='edit_branches'),
    path('branches/delete/<int:pk>/', delete_branch, name='delete_branches'),
    path('company/edit/<int:pk>/add_branch/', add_branch, name='add_branches'),

    path('company/employee/delete/<int:pk>/', delete_employee_company, name='delete_employee_company'),
    path('company/employee/edit/<int:pk>/', update_employee_company, name='update_employee_company'),
    path('company/edit/<int:pk>/add_employee/', add_employee_company, name='add_employee_company'),

    path('branches/employee/delete/<int:pk>/', delete_employee_branch, name='delete_employee_branch'),
    path('branches/employee/edit/<int:pk>/', update_employee_branch, name='update_employee_branch'),
    path('branches/edit/<int:pk>/add_employee/', add_employee_branch, name='add_employee_branch'),
]
