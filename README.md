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

## Enviroments
- [Production](https://dfrsdomain-production.up.railway.app/)  
- [Development](https://dfrsdomain-dev.up.railway.app/)

## :checkered_flag: Starting ##
There are 2 ways of getting this project up and running but before getting started, please make sure you have [docker](https://www.docker.com/) installed if you are using method 2.   
For Method 1, make sure you have [python](https://www.python.org/) 3.10.x and above installed.  

1. Method 1 (Normal Django Way)
2. Method 2 (Docker)


### Method 1 (Normal Django Way)

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

### Docker 

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


## 🔐 Security risks to look for and implement

### Injection
To prevent injection attacks, I would recommend to validate each user input submited through the form, and ideally we should do the same for the logging, but I would skip this for now, because the main purpose is to demonstrate it on the submitted form.

Validating each user input means enforcing the use of regex at inputs where it makes sense.
sanitizing data - preventing that any input isnt harmfull.
At least these two features should be included (my proposal)

### Insecure design
Regarding this risk, it is not much of a technical aspect, but rather an mental tought about overall design of a system - meaning:
we have provided functionality, which validates employee login. Consequently he can only do what his permissions are allowing him to do
Moreover we can mention/include technologies, which helped us to follow the best practices (using cloud - cloud security features, CI/CD with Github, docker,  Concurrent 'transactions', etc.).

### Vulnarable and Outdated components
Regarding this risk, I would suggest that one of us tries to use dependency-check tool for python. If we manage to use it, then we can say that we have met the standards of Vulnarable and Outdated components. Moreover regarding this risk, we can say (in final report if we will have to submit it) that we have used latest versions of django etc.

### Broken Access Control
To tackle these issues, we have to prevent an employee to access admin's functionalitis vice versa, this has been achieved through the use of session tokens (I think we have already implemented this solution (login (store session), logout (delete session), accessing unauthorized pages)), so ,maybe we can mark this task as successfully met?

some additional features that are worth considering regarding AC (access control):
Client-side - this way Django works, as fas as i know, so it makes sense to have this in mind (Client/server side catching) can also be marked as done
insecure design - Tauro has already provided restrictions regarding appropriate passwords - can be marked as done

### Security Logging and Monitoring Failures:
We have also met this feature, however I am not sure if it would make sense to store these data to postgresql?

### Cryptographic Failures:
We have to encrypt sensitive data before sending it to postgresql, and consequently decrypt it when querying? I assume


## :test_tube: Testing

We are using The Default testing module in Django `TestCase` to create our tests.
The `coverage` module is required to run the `coverage commands`.
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

Made with :heart: by 

- <a href="https://github.com/alesteka" target="_blank">Ales Tekavcic</a>
- <a href="https://github.com/muwalofra" target="_blank">Francis Muwalo</a>
- <a href="https://github.com/nkosi-tauro" target="_blank">Nkosilathi Tauro</a>
- <a href="https://github.com/alihu12345" target="_blank">Abdulahi Alihu Ngamjeh</a>
