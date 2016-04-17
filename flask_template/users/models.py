# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask_security import UserMixin, RoleMixin
from sqlalchemy import func

from ..core import db
from ..helpers import JSONSerializer

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin, JSONSerializer):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)  # pylint: disable=invalid-name
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '%s(id=%d, name=%s)' % (self.__class__.__name__, self.id, self.name)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin, JSONSerializer):
    __tablename__ = 'users'
    __json_hidden__ = ['password', 'last_login_ip', 'current_login_ip']
    __json_modifiers__ = {'roles': lambda roles, model: [str(role) for role in roles]}

    id = db.Column(db.Integer(), primary_key=True)  # pylint: disable=invalid-name
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    registered_at = db.Column(db.DateTime(), default=func.now())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '%s(id=%d, email=%s)' % (self.__class__.__name__, self.id, self.email)

    def __str__(self):
        return '{u.first_name} {u.last_name} <{u.email}>'.format(u=self)
