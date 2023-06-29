'''
Forms related to the user service
'''
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

class EmployeeRegisterForm(UserCreationForm):
    '''
    Creating a new form for employee registration
    '''
    # Include the email field with the Default EmailValidator
    email = forms.EmailField(required=True, validators=[validators.EmailValidator()])

    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EmployeeUpdateForm(forms.ModelForm):
    '''
    Creating a form for employee update
    '''
    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = User
        fields = ['username', 'email']


# import the standard Django Forms
# from built-in library
	
# creating a form
class AddFlawForm(forms.Form):
    type = forms.CharField(max_length = 200, required=True)
    CHOICES = [
        ('1', 'Low'),
        ('2', 'Medium'),
        ('3', 'Critical'),
    ]
    severity = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES, 
    )
    description = forms.CharField(max_length = 200, required=False)

