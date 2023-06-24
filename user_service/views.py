'''
User Service views
'''
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EmployeeRegisterForm, EmployeeUpdateForm

# Create your views here.
@login_required(login_url='employee-login')
def register_employee(request):
    '''
    So this will allow an admin to register an employee(new user)
    Without having to use the django admin dashboard
    '''
    if request.method == 'POST':
        # This will take the form inputs (username, password)
        form = EmployeeRegisterForm(request.POST)
        # This will check if the inputs are valid based on the contraints
        if form.is_valid():
            form.save()
            # This will redirect back to the admin view
            return redirect('adminview')
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
        return redirect('adminview')
    context = {'employee': employee}
    return render(request, 'adminview/employee_delete.html', context)

@login_required(login_url='employee-login')
def employee_update(request):
    '''
    This will allow an admin to update an employee
    '''
    if request.method == 'POST':
        # instance=request.user will pass through the user data into the input fields
        form = EmployeeUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('adminview')
    else:
        form = EmployeeUpdateForm(instance=request.user)
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
        if request.user.is_staff:
            return redirect('adminview')
        else:
            return redirect('employeeview', user_id)

    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user, password=password)

        # This will first check if the account exists before it tries to authenticate
        if user is not None:
            if user.is_authenticated:
                login(request, user)
                user_id = request.user.id
                if User.objects.get(username=user).is_staff:
                    return redirect('adminview')
                else:
                    return redirect('employeeview', user_id)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'homeview/login.html')
           