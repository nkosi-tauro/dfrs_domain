'''
URLS for the reporting system
'''
from django.urls import path
from user_service import views as user_view
from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('dfrsadmin', views.adminview, name='adminview'),
    path("cyberdetective/<int:primary_key>", user_view.employee_detail, name="employee-detail"),
    path("cyberdetective/delete/<int:primary_key>",
         user_view.employee_delete, name="employee-delete"),
    path("cyberdetective/update/",
         user_view.employee_update, name="employee-update"),
]
