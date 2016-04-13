# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask import flash
from flask_admin.actions import action
from flask_admin.babel import ngettext, gettext
from wtforms.validators import required, email, ip_address

from ..core import AdminRoleModelView
from ..services import users


class UserView(AdminRoleModelView):
    column_list = ('id', 'first_name', 'last_name', 'email', 'active', 'login_count', 'roles')
    column_searchable_list = ('id','first_name', 'last_name', 'email', 'last_login_ip', 'current_login_ip')
    column_filters = ('id', 'first_name', 'last_name', 'email', 'active', 'confirmed_at', 'registered_at',
                      'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count', u'roles')
    column_editable_list = ('first_name', 'last_name', 'email', 'active', 'confirmed_at', 'registered_at',
                            'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count')
    form_columns = ('first_name', 'last_name', 'email', 'active', 'confirmed_at', 'registered_at', 'last_login_at',
                    'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count', 'roles')
    form_args = {
        'first_name': {
            'validators': [required()]
        },
        'last_name': {
            'validators': [required()]
        },
        'email': {
            'validators': [required(), email()]
        },
        'last_login_ip': {
            'validators': [ip_address()]
        },
        'current_login_ip': {
            'validators': [ip_address()]
        },
    }

    @action('set_active', 'Set Active')
    def set_active(self, ids):
        try:
            count = 0
            for user in users.get_all(*ids):
                users.update(user, active=True)
                count += 1

            flash(ngettext('User(s) successfully set to active.',
                           '%(count)s users were successfully activate.',
                           count,
                           count=count))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to set user(s) to active. %(error)s', error=str(ex)), 'error')

    @action('set_inactive', 'Set Inactive')
    def set_inactive(self, ids):
        try:
            count = 0
            for user in users.get_all(*ids):
                users.update(user, active=False)
                count += 1

            flash(ngettext('User(s) successfully set to inactive.',
                           '%(count)s users were successfully deactivated.',
                           count,
                           count=count))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise
            flash(gettext('Failed to set user(s) to inactive. %(error)s', error=str(ex)), 'error')


class RoleView(AdminRoleModelView):
    column_list = ('id', 'name', 'description')
    column_searchable_list = ('id', 'name', 'description')
    column_filters = ('id', 'name', 'description')
    column_editable_list = ('name', 'description')
    form_columns = ('name', 'description', 'users')
    form_args = {
        'name': {
            'validators': [required()]
        },
        'description': {
            'validators': [required()]
        }
    }
