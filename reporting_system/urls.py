'''
URLS for the reporting system
'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeview, name='homeview'),
]