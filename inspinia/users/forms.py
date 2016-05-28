# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask_security import forms
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(forms.RegisterForm):
    first_name = StringField('First Name', [DataRequired('First name not provided')])
    last_name = StringField('Last Name', [DataRequired('Last name not provided')])
    accept_tos = BooleanField('I agree to the terms', [DataRequired('You must accept the terms')])


class ConfirmRegisterForm(forms.ConfirmRegisterForm):
    first_name = StringField('First Name', [DataRequired('First name not provided')])
    last_name = StringField('Last Name', [DataRequired('Last name not provided')])
    accept_tos = BooleanField('I agree to the terms', [DataRequired('You must accept the terms')])
