"""
Test cases for user_service
"""
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse


class BaseTest(TestCase):
    """
    Base test class for all tests
    """

    def setUp(self):
        # Test Admin user
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username="john", password="johnpassword")
        self.login_url = reverse("homeview")
        self.admin_url = reverse("adminview")
        self.employee_url = reverse("employeeview", args=[self.user.pk])
        self.register_employee_url = reverse("register-employee")
        self.employee_detail_url = reverse("employee-detail", args=[self.user.pk])
        self.employee_delete_url = reverse("employee-delete", args=[self.user.pk])
        self.employee_update_url = reverse("employee-update", args=[self.user.pk])
        self.register_employee = {
            "username": "testEmployee",
            "email": "test@employee.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.update_employee = {
            "username": "testEmployee",
            "email": "test@employee.com",
        }

        return super().setUp()


class LoginServiceGetTest(BaseTest):
    """
    Class that tests get requests of a login service
    """

    def test_login_employee_view(self):
        """
        Checks if the employee gets redirected to his view.
        """
        response = self.client.get(self.employee_url)
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertTemplateUsed(response, "employeeview/employee.html")

    def test_login_admin_view(self):
        """
        Checks if the admin gets redirected to his view.
        """
        self.user.is_staff = True
        response = self.client.get(self.admin_url)
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(self.user.is_staff, True)
        self.assertTemplateUsed(response, "adminview/admin.html")

    def test_home_view(self):
        """
        Checks if the user gets redirected to home after unsuccessfull login.
        """
        self.client.is_authenticated = False # type: ignore
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, "homeview/home.html")


class LoginServicePostTest(BaseTest):
    """
    Class that handles post requests tests of a login service.
    """

    def test_login_employee_view(self):
        """
        Checks if the user is authenticated, and consequently gets redirected to corresponding page.
        """
        response = self.client.post(self.employee_url, format="text/html", follow=True)
        self.client.is_authenticated = True # type: ignore
        self.user.is_staff = False
        redirect_url = response.request["PATH_INFO"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(redirect_url, reverse("employeeview", args=[self.user.pk]))

    def test_login_admin_view(self):
        """
        Checks if the admin is authenticated, and consequently gets redirected to the corresponding page.
        """
        response = self.client.post(self.admin_url, format="text/html", follow=True)
        self.client.is_authenticated = True # type: ignore
        self.user.is_staff = True
        redirect_url = response.request["PATH_INFO"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(redirect_url, reverse("adminview"))

