# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import json
from functools import wraps

from flask import g, current_app
from werkzeug.exceptions import HTTPException

from . import api_manager
from .. import factory, tasks


def create_app(settings_override=None, register_security_blueprint=False):
    app = factory.create_app(__name__, __path__, settings_override, register_security_blueprint)

    # Init API endpoints for models
    api_manager.init_app(app)

    # Setup security async email send
    security_ctx = app.extensions['security']

    @security_ctx.send_mail_task
    def delay_security_email(msg):  # pylint: disable=unused-variable
        tasks.send_security_email.delay(msg)

    # Register custom error handlers so they all return JSON
    if not app.debug:
        for http_exception_class in HTTPException.__subclasses__():
            app.errorhandler(http_exception_class.code)(handle_error)

    return app


def handle_error(ex):
    data = {
        'error': {
            'code': ex.code,
            'name': ex.name,
            'description': ex.description
        }
    }
    if hasattr(g, 'sentry_event_id') and g.sentry_event_id:
        data['error']['event_id'] = g.sentry_event_id
    return current_app.response_class(json.dumps(data), mimetype='application/json', status=ex.code)


def route(blueprint, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)
    kwargs.setdefault('methods', ['GET'])

    def decorator(func):
        @blueprint.route(*args, **kwargs)
        @wraps(func)
        def wrapper(*func_args, **func_kwargs):  # pylint: disable=unused-variable
            status = headers = None
            rv = func(*func_args, **func_kwargs)
            if isinstance(rv, tuple):
                rv, status, headers = rv + (None,) * (3 - len(rv))
            return current_app.response_class(json.dumps(rv), mimetype='application/json', status=status,
                                              headers=headers)

        return func

    return decorator
