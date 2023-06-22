'''
Forms related to the user service
'''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmployeeRegisterForm(UserCreationForm):
    '''
    Creating a new form for employee registration
    '''
    # Include the email field into the default form
    email = forms.EmailField()

    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = User
        fields = ['username', 'email', 'password1', 'password2']
