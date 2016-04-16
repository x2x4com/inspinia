# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import functools
import logging
import os

import celery
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from werkzeug.contrib.fixers import ProxyFix

from .core import db, mail, sentry
from .forms import RegisterForm, ConfirmRegisterForm
from .helpers import register_blueprints
from .models import User, Role


def create_app(package_name, package_path, settings_override=None, register_security_blueprint=True):
    app = Flask(package_name, instance_relative_config=True)
    app.config.from_object('{}.settings'.format(__package__))
    app.config.from_object(settings_override)

    db.init_app(app)
    mail.init_app(app)
    sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'), logging=True, level=logging.ERROR, wrap_wsgi=True)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    Security(app, user_datastore,
             register_blueprint=register_security_blueprint,
             register_form=RegisterForm,
             confirm_register_form=ConfirmRegisterForm)

    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):  # pylint: disable=unused-argument,unused-variable
        # Add default user role
        user_datastore.add_role_to_user(user, user_datastore.find_role('user'))
        db.session.add(user)
        db.session.commit()

    register_blueprints(app, package_name, package_path)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app


def create_celery_app(app=None):
    app = app or create_app(__name__, os.path.dirname(__file__))
    celery_app = celery.Celery(__package__)

    def on_configure(self):  # pylint: disable=unused-argument
        import raven
        from raven.contrib.celery import register_signal, register_logger_signal

        client = raven.Client(app.config.get('SENTRY_DSN'))

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

    celery_app.on_configure = functools.partial(on_configure, celery_app)
    celery_app.conf.update(app.config)
    TaskBase = celery_app.Task  # pylint: disable=invalid-name

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            # Run tasks in context of the flask app
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask  # pylint: disable=invalid-name

    return celery_app
