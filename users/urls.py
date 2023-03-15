from django.urls import path
from .views import (view_profile, update_company, delete_branch, delete_employee_company, add_employee_company,
                    update_employee_company, delete_employee_branch, update_employee_branch, add_employee_branch,
                    get_employee_data, add_branch_company, edit_branch_company, get_branche_data)

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
    path('company/edit/<int:pk>/add_branch/', add_branch_company, name='add_branches_company'),  # добавить филиал
    path('company/branches/edit/<int:pk>/', edit_branch_company, name='edit_branches'),  # редактировать филиал
    path('company/branches/delete/<int:pk>/', delete_branch, name='delete_branches'),  # удалить филиал
    path('company/branches/edit/<int:pk>/add_employee/', add_employee_branch, name='add_employee_branch'),
    # добавить сотрудника филиала
    path('company/branches/employee/edit/<int:pk>/', update_employee_branch, name='update_employee_branch'),
    # редактировать сотрудника филиала
    path('company/branches/employee/delete/<int:pk>/', delete_employee_branch, name='delete_employee_branch'),
    # удалить сотрудника филиала
    path('get_employee_data/<int:pk>/', get_employee_data, name='get_employee_data'),  # получить данные о сотруднике
    path('get_branche_data/<int:pk>/', get_branche_data, name='get_branches_data'),  # получить данные о филиале
]
