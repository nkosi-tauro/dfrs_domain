'''
Models for the Reporting Form
'''
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



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
Vulnerability_Type_Flaw  = [
    ('', ''),
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

CHOICES = [
        ('', ''),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('Critical', 'Critical'),
]

class ReportingFormModel(models.Model):
    '''
    Reporting Form Model
    '''
    first_name = models.CharField(max_length=100, serialize=True)
    last_name = models.CharField(max_length=100, serialize=True)
    email = models.EmailField(validators=[validators.EmailValidator()], serialize=True)
    type_of_vulnerability = models.CharField(max_length=30,
                                             choices=Vulnerability_Type, serialize=True, blank=False)
    description = models.TextField(max_length=1000, serialize=True)

    def __str__(self):
        return f"{self.first_name} - {self.type_of_vulnerability}"

class FlawFormModel(models.Model):
    '''
    Reporting Form Model
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, serialize=True)
    type = models.CharField(max_length=100, choices=Vulnerability_Type_Flaw, blank=False, serialize=True)
    severity = models.CharField(max_length=10, choices=CHOICES, blank=False,serialize=True)
    description = models.TextField(blank=True, serialize=True)

    def __str__(self):
        return f"{self.type}"