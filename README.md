# Django Heroku Docker

This is the ultimate full stack project using Heroku container build manifest to deploy. This is a generate template with Postgres, Celery, Redis, JWT.

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
```

## TIPS

- remember to check `ALLOWED_HOSTS` in settings to white list the correct domain
- killing a port: `kill -9 $(lsof -t -i tcp:8000)`
