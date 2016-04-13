# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from functools import wraps

from flask import abort, jsonify, g
from flask_security import login_required
from werkzeug.exceptions import HTTPException

from .. import factory, settings, tasks
from ..core import sentry
from ..helpers import JSONEncoder


def create_app(settings_override=None, register_security_blueprint=False):
    app = factory.create_app(__name__, __path__, settings_override,
                             register_security_blueprint=register_security_blueprint)

    security_ctx = app.extensions['security']

    @security_ctx.send_mail_task
    def delay_security_email(msg):  # pylint: disable=unused-variable
        tasks.send_security_email.delay(msg)

    # Set the default JSON encoder
    app.json_encoder = JSONEncoder

    # Register custom error handlers so they all return JSON
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
    return jsonify(data), ex.code, {'Content-Type': 'application/json'}


def route(blueprint, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    if kwargs.pop('login_required', True):
        auth = login_required
    else:
        auth = lambda x: x

    def decorator(func):
        @blueprint.route(*args, **kwargs)
        @auth
        @wraps(func)
        def wrapper(*args, **kwargs):  # pylint: disable=unused-variable
            try:
                http_code = 200
                headers = {'Content-Type': 'application/json'}
                data = func(*args, **kwargs)
                if isinstance(data, tuple) and len(data) == 2:
                    http_code = data[1]
                    data = data[0]
                elif isinstance(data, tuple) and len(data) == 3:
                    headers.update(data[2])
                    http_code = data[1]
                    data = data[0]
                return jsonify(data), http_code, headers
            except HTTPException as ex:
                # These are normal HTTP exceptions that should be bubbled up
                if not settings.DEBUG and ex.code >= 500:
                    sentry.captureException()
                raise
            except Exception as ex:
                if settings.DEBUG:
                    raise
                sentry.captureException()
                abort(500, str(ex))

        return func

    return decorator
