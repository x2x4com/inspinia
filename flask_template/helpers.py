# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import pkgutil

from flask import Blueprint

from ._compat import import_module


def register_blueprints(app, package_name, package_path):
    registered_views = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        module = import_module('%s.%s' % (package_name, name))
        for item in dir(module):
            item = getattr(module, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            registered_views.append(item)
    return registered_views
