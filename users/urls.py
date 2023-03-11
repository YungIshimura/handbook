from django.urls import path
from .views import (view_profile, update_company,
                    update_branch, delete_branch, add_branch, delete_employee_company, add_employee_company,
                    update_employee_company, delete_employee_branch, update_employee_branch, add_employee_branch)

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
    path('company/edit/<int:pk>/add_branch/', add_branch, name='add_branches'),  # добавить филиал
    path('company/branches/edit/<int:pk>/', update_branch, name='edit_branches'),  # редактировать филиал
    path('company/branches/delete/<int:pk>/', delete_branch, name='delete_branches'),  # удалить филиал
    path('company/branches/edit/<int:pk>/add_employee/', add_employee_branch, name='add_employee_branch'),
    # добавить сотрудника филиала
    path('company/branches/employee/edit/<int:pk>/', update_employee_branch, name='update_employee_branch'),
    # редактировать сотрудника филиала
    path('company/branches/employee/delete/<int:pk>/', delete_employee_branch, name='delete_employee_branch'),
    # удалить сотрудника филиала
]
