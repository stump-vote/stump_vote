# Heroku cheat sheet

https://devcenter.heroku.com/articles/getting-started-with-python#introduction

## Install
```
$ sudo add-apt-repository "deb https://cli-assets.heroku.com/branches/stable/apt ./"
$ curl -L https://cli-assets.heroku.com/apt/release.key | sudo apt-key add -
$ sudo apt update
$ sudo apt-get install heroku
$ heroku --version
$ heroku login
```

# Deploying to Heroku

For Heroku to work correctly, these files and changes are needed:

- Procfile
- runtime.txt
- add WhiteNoise to the middleware

## Create new Heroku app

Run these commands in the same directory as the Procfile and runtime.txt.

```
$ heroku create stump-vote
$ git remote -v
$ git push origin master
$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
$ heroku ps:scale web=1
```

Deploys to: https://stump-vote.herokuapp.com/

## Use existing Heroku app already deployed

```
$ git remote add heroku https://git.heroku.com/stump-vote.git
```

Run gunicorn via Profile locally on port 5000:

```
$ heroku local
```

## Status

```
$ heroku status
```

## Create a "getting started" project / release management

```
$ git clone git@github.com:heroku/python-getting-started.git
$ heroku create
$ git push heroku master
$ heroku releases
$ git log --oneline -n 3
# Don't forget first to rollback migrations
$ heroku releases:rollback v9
```

## Start web / scale up or down:

```
$ heroku ps:scale web=1
$ heroku open
$ heroku ps:scale web=0
$ heroku ps:scale web+5
```

## Show logs

```
$ heroku logs --tail
$ heroku logs
$ heroku logs --ps web.1 --tail
```

## Show apps

```
$ heroku apps --all
$ heroku ps
$ heroku ps:type
$ heroku ps web
$ heroku apps:info
$ heroku apps:info still-ravine-45910
```

## Dyno

```
$ heroku dyno:type
```

## Run locally using Procfile

Run this in the same directory as Procfile.

```
$ heroku local
$ heroku local:run python manage.py shell
$ DJANGO_SETTINGS_MODULE=gettingstarted.local_settings ./manage.py runserver
```

## Papertrail

```
$ heroku addons:create papertrail
$ heroku addons:docs papertrail
$ heroku addons:open papertrail
```

## Remote shell

```
$ heroku run python manage.py shell
$ heroku run bash
```

## Environment variables / Config vars

```
$ heroku config
$ heroku config:set TIMES=2
$ heroku addons
```

Heroku addons will show if a PostgreSQL database is provisioned.

## Database (Heroku way)

```
$ heroku pg:info
$ heroku run python manage.py showmigrations
$ heroku run python manage.py migrate
$ heroku pg:psql
$ sudo -u postgres createdb heroku_getting_started
$ heroku local:run python manage.py showmigrations
$ heroku local:run python manage.py migrate
```

## Database (Django way)

```
$ DJANGO_SETTINGS_MODULE=gettingstarted.local_settings ./manage.py dbshell
$ DJANGO_SETTINGS_MODULE=gettingstarted.local_settings ./manage.py migrate
```
