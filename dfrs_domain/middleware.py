from django.shortcuts import redirect
from django.urls import reverse

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('adminview')) and request.user.is_authenticated:
            # Check if the user has the necessary role or permissions to access the admin
            if not request.user.is_superuser:
                return redirect('employee-login')  # Redirect to the desired URL if the user doesn't have access

        response = self.get_response(request)
        return response
