# ![Major assignment](hashedin.png)
# Stark Ticket(s) Management System
>  A centralized ticketing system that can be accessed through APIs using Django Framework with Postgres database and delivered as containerized application using docker.

## Requirements  (Prerequisites)
Tools and packages required to successfully install this project.
For example:
* Python 3.x [Install](https://www.python.org/ftp/python/3.9.7/python-3.9.7-macosx10.9.pkg)

## Getting Started

Setup project environment with [virtualenv](https://virtualenv.pypa.io) and [pip](https://pip.pypa.io).

```bash
$ git clone https://github.com/theRuthless/stark_ly3000_web_app.git
$ cd stark_ly3000_web_app
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd backend/
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Features