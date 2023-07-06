'''
Reporting System views
'''
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eventlog.models import Event
from eventlog.events import EventGroup
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import caches
from django import forms
from user_service.forms import EmployeeUpdateForm
from .models import VulnerabilityFormModel, ReportingForm2Model
from user_service.ratelimit import RateLimit, RateLimitExceeded
from .forms import ReportingFormView, AddVulnerabilityForm, GDPRRequestForm, RateLimitForm

import threading

# Start a new Event group
systemEvent = EventGroup()

# Django Emails tend to take a long time, thus holding up the Page 
# So by creating a new Thread we can send the email in the background so that the page can load faster
class EmailThread(threading.Thread):
    '''
    handle mutihreading for emails
    '''
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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

# ----------------------------------------STANDALONE VIEWS----------------------------------------
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
    external_reports = ReportingForm2Model.objects.all()
    internal_reports = VulnerabilityFormModel.objects.all()
    context = {
        'external_reports': external_reports,
        'internal_reports': internal_reports,
    }
    return render(request, 'adminview/admin.html', context)


@login_required(login_url='employee-login')
def employeeview(request, user_id):
    '''
    Employee View
    '''
    employee = User.objects.get(id=user_id)
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

def gdprview(request):
    '''
    The GDPR View
    '''
    if request.method == 'POST':
        form = GDPRRequestForm(request.POST)
        if form.is_valid():
            systemEvent.warning(
                f"A user with email {request.POST['email']} has submitted a data deletion request",
                initiator=get_client_ip(request))
            messages.success(
                request, 'Your Request has been submitted successfully')
        elif form.errors:
            messages.error(request, f"{form.errors}")
    else:
        form = GDPRRequestForm()
    form = GDPRRequestForm()
    context = {'form': form}

    return render(request, 'publicview/gdprview.html', context)

def gdprpolicy(request):
    '''
    The GDPR Compliance Policy View
    '''
    return render(request, 'publicview/gdprcompliance.html')


@login_required(login_url='employee-login')
def cyberdetectiveview(request):
    '''
    The Cyber Detective View
    '''
    cyberdetectives = User.objects.all()
    context = {'cyberdetectives': cyberdetectives}
    return render(request, 'adminview/employee.html', context)

# ----------------------------------------SYSTEM LOGS----------------------------------------
@login_required(login_url='employee-login')
# @cache_page(60 * 15) # Cache for 15 minutes
def systemlogsview(request):
    '''
    The System Logs View
    '''
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'adminview/eventlogs.html', context)

@login_required(login_url='employee-login')
def systemlogsdetailview(request, primary_key):
    '''
    The System Logs View
    '''
    event = Event.objects.get(id=primary_key)
    if request.method == 'POST':
        form = RateLimitForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            ip_address = event.initiator
            try:
                RateLimit(
                    key=f"{ip_address}",
                    limit=1,
                    period=60,
                    cache=caches['default'],
                ).check()
            except RateLimitExceeded as e:
                systemEvent.warning(f"User with IP: {ip_address} has been rate limitted, {e.usage} login requests failed",
                                initiator=ip_address)
                return HttpResponse(
                    f"Rate limit exceeded. You have used {e.usage} requests, limit is {e.limit}. Admin Message: {message}",
                    status=429,
            )        
            systemEvent.warning(f"You have rate limitted a User with the IP: {ip_address}",
                                initiator=request.user)
            messages.success(
                request, 'Your Rate Limit Request has been submitted successfully')
        elif form.errors:
            messages.error(request, f"{form.errors}")
    else:
        form = RateLimitForm()
    form = RateLimitForm()  
    context = {'event': event,
               'form': form}
    return render(request, 'adminview/eventlogsdetail.html', context)

# ----------------------------------------REPORTS----------------------------------------
@login_required(login_url='employee-login')
def reportsdetail(request, primary_key):
    '''
    Public Reports Detail View
    '''
    report = ReportingForm2Model.objects.get(id=primary_key)
    context = {'report': report}
    return render(request, 'adminview/reportsdetail.html', context)

@login_required(login_url='employee-login')
def reports_delete(request, primary_key):
    '''
    This will allow an admin to delete a public vulnerability report
    '''
    report = ReportingForm2Model.objects.get(id=primary_key)
    if request.method=='POST':
        report.delete()
        systemEvent.warning(f"Report deleted: {report}", initiator=request.user)
        return redirect('adminview')
    context = {'report': report}
    return render(request, 'adminview/reportsdelete.html', context)

@login_required(login_url='employee-login')
def reports_update(request, primary_key):
    '''
    This will allow an admin to update a public vulnerability report
    They wont be able to modify any data, just mark the report as fixed or unfixed
    '''
    report = ReportingForm2Model.objects.get(id=primary_key)
    if request.method == 'POST':
        form = ReportingFormView(request.POST, instance=report)
        form.fields = {'status': form.fields['status']}
        if form.is_valid():
            status = form.save(commit=False)
            status.status = form.cleaned_data['status']
            form.save()

            # Email Functionality
            subject = 'Vulnerability Report Update'
            message = f'Your Vulnerability Report Status has been updated\n Status: {report.status}'
            email = EmailMessage(subject, message, from_email='nkosilati23@gmail.com', to=[report.email])
            # Initiate Thread
            EmailThread(email).start()
            
            systemEvent.info(f"The Public Report {report} has been updated.",
                             initiator=request.user)
            return redirect('adminview')
    else:
        form = ReportingFormView(instance=report)
        form.fields = {'status': form.fields['status']}
        form.fields['status'].widget = forms.Select()
    context = {'form': form,
               'request': request.user}
    return render(request, 'adminview/reportsupdate.html', context)

@login_required(login_url='employee-login')
def internalreportsdetail(request, primary_key):
    '''
    Public Reports Detail View
    '''
    report = VulnerabilityFormModel.objects.get(id=primary_key)
    context = {'report': report}
    return render(request, 'adminview/internalreports_detail.html', context)

@login_required(login_url='employee-login')
def internalreports_update(request, primary_key):
    '''
    This will allow an admin to update a public vulnerability report
    They wont be able to modify any data, just mark the report as fixed or unfixed
    '''
    report = VulnerabilityFormModel.objects.get(id=primary_key)
    if request.method == 'POST':
        form = AddVulnerabilityForm(request.POST, instance=report)
        form.fields = {'status': form.fields.get('status')}
        if form.is_valid():
            status = form.save(commit=False)
            status.status = form.cleaned_data['status']
            form.save()
            systemEvent.info(f"The Public Report {report} has been updated.",
                             initiator=request.user)
            return redirect('adminview')
    else:
        form = AddVulnerabilityForm(instance=report)
        form.fields = {'status': form.fields.get('status')}
        form.fields['status'].widget = forms.Select()
    context = {'form': form,
               'request': request.user}
    return render(request, 'adminview/internal_reportsupdate.html', context)

# ----------------------------------------EMPLOYEE ROUTES----------------------------------------
@login_required(login_url='employee-login')
def employeeupdate(request, user_id):
    '''
    This will allow an admin to update an employee
    '''
    employee = User.objects.get(id=user_id)
    if request.method == 'POST':
        # instance=request.user will pass through the user data into the input fields
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            systemEvent.info(f"{employee} has updated their profile.",
                             initiator=request.user)
            return redirect('employeeview', user_id=user_id)
    else:
        form = EmployeeUpdateForm(instance=employee)
    context = {'form': form,
               'user_id': user_id}
    return render(request, 'employeeview/employeeupdate.html', context)


@login_required(login_url='employee-login')
def add_flaw(request, user_id):
    '''
    Service to add the flaws, that have been identified by the employee. 
    This will allow employees to track breaches.
    '''
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
    else:
        initial_data = {'user_id': user_id}
        form = AddVulnerabilityForm(initial=initial_data)

    context = {
        'form': form,
        'user_id': user_id,
    }
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
