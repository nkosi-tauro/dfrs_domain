from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from .settings import SESSION_IDLE_TIMEOUT
import datetime


class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path.startswith(reverse("adminview"))
            and request.user.is_authenticated
        ):
            # Check if the user has the necessary role or permissions to access the admin
            if not request.user.is_superuser:
                return redirect(
                    "employee-logout"
                )  # Redirect to the desired URL if the user doesn't have access

        response = self.get_response(request)
        return response


class SessionIdleTimeout(object):
    """Middle ware to ensure user gets logged out after defined period if inactvity."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_datetime = datetime.datetime.now()
            if "last_active_time" in request.session:
                idle_period = (
                    current_datetime - request.session["last_active_time"]
                ).seconds
                if idle_period > SESSION_IDLE_TIMEOUT:
                    logout(request, "homeview/login.html") # type: ignore
            request.session["last_active_time"] = current_datetime

        response = self.get_response(request)
        return response
