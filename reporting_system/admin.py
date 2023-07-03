'''
Register your custom models here.
'''
from django.contrib import admin
from .models import ReportingFormModel, VulnerabilityFormModel

# Register your models here.
admin.site.register(ReportingFormModel)
admin.site.register(VulnerabilityFormModel)
