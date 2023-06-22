'''
User Service views
'''
from django.shortcuts import render, redirect
from .forms import EmployeeRegisterForm
from django.contrib.auth.models import User

# Create your views here.
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


def employee_detail(request, primary_key):
    '''
    This will allow an admin to view a specific employee and edit or delete it
    '''
    employee = User.objects.get(id=primary_key)
    context = {'employee': employee}
    return render(request, 'adminview/employee_detail.html', context)

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
