'''
Models for the Reporting Form
'''
from django.db import models
from django.core import validators

# Create your models here.
Vulnerability_Type  = [
    ('Injection', 'Injection'),
    ('Broken Authentication', 'Broken Authentication'),
    ('Sensitive data exposure', 'Sensitive data exposure'),
    ('XML External Entities (XXE)', 'XML External Entities (XXE)'),
    ('Security misconfigurations', 'Security misconfigurations'),
    ('Cross Site Scripting (XSS)', 'Cross Site Scripting (XSS)'),
    ('Broken Access control', 'Broken Access control'),
    ('Insecure Deserialization', 'Insecure Deserialization'),
    ('Availability', 'Availability'),
    ('Integrity', 'Integrity'),
    ('Confidentiality', 'Confidentiality'),
]

class ReportingFormModel(models.Model):
    '''
    Reporting Form Model
    '''
    first_name = models.CharField(max_length=100, serialize=True)
    last_name = models.CharField(max_length=100, serialize=True)
    email = models.EmailField(validators=[validators.EmailValidator()], serialize=True)
    type_of_vulnerability = models.CharField(max_length=30,
                                             choices=Vulnerability_Type, serialize=True, blank=True)
    description = models.TextField(max_length=1000, serialize=True)

    def __str__(self):
        return f"{self.first_name} - {self.type_of_vulnerability}"
