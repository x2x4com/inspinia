# flask-template

Template flask application using Flask-Admin, Flask-Security, SQLAlchemy, Sentry, and Celery among other common flask
extensions.

***


### Install

> Due to a strict requirements.txt it is recommended you use a virtualenv

```bash
git clone https://github.com/20miler10/flask-template.git
cd flask-template
python setup.py install
```

### Setting Up The Database

This project uses Postgres so make sure you have it installed first. Then you can setup the db using the following
commands:

```bash
createdb flask_template
python -m flask_template.manage db upgrade
```

#### Create A Database Revision

After making changes to the db models you can create a new version of the database using alembic:

```bash
python -m flask_template.manage db migrate -m "<commit message>"
```

Review the migration file and make sure everything is correct, then run:

```bash
python -m flask_template.manage db upgrade
```

### Running The Flask App

There are several ways to run the app, the easiest using the [heroku toolbelt](https://toolbelt.heroku.com/):

```bash
heroku local -e env.test
```

An alternative to using the heroku toolbelt is to use [honcho](https://honcho.readthedocs.org/en/latest/):

```bash
honcho -e .env.test start
```

Lastly you can manually run the application

```bash
python -m flask_template
```