from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def homeview(request):
    return render(request,'homeview/home.html')

def adminview(request):
    cyberdetectives = User.objects.all()
    context = {'cyberdetectives': cyberdetectives}
    return render(request,'adminview/admin.html', context)