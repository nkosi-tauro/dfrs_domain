from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flaw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    severity = models.CharField(max_length=1, choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'Critical')])
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.type