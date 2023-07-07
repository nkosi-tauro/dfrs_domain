from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BaseViewsTest(TestCase):
    """
    Base class for all view tests.
    """

    def setUp(self):
        # Create a test employee and admin user
        self.employee = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.employee.save()
        self.admin = User.objects.create_user(
            "john", "lennon@thebeatles.com", "johnpassword"
        )
        self.admin.is_superuser = True
        self.admin.save()

        return super().setUp()


class CanViewSitePages(TestCase):
    """
    Tests that the site pages can be viewed.
    """

    def test_can_view_homeview(self):
        url = reverse("homeview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homeview/home.html")

    def test_can_view_adminview(self):
        # Log in with admin user
        self.client.login(username="john", password="johnpassword")
        url = reverse("adminview")
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "adminview/admin.html")

    def test_can_view_employeeview(self):
        # Log in with employee user
        self.client.login(username="testuser", password="testpassword")
        url = reverse("employeeview", args=[self.client.request.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "employeeview/employee.html")

    def test_can_view_publicview(self):
        url = reverse("publicview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "publicview/public.html")

    def test_can_view_gdprview(self):
        url = reverse("gdprview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "publicview/gdprview.html")
