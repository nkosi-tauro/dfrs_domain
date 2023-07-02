from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create your models here.

#class Flaww(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    type = models.CharField(max_length=200)
#    severity = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('Critical', 'Critical')])
#    description = models.CharField(max_length=200)
#    def __str__(self):
#        return self.type




CHOICES = [
        ('', ''),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('Critical', 'Critical'),
]


Vulnerability_Type  = [
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


def validate_choice(value):
    if value == 1:        
        raise ValidationError('severity type not selected')

class FlawFormModel(models.Model):
    '''
    Reporting Form Model
    '''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=Vulnerability_Type, blank=False)
    severity = models.CharField(max_length=10, choices=CHOICES, blank=False,validators=[validate_choice])
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.type