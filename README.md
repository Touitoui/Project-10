# Project-10  SoftDesk API

## Installation and Setup
Install Pipenv if you don't have it:
`pip install --user pipenv`


Create a virtual environment and install dependencies using Pipenv:

`pipenv sync`


Set the database:
```
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
``` 


Create a superuser:

`pipenv run python manage.py createsuperuser`


Run the server:

`pipenv run python manage.py runserver`

## Usage

Register a user by sending a POST request to `/api/register/` with the following JSON body:
```
    "username": "your_username", (Alphanumeric only, Required)
    "email": "your@email.com, (Required)
    "password": "your_password", (Required)
    "date_of_birth": "YYYY-MM-DD", (Required)
    "can_be_contacted": true", (Default: false)
    "can_data_be_shared": true" (Default: false)
```

Get a token by sending a POST request to `/api/token/` with the following JSON body:
```
    "username": "your_username",
    "password": "your_password"
```

Refresh the token by sending a POST request to `/api/token/refresh/` with the following JSON body:
```
    "refresh": "your_refresh_token"
```

Use the access token in the Authorization header for subsequent requests:
```
Authorization: Bearer your_access_token
```

See Postman file for subsequent requests: `Project 10.postman_collection.json`