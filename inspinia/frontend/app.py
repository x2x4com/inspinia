# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask import Blueprint, render_template
from flask_security import login_required

from . import route

bp = Blueprint('app', __name__)


@route(bp, '/')
@login_required
def index():
    return render_template('index.html')
