"""
Test cases related to the "cyberdetective" functionality
Actions that can be performed by an Admin user
"""
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse


class BaseTest(TestCase):
    """
    Base test class for all tests
    """

    def setUp(self):
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


class RegisterEmployeeTest(BaseTest):
    """
    Test class for register employee
    """

    def test_can_view_register_employee_page(self):
        """
        This checks if the register employee page can be viewed.
        And also if the right template has been used.
        """
        response = self.client.get(self.register_employee_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adminview/register_employee.html")

    def test_register_employee_form_valid_data(self):
        """
        Tests if the Employee can be registered with valid data.
        """
        response = self.client.post(
            self.register_employee_url, self.register_employee, format="text/html"
        )
        self.assertEqual(response.status_code, 302)


class EmployeeDetailTest(BaseTest):
    """
    Tests employee detail view.
    """

    def test_employee_detail_view(self):
        """
        Tests if the view template has been successfully rendered.
        """
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adminview/employee_detail.html")


class EmployeeDeleteTest(BaseTest):
    """
    Class used to test delete operation
    """

    def test_employee_delete_view(self):
        """
        Checks is the user has been redirected to appropriate page.
        """
        response = self.client.get(self.employee_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adminview/employee_delete.html")

    def test_employee_delete(self):
        """
        Checks if the user has been successfully deleted
        """
        response = self.client.post(self.employee_delete_url, format="text/html")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cyberdetectiveview"))


class EmployeeUpdateTest(BaseTest):
    """
    Class to test update operation over the employee
    """

    def test_employee_update_view(self):
        """
        Check if the appropriate page was rendered after update
        """
        response = self.client.get(self.employee_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adminview/employee_update.html")

    def test_employee_update(self):
        """
        Checks if the update was successfull.
        """
        response = self.client.post(
            self.employee_update_url, self.update_employee, format="text/html"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("cyberdetectiveview"))
