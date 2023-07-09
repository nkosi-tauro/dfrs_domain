'''
Test cases for user_service
'''
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase, RequestFactory
from user_service.views import get_client_ip
from user_service.ratelimit import RateLimitExceeded, RateLimit
from django.core.exceptions import PermissionDenied
from django.core.cache import caches
from datetime import timedelta


class BaseTest(TestCase):
    '''
    Base test class for all tests
    '''
    def setUp(self):
        # Test Admin user
        self.factory = RequestFactory()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username='john', password='johnpassword')
        self.login_url = reverse('homeview')
        self.admin_url = reverse('adminview')
        self.employee_url = reverse('employeeview', args=[self.user.pk])
        self.register_employee_url = reverse('register-employee')
        self.employee_detail_url = reverse('employee-detail', args=[self.user.pk])
        self.employee_delete_url = reverse('employee-delete', args=[self.user.pk])
        self.employee_update_url = reverse('employee-update', args=[self.user.pk])
        self.register_employee = {
            'username': 'testEmployee',
            'email' : 'test@employee.com',
            'password1' : 'testpassword',
            'password2' : 'testpassword',
        }
        self.update_employee = {
            'username': 'testEmployee',
            'email': 'test@employee.com'}

        request = self.factory.get('/')
        ip_address = get_client_ip(request)
        self.cache = caches["default"]
        
        self.rate_limit = RateLimit(
            key=ip_address,
            limit=5,
            period=10,
            cache=self.cache,
            key_prefix="rl:",
        )

        return super().setUp()
    

class GetClientIpTest(BaseTest):
    '''
    Class to test obtaining an IP Address of a user.
    '''
    def test_ip(self):
        '''
        Tests if IP can be obtained during the requests.
        '''
        request = self.factory.get('/')
        request.META = {
            'HTTP_X_FORWARDED_FOR': '192.168.1.1, 10.0.0.1',
            'REMOTE_ADDR': '127.0.0.1',
        }
        client_ip = get_client_ip(request)
        self.assertEqual(client_ip, "192.168.1.1")
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
        response = self.client.post(self.register_employee_url, self.register_employee,
                                    format='text/html')
        self.assertEqual(response.status_code, 302)


class EmployeeDetailTest(BaseTest):
    '''
    Tests employee detail view.
    '''
    def test_employee_detail_view(self):
        '''
        Tests if the view template has been successfully rendered.
        '''
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/employee_detail.html')


class EmployeeDeleteTest(BaseTest):
    '''
    Class used to test delete operation
    '''
    def test_employee_delete_view(self):
        '''
        Checks is the user has been redirected to appropriate page.
        '''
        response = self.client.get(self.employee_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/employee_delete.html')
        
    def test_employee_delete(self):
        '''
        Checks if the user has been successfully deleted
        '''
        response = self.client.post(self.employee_delete_url,format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cyberdetectiveview'))

class EmployeeUpdateTest(BaseTest):
    '''
    Class to test update operation over the employee
    '''
    def test_employee_update_view(self):
        '''
        Check if the appropriate page was rendered after update
        '''
        response = self.client.get(self.employee_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminview/employee_update.html')

    def test_employee_update(self):
        '''
        Checks if the update was successfull.
        '''
        response = self.client.post(self.employee_update_url,self.update_employee
                ,format='text/html')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('cyberdetectiveview'))


class LoginServiceGetTest(BaseTest):
    '''
    Class that tests get requests of a login service
    '''
    def test_login_employee_view(self):
        '''
        Checks if the employee gets redirected to his view.
        '''
        response = self.client.get(self.employee_url)
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertTemplateUsed(response, 'employeeview/employee.html')
    
    
    def test_login_admin_view(self):
        '''
        Checks if the admin gets redirected to his view.
        '''
        self.user.is_staff=True
        response = self.client.get(self.admin_url)
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(self.user.is_staff, True)
        self.assertTemplateUsed(response, 'adminview/admin.html')
    
    def test_home_view(self):
        '''
        Checks if the user gets redirected to home after unsuccessfull login.
        '''   
        self.client.is_authenticated=False
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'homeview/home.html')

class LoginServicePostTest(BaseTest):
    '''
    Class that handles post requests tests of a login service.
    '''
    def test_login_employee_view(self):
        '''
        Checks if the user is authenticated, and consequently gets redirected to corresponding page.
        '''
        response = self.client.post(self.employee_url, format='text/html', follow=True)
        self.client.is_authenticated=True
        self.user.is_staff=False
        redirect_url = response.request["PATH_INFO"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(redirect_url, reverse('employeeview', args=[self.user.pk]))

    def test_login_admin_view(self):
        '''
        Checks if the admin is authenticated, and consequently gets redirected to the corresponding page.
        '''
        response = self.client.post(self.admin_url, format='text/html', follow=True)
        self.client.is_authenticated=True
        self.user.is_staff=True
        redirect_url = response.request["PATH_INFO"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(redirect_url, reverse('adminview'))


class RateLimitTest(BaseTest):
    '''
    Class to test rate limits of the logins.
    '''
    def test_rate_limit_above_limit(self):
        '''
        Method to test if the Exception has been successfully raised after too many login attempts.
        '''
        with self.assertRaises(RateLimitExceeded) as cm:
            self.rate_limit.check(6)
        self.assertEqual(cm.exception.limit, self.rate_limit.limit)

    def test_custom_period_as_timedelta(self):
        '''
        Checks timedelta period option
        '''
        custom_rate_limit = RateLimit(
            key="",
            limit=10,
            period=timedelta(minutes=30),
            cache=self.cache,
            key_prefix="rl:",
        )
        self.assertEqual(custom_rate_limit.seconds, 1800)

    def test_custom_period_as_seconds(self):
        '''
        Checks seconds period option
        '''
        custom_rate_limit = RateLimit(
            key="",
            limit=10,
            period=3600,
            cache=self.cache,
            key_prefix="rl:",
        )
        self.assertEqual(custom_rate_limit.seconds, 3600)
