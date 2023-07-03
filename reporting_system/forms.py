'''
Reporting System Forms

'''
from django import forms
from .models import ReportingFormModel, VulnerabilityFormModel

class ReportingFormView(forms.ModelForm):
    '''
    Reporting Form
    '''
    class Meta:
        '''
        This class is used to set the model we want to interact with 
        and fields that will be in the form
        '''
        model = ReportingFormModel
        fields = ['first_name', 'last_name', 'email', 'type_of_vulnerability', 'description']

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
