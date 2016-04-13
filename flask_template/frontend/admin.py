# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from celery.backends import get_backend_by_url
from celery.backends.redis import RedisBackend
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from redis import Redis

from ..core import db
from ..models import Role, User
from ..views import AdminRoleIndexView, SuperuserRedisCliView, RoleView, UserView


def init_app(app):
    admin = Admin(app,
                  name=app.config['APP_NAME'],
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
    # Add Redis console
    backend, url = get_backend_by_url(app.config['BROKER_URL'])
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
