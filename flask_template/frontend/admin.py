# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from celery.backends import get_backend_by_url
from celery.backends.redis import RedisBackend
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.rediscli import RedisCli
from flask_admin import helpers as admin_helpers
from redis import Redis

from .. import __pkg_name__
from ..core import db, UserRoleViewMixin
from ..models import Role, User
from ..views import RoleView, UserView


class AdminRoleIndexView(UserRoleViewMixin, AdminIndexView):
    __role__ = 'admin'


class SuperuserRedisCliView(UserRoleViewMixin, RedisCli):
    __role__ = 'superuser'

    def __init__(self, *args, **kwargs):
        super(SuperuserRedisCliView, self).__init__(*args, **kwargs)
        self.menu_icon_type = 'fa'
        self.menu_icon_value = 'fa-terminal'


def init_app(app):
    admin = Admin(app,
                  name=app.config.get('APP_NAME', __pkg_name__),
                  index_view=AdminRoleIndexView(menu_icon_type='fa', menu_icon_value='fa-home'),
                  base_template='admin_master.html',
                  template_mode='bootstrap3',
                  category_icon_classes={
                      'Models': 'fa fa-database',
                      'Tools': 'fa fa-briefcase',
                      'Home': 'fa fa-home'
                  })
    # Add model views
    admin.add_view(RoleView(Role, db.session, name='Roles', endpoint='roles', category='Models',
                            menu_icon_type='fa', menu_icon_value='fa-user-plus'))
    admin.add_view(UserView(User, db.session, name='Users', endpoint='users', category='Models',
                            menu_icon_type='fa', menu_icon_value='fa-users'))
    # Add Redis console for Celery broker
    backend, url = get_backend_by_url(app.config.get('BROKER_URL'))
    if backend is RedisBackend:
        admin.add_view(SuperuserRedisCliView(Redis.from_url(url), name='Redis CLI', endpoint='rediscli',
                                             category='Tools'))

    security_ctx = app.extensions['security']

    @security_ctx.context_processor
    def security_context_processor():  # pylint: disable=unused-variable
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
        )
