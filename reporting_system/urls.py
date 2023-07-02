'''
URLS for the reporting system
'''
from django.urls import path
from django.contrib.auth import views as auth_views
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
    path("dfrsadmin/cyberdetectives/",
         views.cyberdetectiveview, name="cyberdetectiveview"),
    path("dfrsadmin/systemlogs/",
         views.systemlogsview, name="systemlogsview"),
    path("cyberdetective/update/",
         user_view.employee_update, name="employee-update"),
    path('login/', user_view.login_service, name='employee-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='homeview/logout.html'),
         name='employee-logout'),
    path("employee/<int:user_id>",views.employeeview, name="employeeview"),
    path("report/",views.publicview, name="publicview"),
    path("employee/<int:user_id>/flaw",user_view.add_flaw, name="add-flaw"),
    path("employee/<int:user_id>/remove/<int:flaw>",user_view.remove_flaw, name="remove-flaw"),
    path("employee/<int:user_id>/edit/<int:flaw>",user_view.edit_flaw, name="edit-flaw"),

]
