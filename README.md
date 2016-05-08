# flask-template

Template flask application using Flask-Admin, Flask-Security, SQLAlchemy, Sentry, and Celery among other common flask
extensions.

***

### Install

> Due to a strict requirements.txt/install-requirements.txt it is recommended you use a virtualenv

```bash
git clone https://github.com/20miler10/flask-template.git
cd flask-template
python setup.py install
```

***

### Setting Up The Database

This project uses Postgres so make sure you have it installed first. Then you can setup the db using the following
commands:

```bash
createdb flask_template
python -m flask_template.manage db upgrade
```

#### Creating A Database Revision

After making changes to the db models you can create a new version of the database using alembic:

```bash
python -m flask_template.manage db migrate -m "<commit message>"
```

Review the migration file and make sure everything is correct, then run:

```bash
python -m flask_template.manage db upgrade
```

***

### Running The Flask App

There are several ways to run the app, the easiest using the [heroku toolbelt](https://toolbelt.heroku.com/):

```bash
heroku local -e env.dev
```

An alternative to using the heroku toolbelt is to use [honcho](https://honcho.readthedocs.org/en/latest/):

```bash
honcho -e .env.dev start
```

Lastly you can manually run the application using strictly environment variable configuration:

```bash
python -m flask_template.main
# In a separate shell
celery worker -A flask_template.tasks
```

***

### Configuration

All configuration is contained in the environment. You can check the current settings with the fllowing command:

```bash
python -m flask_template.settings
```

Or retrieve a single setting:

```bash
python -m flask_template.settings <setting_name>
```

***

### Makefile Targets

> Makefile commands will only work inside a [virtualenv]() or a [condaenv]()

#### `make init`

Initializes the virtualenv with an up-to-date version of setuptools, pip, and installs [pip-tools]().

#### `make install`

[pip-compiles]() requirements.txt and install-requirements.txt then [pip-syncs]() the environment.

#### `make requirements.txt`

[pip-compiles]() requirements.txt

#### `make install-requirements.txt`

[pip-compiles]() install-requirements.txt

#### `make check`

Runs the `lint` and `test` Makefile targets.

#### `make lint`

Runs [pylint]() on all packages and modules.

#### `make test`

Runs [py.test]() with tests located inside the tests/ folder as well as any tests nested in project level packages and
submodules. Coverage is also calculated when running all tests.

#### `make test-unit`

Same as `make test` excluding coverage and tests marked as `integration`.

#### `make test-integration`

Same as `make test` excluding coverage and tests **not** marked as `integration`.

#### `make build`

Builds a wheel using setuptools' bdist_wheel command.

#### `make clean`

Cleans the project of compiled python files and files generated by the above comands such as build and dist directories.
