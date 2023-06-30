'''
Reporting System views
'''
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eventlog.models import Event
from eventlog.events import EventGroup
from .forms import ReportingFormView

# Start a new Event group
systemEvent = EventGroup()

def get_client_ip(request):
    '''
    Get Client IP address, this will be used to track users at login
    Possible Usage:
    To see if a specific IP is trying to bruteforce its way into the system
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address

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


def publicview(request):
    '''
    The General Public View
    '''
    if request.method == 'POST':
        form = ReportingFormView(request.POST)
        if form.is_valid():
            form.save()
            systemEvent.info(
                "A Public user has submitted a new vulnerability report",
                             initiator=get_client_ip(request))
        elif form.errors:
            messages.add_message(request, messages.ERROR, f"{form.errors}")
    else:
        form =ReportingFormView()
    form = ReportingFormView()
    context = {'form': form}

    return render(request,'publicview/public.html', context)
