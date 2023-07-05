<h1 align="center">The Dutch Forensics Reporting System</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/nkosi-tauro/dfrs_domain?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/nkosi-tauro/dfrs_domain?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/nkosi-tauro/dfrs_domain?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/nkosi-tauro/dfrs_domain?color=56BEB8">

  [![Django CI](https://github.com/nkosi-tauro/dfrs_domain/actions/workflows/django.yml/badge.svg)](https://github.com/nkosi-tauro/dfrs_domain/actions/workflows/django.yml)

</p>

## :dart: About ##

The Dutch Forensic Reporting System aims to provide a comprehensive reporting service for identifying flaws in ICT systems across various organisations.

## 💻View Deployed Project
- [Production](https://dfrsdomain-production.up.railway.app/)  
- [Development](https://dfrsdomain-dev.up.railway.app/)

## :checkered_flag: Starting ##
There are 2 ways of getting this project up and running but before getting started, please make sure you have [docker](https://www.docker.com/) installed if you are using method 2.   
For Method 1, make sure you have [python](https://www.python.org/) 3.10.x and above installed.  

1. Python
2. Docker

_Important:_  
When Running locally please make sure that `DEBUG` and `SECURE_SSL_REDIRECT` are set to  `DEBUG=True` and `SECURE_SSL_REDIRECT=False` inside the `settings.py` file


### 1. Python

```bash
# Clone this project
$ git clone https://github.com/nkosi-tauro/dfrs_domain

# Access directory
$ cd dfrs_domain

# install pip packages
$ pip install -r requirements.txt

# Run the project
$ python manage.py runserver

#For Linux/Mac use:
$ python3 manage.py runserver

# The server will initialize on <http://127.0.0.1:8000>
```

### 2. Docker 

```bash
# Clone this project
$ git clone https://github.com/nkosi-tauro/dfrs_domain

# Access directory
$ cd dfrs_domain

# build docker container
$ docker build --tag dfrs_domain .

# Run the project
$ docker run --env-file=.env --publish 8000:8000 dfrs_domain

# The server will initialize on <http://127.0.0.1:8000>
```

## 🗃️ Adding Packages

```bash
#After installing new packages or tools via pip, run:
$ pip freeze > requirements.txt
#To add the packages to the requirements.txt file.
```


## 🔐 Security Risks and Mitigations.

### 1. Risk: Injection
*Mitigation:*  
In our application, we have implemented Django's querysets which implement query parameterisation to protect against SQL injection attacks (Django, N.D). Additionally, we utilise the built-in validators to validate and sanitize user input, ensuring adherence to specific regex patterns which are utilised under the hood. These measures collectively enhance the security of our application by safeguarding against malicious SQL injections and promoting secure user input handling.


### 2. Risk(s):  Insecure design + 3. Vulnerable and Outdated components
*Mitigation(s):*  
We added a [Django Dependency and Security checker](https://github.com/marketplace/actions/django-security-check). It scans the repo and helps to continuously monitor and fix common security vulnerabilities in the Django application. With this tool we can keep up to date with any changes to the tools we utilise in the project and update and or fix them if any issues arise.  

These where some of the security issues identified in our Project:   

![Alt text](security_images/securityBefore.png)


After fixing the issues:  

![Alt text](security_images/securityAfter.png)


### 4. Risk: Broken Access Control
*Mitigation:*   
Using The Django authentication provider allowed us to implement role based access to the application. Using the `@login_required(login_url='employee-login')` decorators, we can __secure__ routes behind the authentication system and any unauthenticated users will not be able to visit them. Furthermore we added a redirect system for Authenticated users roles, `admin` or `employee`. Based on their role the authenticated user will be redirected to the relevant view where they have permissions.  

Code Snippets:  
```py
#login decorator on route
@login_required(login_url='employee-login')
def someview(request):
    return render(request, 'this/this.html')
```

```py
# Role based authentication
user = authenticate(username=req_user, password=password)
# This will first check if the account exists before it tries to authenticate
if user is not None:
  login(request, user)
  if user.is_authenticated:
    if User.objects.get(username=user).is_staff:         
      # Redirect to the admin view
      return redirect('adminview')
    else:
      # Redirect to the employee view
      return redirect('employeeview', user_id)
```

### 5. Risk: Security Logging and Monitoring Failures:
*Mitigation:*  
We Implemented a logging feature that logs/Tracks the following:

- When a user of the General Public submits a vulnerability report
- When a user attempts and fails to login, it captures their IP - the plan would be then to rate limit the IP if we notice malicious activity (e.g repeat incorrect login attempts)
- When Employees login
- When Employees submit a vulnerability report  

The logs are only viewable by an admin user.  
![Alt text](security_images/logs.png)

### 6. Risk: Cryptographic Failures:
*Mitigation:*  
We used The Django authentication provider which is a trusted authentication library (Django, N.D). This ensures the secure handling of sensitive data. SSL/TLS are enforced on the Server which encrypts any data moving between the application and database. 

Server deployed on HTTPS Protocol:  
![Alt text](security_images/https.png)

Let's Encrypt Certificate:  
![Alt text](security_images/cert.png)


## 🕵️ GDPR Compliance.
As part of out application complying with GDPR, users can request that their data be deleted from the Dutch Forensics Reporting System.


## :test_tube: Testing

We are using The Default testing module in Django `TestCase` to create our tests.
The `coverage` module is required if you want to run the `coverage commands`.
```bash
# Install coverage:
$ python3 -m pip install coverage

#For Linux/Mac use:
$ python3 -m pip install coverage

```

*Note: The tests take a while (few seconds) as a test database needs to be created.*  
*Replace the variable `django_app_name` with either*:
- `user_service`
- `reporting_system`

```bash
#To run all the tests run:
$ python manage.py test

#For Linux/Mac use:
$ python3 manage.py test

#To view Test Coverage in terminal:
$ coverage run --source='django_app_name' manage.py test && coverage report

#To view Test Coverage via HTML:
$ coverage run --source='django_app_name' manage.py test && coverage report && coverage html

```
## 🔍 References

Django, (N.D). Security In Django. _SQL Injection Protection_ Available from:
https://docs.djangoproject.com/en/4.2/topics/security/ [Accessed 03 July 2023]

Django, (N.D). Security In Django. Available from:
https://docs.djangoproject.com/en/4.2/topics/security/ [Accessed 03 July 2023]


## ✍️ Authors
Made with :heart: by 

- <a href="https://github.com/alesteka" target="_blank">Ales Tekavcic</a>
- <a href="https://github.com/muwalofra" target="_blank">Francis Muwalo</a>
- <a href="https://github.com/nkosi-tauro" target="_blank">Nkosilathi Tauro</a>
- <a href="https://github.com/alihu12345" target="_blank">Abdulahi Alihu Ngamjeh</a>
