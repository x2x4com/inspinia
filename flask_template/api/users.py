# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask import Blueprint
from flask_login import current_user

from . import route

bp = Blueprint('users', __name__, url_prefix='/users')


@route(bp, '/whoami')
def whoami():
    """Returns the user instance of the currently authenticated user."""
    return dict(user=current_user._get_current_object())
