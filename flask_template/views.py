# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask_admin import AdminIndexView
from flask_admin.contrib.rediscli import RedisCli

from .core import UserRoleViewMixin
from .users.views import *


class AdminRoleIndexView(UserRoleViewMixin, AdminIndexView):
    __role__ = 'admin'


class SuperuserRedisCliView(UserRoleViewMixin, RedisCli):
    __role__ = 'superuser'

    def __init__(self, *args, **kwargs):
        super(SuperuserRedisCliView, self).__init__(*args, **kwargs)
        self.menu_icon_type = 'fa'
        self.menu_icon_value = 'fa-terminal'
