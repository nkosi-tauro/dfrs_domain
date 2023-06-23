from django.shortcuts import render

#new Imports
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.
def homeview(request):
    return render(request,'home.html')
    

def print_u(request):
    if request.method == 'POST':
        user = request.POST['Username']
        print("dasdasdas")
        return render(request, 'print_u.html')

