
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