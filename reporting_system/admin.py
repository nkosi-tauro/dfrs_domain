'''
Register your custom models here.
'''
from django.contrib import admin
from .models import ReportingForm2Model, VulnerabilityFormModel

# Register your models here.
admin.site.register(ReportingForm2Model)
admin.site.register(VulnerabilityFormModel)
