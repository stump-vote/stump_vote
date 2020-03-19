# Stump
Stump is a non-partisan, crowd-sourced,
voter-empowerment platform. [Sign up](https://stump.vote/) to try the prototype.
## Frontend Development
## Backend Development

## Django development notes

### Dependencies

- Python 3.6 or higher
- pipenv
- PostgreSQL 10 and SQLite3
OR
- Docker

### Quickstart

On localhost:

```bash
$ cd backend/api
$ pipenv sync --dev
$ pipenv shell
$ cd stump_backend
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

With docker-compose:
1. Copy and paste the following environment variables into ```backend/api/.env.dev```:
```bash
DEBUG=1
SECRET_KEY=stump_dev
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
DB_USER=stump_dev
DB_PASSWORD=stump_dev
DB_NAME=stump_dev
DB_HOST=postgres
DB_PORT=5432
DATABASE=postgres
```
2. In terminal, navigate to project root, then do
```bash
$ cd backend
$ docker-compose -f docker-compose.local.yml up --build -d
$ docker-compose -f docker-compose.local.yml exec api python manage.py migrate
$ docker-compose -f docker-compose.local.yml exec api python manage.py createsuperuser
```

### Sample and testing API endpoints

- <http://localhost:8000/admin/>
- <http://localhost:8000/api/v0/samples/>
- <http://localhost:8000/api/v0/somedata/>
- <http://localhost:8000/api/v0/candidates/>

## Deployment
### Environment Variables
The following environment variables should be set using the command line or using .env files:
  - Django app (```backend/api/.env.prod```):
    - DEBUG : set to 1 to run django server in debug mode and 0 otherwise (see Django docs for [DEBUG](https://docs.djangoproject.com/en/3.0/ref/settings/#debug))
    - SECRET_KEY : secret key for Django app (see [SECRET_KEY](https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key))
    - DJANGO_ALLOWED_HOSTS : hosts that Django is allowed to serve (see [ALLOWED_HOSTS](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts))
    - DB_USER (see Django docs for [DATABASES](https://docs.djangoproject.com/en/3.0/ref/settings/#databases))
    - DB_PASSWORD (see Django docs for [DATABASES](https://docs.djangoproject.com/en/3.0/ref/settings/#databases))
    - DB_NAME (see Django docs for [DATABASES](https://docs.djangoproject.com/en/3.0/ref/settings/#databases))
    - DB_HOST (see Django docs for [DATABASES](https://docs.djangoproject.com/en/3.0/ref/settings/#databases))
    - DB_PORT (see Django docs for [DATABASES](https://docs.djangoproject.com/en/3.0/ref/settings/#databases))
  - Postgres (```backend/api/.env.prod.db```):
    - POSTGRES_USER : name of database user
    - POSTGRES_PASSWORD : user's password
    - POSTGRES_DB : name of the application database

### Running in production mode

```bash
$ cd backend
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec api python manage.py migrate --noinput
$ docker-compose -f docker-compose.prod.yml exec api python manage.py collectstatic --no-input --clear
```

## Maintainers
| Name | Role | Contact |
| ---  | --- | --- |
| Brian Hedden  |   |   |
| Carlos Perez  | Backend Engineer | perez@doorstep.com |
| Henry Lai | | |
| Wes Galbraith | Backend Engineer | galbwe92@gmail.com |
| Zachary Rose  |   |   |
