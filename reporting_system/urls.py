'''
URLS for the reporting system
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
    path('login_u', views.print_u, name='login_u'),

]