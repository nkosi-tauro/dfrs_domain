'''
URLS for the reporting system
'''
from django.urls import path
from django.contrib.auth import views as auth_views
from user_service import views as user_view
from . import views

urlpatterns = [
     # Home Route
    path('', views.homeview, name='homeview'),
     # Admin Routes
    path('dfrsadmin', views.adminview, name='adminview'),
    path(f'dfrsadmin/reports/<int:primary_key>',
         views.reportsdetail, name='reports-detail'),
    path("dfrsadmin/reports/delete/<int:primary_key>",
         views.reports_delete, name="reports-delete"),
    path("dfrsadmin/register/cyberdetective/",
         user_view.register_employee, name="register-employee"),
    path("dfrsadmin/cyberdetective/<int:primary_key>",
         user_view.employee_detail, name="employee-detail"),
    path("dfrsadmin/cyberdetective/delete/<int:primary_key>",
         user_view.employee_delete, name="employee-delete"),
    path("dfrsadmin/cyberdetectives/",
         views.cyberdetectiveview, name="cyberdetectiveview"),
    path("dfrsadmin/cyberdetective/update/<int:primary_key>",
         user_view.employee_update, name="employee-update"),
    path("dfrsadmin/systemlogs/",
         views.systemlogsview, name="systemlogsview"),
    path("dfrsadmin/systemlogs/<int:primary_key>",
         views.systemlogsdetailview, name="systemlogsdetailview"),
     # Login/Logout Routes
    path('login/', user_view.login_service, name='employee-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='homeview/logout.html'),
         name='employee-logout'),
     # Employee Routes
    path("employee/<int:user_id>",views.employeeview, name="employeeview"),
    path("employee/<int:user_id>/flaw",views.add_flaw, name="add-flaw"),
    path("employee/<int:user_id>/remove/<int:flaw>",views.remove_flaw, name="remove-flaw"),
    path("employee/<int:user_id>/edit/<int:flaw>",views.edit_flaw, name="edit-flaw"),
     # Public Routes
    path("report/",views.publicview, name="publicview"),
    path("gdpr-delete/",views.gdprview, name="gdprview"),

]
