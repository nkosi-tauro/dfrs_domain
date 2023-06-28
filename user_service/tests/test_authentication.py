'''
Test cases for user_service
'''
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class BaseTest(TestCase):
    '''
    Base test class for all tests
    '''
    def setUp(self):
        self.register_employee_url = reverse('register-employee')
        # Test Admin user
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='john', password='johnpassword')
        self.test_employee = {
            'username': 'testEmployee',
            'email' : 'test@employee.com',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        return super().setUp()


class RegisterEmployeeTest(BaseTest):
    '''
    Test class for register employee
    '''
    def test_can_view_register_employee_page(self):
        '''
        This checks if the register employee page can be viewed.
        And also if the right template has been used.
        '''
        response = self.client.get(self.register_employee_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/register_employee.html')

    def test_register_employee_form_valid_data(self):
        '''
        Tests if the Employee can be registered with valid data.
        '''
        response = self.client.post(self.register_employee_url, self.test_employee,
                                    format='text/html')
        self.assertEqual(response.status_code, 302)
