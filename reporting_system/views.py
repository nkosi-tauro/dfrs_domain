'''
Reporting System views
'''
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eventlog.models import Event
from eventlog.events import EventGroup
from .models import VulnerabilityFormModel
from .forms import ReportingFormView, AddVulnerabilityForm

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
    return render(request, 'homeview/home.html')


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
    return render(request, 'adminview/admin.html', context)


@login_required(login_url='employee-login')
def employeeview(request, user_id):
    '''
    Employee View
    '''
    employee = User.objects.all()
    flaws_context = VulnerabilityFormModel.objects.filter(
        user_id=user_id)  # Query the database for flaws related to the user
    context = {
        'employee': employee,
        "user_id": user_id,
        "flaws": flaws_context
    }
    return render(request, 'employeeview/employee.html', context)


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
            messages.success(
                request, 'Your Report has been submitted successfully')
        elif form.errors:
            messages.error(request, f"{form.errors}")
    else:
        form = ReportingFormView()
    form = ReportingFormView()
    context = {'form': form}

    return render(request, 'publicview/public.html', context)


@login_required(login_url='employee-login')
def cyberdetectiveview(request):
    '''
    The Cyber Detective View
    '''
    cyberdetectives = User.objects.all()
    context = {'cyberdetectives': cyberdetectives}
    return render(request, 'adminview/employee.html', context)


@login_required(login_url='employee-login')
def systemlogsview(request):
    '''
    The System Logs View
    '''
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'adminview/eventlogs.html', context)


@login_required(login_url='employee-login')
def add_flaw(request, user_id):
    '''
    Service to add the flaws, that have been identified by the employee. 
    This will allow employees to track breaches.
    '''
    form = AddVulnerabilityForm()
    context = {
        'form': form,
        'user_id': user_id,
    }
    if request.method == 'POST':
        form = AddVulnerabilityForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id_id = user_id
            obj.save()
            systemEvent.info(
                f"Cyberdetective {request.user} has submitted a new vulnerability report",
                initiator=request.user)
            return redirect('employeeview', user_id=user_id)
        context["not_valid"] = 1
    return render(request, 'employeeview/addFlaw.html', context)


@login_required(login_url='employee-login')
def remove_flaw(request, user_id, flaw):
    '''
    Service to delete the chosen flaw.
    '''
    if request.method == 'POST':
        # flaw = AddVulnerabilityForm.objects.get(id=flaw)
        # Query the database for flaws related to the user
        flaw = VulnerabilityFormModel.objects.filter(id=flaw)
        flaw.delete()
        # Redirect back to employee view
        return redirect('employeeview', user_id)

    context = {"user_id": user_id,
               "flaw_id": flaw
               }
    return render(request, 'employeeview/remove_flaw.html', context=context)


@login_required(login_url='employee-login')
def edit_flaw(request, user_id, flaw):
    '''
    Service to modify the chosen flaw.
    '''
    context = {"user_id": user_id,
               "flaw_id": flaw}
    flaw_record = VulnerabilityFormModel.objects.get(id=flaw)
    if request.method == 'POST':
        form = AddVulnerabilityForm(request.POST, instance=flaw_record)
        print(request)
        if form.is_valid():
            type_flaw = request.POST["type"]
            severity = request.POST["severity"]
            description = request.POST["description"]
            VulnerabilityFormModel.objects.filter(id=flaw).update(
                type=type_flaw , severity=severity, description=description)
            # Redirect back to employee view
            return redirect('employeeview', user_id)
        context["not_valid"] = 1
    form = AddVulnerabilityForm(instance=flaw_record)
    print(request.user)
    context['form'] = form
    return render(request, 'employeeview/edit_flaw.html', context)
