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
```bash
$ cd backend
$ docker-compose up --build -d
$ docker-compose exec api python manage.py migrate
$ docker-compose exec api python manage.py createsuperuser
```

### Sample and testing API endpoints

- <http://localhost:8000/admin/>
- <http://localhost:8000/api/v0/samples/>
- <http://localhost:8000/api/v0/somedata/>
- <http://localhost:8000/api/v0/candidates/>

## Deployment
## Maintainers
| Name | Role | Contact |
| ---  | --- | --- |
| Brian Hedden  |   |   |
| Carlos Perez  | Backend Engineer | perez@doorstep.com |
| Henry Lai | | |
| Wes Galbraith | Backend Engineer | galbwe92@gmail.com |
| Zachary Rose  |   |   |
