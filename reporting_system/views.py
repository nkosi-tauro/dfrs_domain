'''
Reporting System views
'''
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from eventlog.models import Event


# Create your views here.
def homeview(request):
    '''
    The Landing Page
    '''
    return render(request,'homeview/home.html')

@login_required(login_url='employee-login')
def adminview(request):
    '''
    Admin View
    '''
    cyberdetectives = User.objects.all()
    events = Event.objects.all()
    context = {
        'cyberdetectives': cyberdetectives,
        'events': events,
        }
    return render(request,'adminview/admin.html', context)

@login_required(login_url='employee-login')
def employeeview(request, primary_key):
    '''
    Employee View
    '''
    # If you want to get the user object by primary key
    # .all() will return a list of all objects(users)
    # employee = User.objects.get(id=primary_key)
    employee = User.objects.all()

    context = {
        'employee': employee,
        }

    return render(request,'employeeview/employee.html', context)
