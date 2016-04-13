# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask_script import prompt, prompt_pass, Manager
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict

from .forms import RegisterForm
from ..services import users, roles

user_manager = Manager(usage='Perform database operations on users')


@user_manager.option('-f', '--first_name', dest='first_name')
@user_manager.option('-l', '--last_name', dest='last_name')
@user_manager.option('-e', '--email', dest='email')
@user_manager.option('-p', '--password', dest='password')
def create(first_name=None, last_name=None, email=None, password=None):
    first_name = first_name or prompt('First Name'),
    last_name = last_name or prompt('Last Name'),
    email = email or prompt('Email'),
    password = password or prompt_pass('Password')
    form = RegisterForm(MultiDict(dict(first_name=first_name,
                                       last_name=last_name,
                                       email=email,
                                       password=password,
                                       password_confirm=prompt_pass('Confirm Password'),
                                       accept_tos=True)), csrf_enabled=False)
    if form.validate():
        user = register_user(first_name=first_name, last_name=last_name, email=email, password=password)
        print('%s created successfully' % repr(user))
        return
    print('Error creating user:')
    for errors in form.errors.values():
        print('\n'.join(errors))


@user_manager.option('-e', '--email', dest='email')
def delete(email=None):
    email = email or prompt('Email')
    user = users.first(email=email)
    if not user:
        print('No user found with email %s' % email)
        return
    users.delete(user)
    print('%s deleted successfully' % repr(user))


@user_manager.option('-e', '--email', dest='email')
@user_manager.option('-r', '--role', dest='role')
def add_role(email=None, role=None):
    email = email or prompt('Email')
    user = users.first(email=email)
    if not user:
        print('No user found with email %s' % email)
        return
    role = role or prompt('Role')
    role = roles.first(name=role)
    if not role:
        print('No role found with name %s' % role)
        return
    if role not in user.roles:
        user.roles.append(role)
        users.save(user)
        print('Successfully added %s to %s' % (repr(role), repr(user)))
    else:
        print('%s already has %s' % (repr(user), repr(role)))


@user_manager.option('-e', '--email', dest='email')
@user_manager.option('-r', '--role', dest='role')
def remove_role(email=None, role=None):
    email = email or prompt('Email')
    user = users.first(email=email)
    if not user:
        print('No user found with email %s' % email)
        return
    role = role or prompt('Role')
    role = roles.first(name=role)
    if not role:
        print('No role found with name %s' % role)
        return
    if role in user.roles:
        user.roles.remove(role)
        users.save(user)
        print('Successfully removed %s from %s' % (repr(role), repr(user)))
    else:
        print('%s does not have %s' % (repr(user), repr(role)))


@user_manager.command
def list_all():
    for user in users.all():
        print(repr(user))


role_manager = Manager(usage='Perform database operations on roles')


@role_manager.option('-n', '--name', dest='name')
@role_manager.option('-d', '--description', dest='description')
def create(name=None, description=None):
    name = name or prompt('Name'),
    description = description or prompt('Description'),
    role = roles.new(name=name, description=description)
    roles.save(role)
    print('%s created successfully' % repr(role))
    return


@role_manager.option('-n', '--name', dest='name')
def delete(name=None):
    name = name or prompt('Name')
    role = roles.first(name=name)
    if not role:
        print('No role found with name %s' % name)
        return
    roles.delete(role)
    print('%s deleted successfully' % repr(role))


@role_manager.command
def list_all():
    for role in roles.all():
        print(repr(role))
