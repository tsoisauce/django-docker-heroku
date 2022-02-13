# Django Heroku Docker

This is the ultimate full stack project using Heroku container build manifest to deploy. This is a generate template with Postgres, Celery, Redis.

## Workflow

- either use docker or virtual environment of your choice with Python 3.10.2
- update/install dependencies `pip install -r requirements.txt`
- start Django web server: `python manage.py runserver_plus`
- start Celery workers: `celery -A app worker -l INFO`
- to access shell: `python manage.py shell_plus`

## Deploy on Heroku

This template has a Dockerfile that is Django deployment ready using Heroku's container build manifest process. Each process in the Dockerfile is annotated to eplain each process. Migrations will be runned manually via Heroku docker container command line.

## Docker

remove existing images

```bash
docker stop django-heroku
docker rm django-heroku
```

build locally:

```bash
docker build -t web:latest .
docker run -d --name django-heroku -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

view static files:

```bash
docker exec django-heroku ls /app/staticfiles
docker exec django-heroku ls /app/staticfiles/admin
```

to run commands within deployed heroku container:

```bash
heroku run python manage.py makemigrations -a {{HEROKU_APP_NAME}}
heroku run python manage.py migrate -a {{HEROKU_APP_NAME}}
```

## Deploying on Heroku

### Deploy via container manifest

Sign up for a Heroku acount and download their [CLI](https://devcenter.heroku.com/articles/heroku-cli)

create a new Heroku app. This will generate a new app and corresponding remotes. You will then push to this remote to deploy on Heroku master. In this example, the name of our application is:  `morning-sierra-00895`

Note: be sure to update this in your allowed host.  Replace anywhere that has, `morning-sierra-00895`

```bash
heroku create
Creating app... done, ⬢ morning-sierra-00895
https://morning-sierra-00895.herokuapp.com/ | https://git.heroku.com/morning-sierra-00895.git
```

add `SECRET_KEY` environment varaible to Heroku. This is a 50 character maximum string that is randomly generated and use to validate your application.

Note: remember to replace `YOUR_SECRET_KEY` with your key and rplace `morning-sierra-00895` with your app's name

```bash
heroku config:set SECRET_KEY={{YOU_SECRET_KEY}} -a morning-sierra-00895
Setting SECRET_KEY and restarting ⬢ morning-sierra-00895... done, v3
SECRET_KEY: {{YOU_SECRET_KEY}}
```

We will be using [Heroku container build manifest](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) to deploy our Docker images.

Setup your Heroku container stack

```bash
heroku stack:set container -a morning-sierra-00895 
Setting stack to container... done
```

Create an `heroku.yml` file this will inform heroku on the Dockerfile to build from and any commands to run.

There are three types of stages:

- `setup` is used to define Heroku addons and configuration variables to create during app provisioning.
- `release` is used to define tasks that you'd like to execute during a release.
- `run` is used to define which commands to run for the web and worker processes.

Next, install the `heroku-manifest` plugin from the beta CLI channel:

```bash
heroku plugins:install @heroku-cli/plugin-manifest
Installing plugin manifest... installed v0.0.5
```

With that, initialize a Git repo and create a commit.

Then, add the Heroku remote:

```bash
heroku git:remote -a morning-sierra-00895
set git remote heroku to https://git.heroku.com/morning-sierra-00895.git
```

Deploy to Heroku master to build your image and deploy your container:

```bash
git push heroku master
```

### Add Postgres DB and Redis

#### Create the Postgres database

```bash
heroku addons:create heroku-postgresql:hobby-dev -a morning-sierra-00895
Creating heroku-postgresql:hobby-dev on ⬢ morning-sierra-00895... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-solid-97726 as DATABASE_URL
Use heroku addons:docs heroku-postgresql to view documentation
```

Once the database is up, run the migrations:

```bash
heroku run python manage.py makemigrations -a morning-sierra-00895
heroku run python manage.py migrate -a morning-sierra-00895
```

#### Create Redis:

```bash
heroku addons:create heroku-redis:hobby-dev -a morning-sierra-00895
Creating heroku-redis:hobby-dev on ⬢ morning-sierra-00895... free
Your add-on should be available in a few minutes.
! WARNING: Data stored in hobby plans on Heroku Redis are not persisted.
redis-crystalline-94825 is being created in the background. The app will restart when complete...
Use heroku addons:info redis-crystalline-94825 to check creation progress
Use heroku addons:docs heroku-redis to view documentation
```

## Celery

This project also inludes Celery to manage cron jobs and background workers. It is configured to use Redis as a boker.

Install redis and to start workers:

```bash
celery -A app worker -l INFO
```

### sample Celery task

Thir project has a sample test task that sleeps for 3-seconds. This ban be triggered by the following requests:

create task:

```curl
curl --location --request POST 'localhost:8000/task' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "test"
}'
```

get task status (sample task id 388b2b9e-d2d7-491c-93a5-ecc6034e555e):

```curl
curl --location --request GET 'localhost:8000/task/388b2b9e-d2d7-491c-93a5-ecc6034e555e' \
--header 'Content-Type: application/json' \
--data-raw '{
    "type": "test"
}'
```

## TIPS

- remember to check `ALLOWED_HOSTS` in settings to white list the correct domain
- killing a port: `kill -9 $(lsof -t -i tcp:8000)`

## TODO

- GraphQL
- REST Framework
- JWT
