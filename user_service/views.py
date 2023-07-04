'''
User Service views
'''
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from eventlog.events import EventGroup
from .forms import EmployeeRegisterForm, EmployeeUpdateForm

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

@login_required(login_url='employee-login')
def register_employee(request):
    '''
    So this will allow an admin to register an employee(new user)
    Without having to use the django admin dashboard
    '''
    if request.method == 'POST':
        # This will take the form inputs (username, email, password)
        form = EmployeeRegisterForm(request.POST)
        email= request.POST.get('email')
        # This will check if the inputs are valid based on the contraints
        if form.is_valid():
            form.save()
            systemEvent.info(f"New employee registered: {form.cleaned_data['username']}",
                             initiator=request.user)
            # This will redirect back to the admin view
            return redirect('adminview')
        elif form.errors:
            # This will display the error messages
            if User.objects.filter(username=form.fields['username']).exists():
                messages.add_message(request, messages.ERROR, 'Username already exists')
            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Email already exists')
            messages.add_message(request, messages.ERROR, f"{form.errors}")
    else:
        form = EmployeeRegisterForm()
    form = EmployeeRegisterForm()
    context = {'form': form}
    return render(request, 'adminview/register_employee.html', context)

@login_required(login_url='employee-login')
def employee_detail(request, primary_key):
    '''
    This will allow an admin to view a specific employee and edit or delete it
    '''
    employee = User.objects.get(id=primary_key)
    context = {'employee': employee}
    return render(request, 'adminview/employee_detail.html', context)

@login_required(login_url='employee-login')
def employee_delete(request, primary_key):
    '''
    This will allow an admin to delete an employee
    '''
    employee = User.objects.get(id=primary_key)
    if request.method=='POST':
        employee.delete()
        systemEvent.warning(f"Employee deleted: {employee}", initiator=request.user)
        return redirect('cyberdetectiveview')
    context = {'employee': employee}
    return render(request, 'adminview/employee_delete.html', context)

@login_required(login_url='employee-login')
def employee_update(request, primary_key):
    '''
    This will allow an admin to update an employee
    '''
    employee = User.objects.get(id=primary_key)
    print(employee)
    if request.method == 'POST':
        # instance=request.user will pass through the user data into the input fields
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            systemEvent.info(f"{employee}'s profile has been updated.",
                             initiator=request.user)
            return redirect('cyberdetectiveview')
    else:
        form = EmployeeUpdateForm(instance=employee)
    context = {'form': form,
               'request': request.user}
    return render(request, 'adminview/employee_update.html', context)


def login_service(request):
    '''
    Login Service. 
    This will enable admins and staff to login from one entry point
    And then be redirected to the relavant view based on their permissions.
    '''
    # Check if user is already logged in and redirect them to the correct view
    if request.user.is_authenticated:
        user_id = request.user.id
        if request.user.is_staff:
            return redirect('adminview')
        else:
            return redirect('employeeview', user_id)

    if request.method == 'POST':
        req_user = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=req_user, password=password)
        # This will first check if the account exists before it tries to authenticate
        if user is not None:
            # Moved login here to fix Anonymous user error
            login(request, user)
            user_id = request.user.id
            if user.is_authenticated:
                if User.objects.get(username=user).is_staff:
                    systemEvent.info(f"Admin logged in: {user}",
                                     initiator=request.user)
                    # Redirect to the admin view
                    return redirect('adminview')
                else:
                    systemEvent.info(f"Employee logged in: {user}",
                                     initiator=request.user)
                    # Redirect to the employee view
                    return redirect('employeeview', user_id)
        else:
            systemEvent.warning(f"User with IP: {get_client_ip(request)} failed to login",
                                initiator=get_client_ip(request))
            messages.error(request, 'Invalid username or password.')
    return render(request, 'homeview/login.html')
