'''
URLS for the reporting system
'''
from django.urls import path
from user_service import views as user_view
from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('dfrsadmin', views.adminview, name='adminview'),
    path("dfrsadmin/register/cyberdetective/",
         user_view.register_employee, name="register-employee"),
    path("dfrsadmin/cyberdetective/<int:primary_key>",
         user_view.employee_detail, name="employee-detail"),
    path("dfrsadmin/cyberdetective/delete/<int:primary_key>",
         user_view.employee_delete, name="employee-delete"),
    path("cyberdetective/update/",
         user_view.employee_update, name="employee-update"),
    path('login', views.loginPopup, name='login'),
    path("employee",views.employeeview, name="employeeview"),
]
