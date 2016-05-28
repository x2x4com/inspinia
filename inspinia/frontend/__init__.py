# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from functools import wraps

from flask import render_template, request
from werkzeug.exceptions import InternalServerError, NotFound, Unauthorized, Forbidden

from . import assets, admin
from .. import factory, tasks


def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    # Configure the jinja2 environment
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.auto_reload = app.config.get('DEBUG', True)

    # Init assets
    assets.init_app(app)

    # Init admin
    admin.init_app(app)

    # Setup security async email send
    security_ctx = app.extensions['security']

    @security_ctx.send_mail_task
    def delay_security_email(msg):  # pylint: disable=unused-variable
        tasks.send_security_email.delay(msg)

    # Register custom error handlers
    if not app.debug:
        for ex in [InternalServerError, NotFound, Unauthorized, Forbidden]:
            app.errorhandler(ex.code)(handle_error)

    return app


def handle_error(error):
    return render_template('error.html', error=error, return_url=request.args.get('return_url'))


def route(blueprint, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)
    kwargs.setdefault('methods', ['GET'])

    def decorator(func):
        @blueprint.route(*args, **kwargs)
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):  # pylint: disable=unused-variable
            return func(*func_args, **func_kwargs)

        return func

    return decorator
