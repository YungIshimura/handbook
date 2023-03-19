from django.urls import path
from .views import (view_profile, update_company, delete_branch, delete_employee_company, add_employee_company,
                    update_employee_company, get_employee_data, add_branch_company, update_branch_company,
                    get_branche_data,
                    delete_license_company, add_license_company, get_license_data, update_license_company,
                    add_contact_phone_company, delete_contact_phone_company,
                    get_contact_phone_data, update_contact_phone_company, delete_contact_email_company,
                    add_contact_email_company, get_contact_email_data, update_contact_email_company,
                    delete_contact_url_company, add_contact_url_company, get_contact_url_data,
                    update_contact_url_company, update_data_company)

app_name = 'users'

urlpatterns = [
    path('profile/', view_profile, name='profile'),

    path('company/edit/<int:pk>/', update_company, name='edit_company'),  # редактировать данные компании
    path('company/edit/<int:pk>/add_employee/', add_employee_company, name='add_employee_company'),
    # добавить сотрудника компании
    path('company/employee/edit/<int:pk>/', update_employee_company, name='update_employee_company'),
    # редактировать сотрудника компании
    path('company/employee/delete/<int:pk>/', delete_employee_company, name='delete_employee_company'),
    # удалить сотрудника компании
    path('company/edit/<int:pk>/add_branch/', add_branch_company, name='add_branches'),  # добавить филиал
    path('company/branches/edit/<int:pk>/', update_branch_company, name='update_branches'),  # редактировать филиал
    path('company/branches/delete/<int:pk>/', delete_branch, name='delete_branches'),  # удалить филиал
    # удалить сотрудника филиала
    path('company/edit/<int:pk>/add_license/', add_license_company, name='add_license'),  # добавить лицензию
    path('company/license/edit/<int:pk>/', update_license_company, name='update_license'),  # редактировать лицензию
    path('company/license/delete/<int:pk>/', delete_license_company, name='delete_license'),  # удалить лицензию
    path('company/edit/<int:pk>/add_contact_phone/', add_contact_phone_company, name='add_contact_phone'),
    # добавить контактные телефоны компании
    path('company/contact_phone/edit/<int:pk>/', update_contact_phone_company, name='update_contact_phone'),
    # редактировать номера телефонов компании
    path('company/contact_phone/delete/<int:pk>/', delete_contact_phone_company, name='delete_contact_phone'),
    # удалить контактные номера компании
    path('company/edit/<int:pk>/add_contact_email/', add_contact_email_company, name='add_contact_email'),
    # добавить контактный email компании
    path('company/contact_email/edit/<int:pk>/', update_contact_email_company, name='update_contact_email'),
    # редактировать email компании
    path('company/contact_email/delete/<int:pk>/', delete_contact_email_company, name='delete_contact_email'),
    # удалить контактные номера компании
    path('company/edit/<int:pk>/add_contact_url/', add_contact_url_company, name='add_contact_url'),
    # добавить контактный url компании
    path('company/contact_url/edit/<int:pk>/', update_contact_url_company, name='update_contact_url'),
    # редактировать url компании
    path('company/contact_url/delete/<int:pk>/', delete_contact_url_company, name='delete_contact_url'),
    # удалить контактный url компании
    path('company/edit/<int:pk>/update_data_company/', update_data_company, name='update_data_company'),
    # обновить данные компании
  
    path('get_employee_data/<int:pk>/', get_employee_data, name='get_employee_data'),  # получить данные о сотруднике
    path('get_branche_data/<int:pk>/', get_branche_data, name='get_branches_data'),  # получить данные о филиале
    path('get_license_data/<int:pk>/', get_license_data, name='get_license_data'),  # получить данные о лицензии
    path('get_contact_phone_data/<int:pk>/', get_contact_phone_data, name='get_contact_phone_data'),
    # получить данные о номерах телефонов
    path('get_contact_email_data/<int:pk>/', get_contact_email_data, name='get_contact_email_data'),
    # получить данные о email
    path('get_contact_url_data/<int:pk>/', get_contact_url_data, name='get_contact_url_data'),
    # получить данные о url
]
