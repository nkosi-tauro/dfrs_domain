'''
User Service views
'''
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register_employee(request):
    '''
    So this will allow an admin to register an employee(new user)
    Without having to use the django admin dashboard
    '''
    if request.method == 'POST':
        # This will take the form inputs (username, password)
        form = UserCreationForm(request.POST)
        # This will check if the inputs are valid based on the contraints
        if form.is_valid():
            form.save()
            # This will redirect back to the admin view
            return redirect('adminview')
    else:
        form = UserCreationForm()
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'adminview/register_employee.html', context)
