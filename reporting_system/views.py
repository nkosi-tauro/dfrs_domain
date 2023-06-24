from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.templatetags.static import static
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



import json





# Create your views here.
def homeview(request):
    return render(request,'homeview/home.html')

def adminview(request):
    cyberdetectives = User.objects.all()
    context = {'cyberdetectives': cyberdetectives}
    return render(request,'adminview/admin.html', context)

@login_required
def employeeview(request):
    print("employee!")
    employee = User.objects.all()
    #u = request.user()
    context = {'employee': employee}
    return render(request,'employeeview/employee.html', context)


def loginPopup(request):

    if request.method == 'POST':
        user = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(username=user, password=password)

        if user.is_authenticated:
            login(request, user)
            if User.objects.get(username=user).is_staff:
                return adminview(request)
            else:
                return employeeview(request)
        else:
            print("Not yet implemented")
    else:
        print("TODO")
           
              

    #   User = get_user_model()
    #   users = User.objects.all()
    #   userList =User.objects.values()
    #   print(users)
    #   print(userList)
    
    #   

    #   

    #   print("!test")
    #   print(user_a)
    #   
    #   #login(request, user)
    #   return render(request, '')
    #    if users == "test":
    #        print("aaaa")
    #        login(request, user)
#
    #        #return HttpResponse("<script>console.log(\"Welcome!\");</script>")
    #        return render(request, 'employeeview/employee.html')
