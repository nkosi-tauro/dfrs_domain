from django.shortcuts import render

# Create your views here.
def homeview(request):
    return render(request,'homeview/home.html')

def adminview(request):
    return render(request,'adminview/admin.html')