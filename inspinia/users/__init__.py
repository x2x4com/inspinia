# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from .models import User, Role
from ..core import Service


class UsersService(Service):
    __model__ = User


class RolesService(Service):
    __model__ = Role
