'''
Reporting System Forms

'''
from django import forms
from django.core import validators
from .models import ReportingForm2Model, VulnerabilityFormModel


class ReportingFormView(forms.ModelForm):
    '''
    Reporting Form
    '''
    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = ReportingForm2Model
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.HiddenInput()  # Hide the status field by default

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        if status == 'fixed':
            self.fields['status'].widget = forms.TextInput()  # Display the status field if it's marked as fixed
        return cleaned_data

class AddVulnerabilityForm(forms.ModelForm):
    '''
    Creating a form to add a Vulnerability
    '''
    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = VulnerabilityFormModel
        fields = ['type', 'severity', 'description']

class GDPRRequestForm(forms.Form):
    '''
    GDPR Request Form
    '''
    email = forms.EmailField(max_length=100, validators=[validators.EmailValidator()])
    message = forms.CharField(max_length=200)

class RateLimitForm(forms.Form):
    '''
    Rate Limit Form
    '''
    message = forms.CharField(max_length=200)