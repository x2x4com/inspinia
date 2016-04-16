# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import importlib
import pkgutil

from flask import Blueprint, json


def register_blueprints(app, package_name, package_path):
    registered_views = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(module):
            item = getattr(module, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            registered_views.append(item)
    return registered_views


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, JSONSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JSONSerializer(object):
    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for prop in self.__mapper__.iterate_properties:
            yield prop.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv
