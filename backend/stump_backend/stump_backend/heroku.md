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

First, create a Django secret key:
```
$ python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

Run these commands in the root git directory.


```
$ heroku create stump-vote  (note: do this in the root git directory)
$ heroku config:set SECRET_KEY=<secret>
$ heroku config:set DJANGO_ALLOWED_HOSTS=stump-vote.herokuapp.com
$ git remote -v
$ git subtree push --prefix backend/stump_backend heroku master
$ heroku run python stump_backend/manage.py migrate
$ heroku run python stump_backend/manage.py createsuperuser
$ heroku ps:scale web=1
```

Deploys to: https://stump-vote.herokuapp.com/

Note: will need to set, which are found in the Heroku Datastores:
- DATABASE_URL
- DB_HOST
- DB_NAME
- DB_PASSWORD
- DB_PORT
- DB_USER

## Use existing Heroku app already deployed

```
$ git remote add heroku https://git.heroku.com/stump-vote.git
```

Run gunicorn via Profile locally on port 5000:

```
$ heroku local
```

## Using the frontend demo side-loader

Prior to the monorepo, whereby both the frontend and backend are in an integrated repo, the frontend React app
is built separately from the Heroku deployment. The process of deploying the frontend uses a *side-loader*
that copies the React static build from Amazon S3 to the Heroku dyno.

The deployment is therefore a two step process:
1) Build the React app and copy the files to S3
2) Deploy the backend app which kicks off a gulp task to fetch the app and copy it to a Django-accessible static directory.

### Prerequisites

Using your Amazon S3 credentials, logon to the AWS console and create an S3 bucket called `stump-vote-frontend-demo`.
Note that this bucket does not need any public access permissions; the default locked down permissions are fine.

Also create an IAM user with credentials with read access to the bucket.

### Build React app

You will need the aws-cli tools installed to run `aws` from the command line.

Build and upload the build statics to S3:

```
$ cd frontend-demo
$ npm run build
$ cd build
$ aws s3 sync . s3://stump-vote-frontend-demo/ --delete
```

### Deploy the React and Django app to Heroku

#### Heroku setup

Heroko needs the nodejs Heroku build pack.

```
$ heroku buildpacks
=== stump-vote Buildpack URLs
1. heroku/nodejs
2. heroku/python
```

And the S3 keys from the AWS IAM console:
```
$ heroku config:set AWS_ACCESS_KEY_ID=<access key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<secret key>
```

Review `gulpfile.js` and `package.json` and the step "heroku-postbuild".

### Deployment

After copying up the React app to S3, deploy the backend to Heroku. To deploy a branch other than master, starting
from the root of the project.

```
$ cd stump_vote
$ git push heroku `git subtree split --prefix backend/stump_backend react_proto1`:master
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
