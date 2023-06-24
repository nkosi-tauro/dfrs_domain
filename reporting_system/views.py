'''
Reporting System views
'''
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def homeview(request):
    '''
    The Landing Page
    '''
    return render(request,'homeview/home.html')

@login_required
def adminview(request):
    '''
    Admin View
    '''
    cyberdetectives = User.objects.all()
    context = {'cyberdetectives': cyberdetectives}
    return render(request,'adminview/admin.html', context)

@login_required
def employeeview(request):
    '''
    Employee View
    '''
    employee = User.objects.all()
    context = {'employee': employee}
    return render(request,'employeeview/employee.html', context)
