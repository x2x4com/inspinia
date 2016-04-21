# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import logging

from flask_restless import APIManager, ProcessingException
from flask_security import auth_required, roles_accepted

from ..core import db
from ..models import User, Role


class ProcessingExceptionFilter(logging.Filter):
    def filter(self, rec):
        if hasattr(rec, 'exc_info') and isinstance(rec.exc_info, tuple) and len(rec.exc_info) == 3 and \
                        rec.exc_info[0] is ProcessingException:
            return False
        return True


def auth_func(*args, **kwargs):  # pylint: disable=unused-argument
    if auth_required('token')(lambda: None)() is not None:
        raise ProcessingException(status=401, detail='Unauthorized')


def admin_or_superuser(*args, **kwargs):  # pylint: disable=unused-argument
    if roles_accepted('admin', 'superuser')(lambda: None)():
        raise ProcessingException(status=403, detail='Forbidden')


admin_only_preprocessors = dict(
    GET_COLLECTION=[auth_func, admin_or_superuser],  # /api/user
    GET_RESOURCE=[auth_func, admin_or_superuser],  # /api/user/1
    GET_RELATION=[auth_func, admin_or_superuser],  # /api/user/1/articles
    GET_RELATED_RESOURCE=[auth_func],  # /api/user/1/articles/2
    DELETE_RESOURCE=[auth_func, admin_or_superuser],  # /api/user/1
    POST_RESOURCE=[auth_func, admin_or_superuser],  # /api/user
    PATCH_RESOURCE=[auth_func, admin_or_superuser],  # /api/user/1
    GET_RELATIONSHIP=[auth_func, admin_or_superuser],  # /api/user/1/relationships/articles
    DELETE_RELATIONSHIP=[auth_func, admin_or_superuser],  # /api/user/1/relationships/articles
    POST_RELATIONSHIP=[auth_func, admin_or_superuser],  # /api/user/1/relationships/articles
    PATCH_RELATIONSHIP=[auth_func, admin_or_superuser],  # /api/user/1/relationships/articles
)

all_methods = {'GET', 'POST', 'PUT', 'PATCH', 'DELETE'}


def init_app(app):
    manager = APIManager(app, flask_sqlalchemy_db=db)
    manager.create_api(User,
                       preprocessors=admin_only_preprocessors,
                       url_prefix='',
                       methods=all_methods,
                       max_page_size=100,
                       exclude=('password',))
    manager.create_api(Role,
                       preprocessors=admin_only_preprocessors,
                       url_prefix='',
                       methods=all_methods,
                       max_page_size=100)
    app.logger.addFilter(ProcessingExceptionFilter())
