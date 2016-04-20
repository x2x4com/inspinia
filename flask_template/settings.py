# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import os
import re

email_pattern = re.compile(r'^([\w ]+)\s+<(.*?@.*?)>$')


def get_int_env_var(name, default):
    try:
        return int(os.environ.get(name) or default)
    except:
        raise AssertionError("Environment variable '{}' must be an integer".format(name))


def get_bool_env_var(name, default):
    value = (os.environ.get(name) or str(default)).lower()
    if value not in ['true', 'false']:
        raise AssertionError("Environment variable '{}' must be 'true' or 'false' (case-insensitive)".format(name))
    return value == 'true'


def get_str_env_var(name, default=None):
    return os.environ.get(name) or default


def parse_email(raw_string):
    match = email_pattern.match(raw_string.strip())
    if match:
        return match.group(1), match.group(2)
    raise ValueError('Invalid email "{}". Ex. "Jane Doe <jane@example.com>"'.format(raw_string))


# App config
DEBUG = get_bool_env_var('DEBUG', True)
APP_NAME = get_str_env_var('APP_NAME', 'Flask Template')
SECRET_KEY = get_str_env_var('SECRET_KEY', 'secret-key')

WTF_CSRF_ENABLED = False

# SQLAlchemy config
SQLALCHEMY_DATABASE_URI = get_str_env_var('SQLALCHEMY_DATABASE_URI',
                                          get_str_env_var('DATABASE_URL', 'postgresql://localhost:5432/flask_template'))
SQLALCHEMY_TRACK_MODIFICATIONS = get_bool_env_var('SQLALCHEMY_TRACK_MODIFICATIONS', False)

CACHE_TYPE = 'redis'
CACHE_REDIS_URL = get_str_env_var('CACHE_REDIS_URL', get_str_env_var('REDIS_URL', 'redis://localhost:6379/0'))

# Mail config
MAIL_SERVER = get_str_env_var('MAIL_SERVER', get_str_env_var('POSTMARK_SMTP_SERVER'))
MAIL_PORT = get_int_env_var('MAIL_PORT', get_int_env_var('POSTMARK_SMTP_PORT', 587))
MAIL_USE_TLS = get_bool_env_var('MAIL_USE_TLS', True)
MAIL_USE_SSL = get_bool_env_var('MAIL_USE_SSL', False)
MAIL_USERNAME = get_str_env_var('MAIL_USERNAME', get_str_env_var('POSTMARK_API_KEY'))
MAIL_PASSWORD = get_str_env_var('MAIL_PASSWORD', get_str_env_var('POSTMARK_API_KEY'))
MAIL_DEFAULT_SENDER = get_str_env_var('MAIL_DEFAULT_SENDER', 'no-reply@localhost')
MAIL_SUPPRESS_SEND = get_bool_env_var('MAIL_SUPPRESS_SEND', True)

# Celery config
BROKER_URL = get_str_env_var('BROKER_URL', get_str_env_var('REDIS_URL', 'redis://localhost:6379/0'))
CELERYD_CONCURRENCY = get_int_env_var('CELERYD_CONCURRENCY', 1)
CELERYD_TASK_SOFT_TIME_LIMIT = get_int_env_var('CELERYD_TASK_SOFT_TIME_LIMIT', 60 * 45)
CELERYD_TASK_TIME_LIMIT = get_int_env_var('CELERYD_TASK_TIME_LIMIT', 60 * 60)
CELERY_ENABLE_UTC = get_bool_env_var('CELERY_ENABLE_UTC', True)
CELERY_MESSAGE_COMPRESSION = get_str_env_var('CELERY_MESSAGE_COMPRESSION', 'gzip')
CELERY_RESULT_BACKEND = get_str_env_var('CELERY_RESULT_BACKEND')

# Celery Mail config, defaults to the Mail config
CELERY_SEND_TASK_ERROR_EMAILS = get_bool_env_var('CELERY_SEND_TASK_ERROR_EMAILS', False)
ADMINS = [parse_email(admin) for admin in get_str_env_var('ADMINS', '').split(',') if admin.strip()]
SERVER_EMAIL = get_str_env_var('SERVER_EMAIL', MAIL_DEFAULT_SENDER)
EMAIL_HOST = get_str_env_var('EMAIL_HOST', MAIL_SERVER)
EMAIL_PORT = get_int_env_var('EMAIL_PORT', MAIL_PORT)
EMAIL_HOST_USER = get_str_env_var('EMAIL_HOST_USER', MAIL_USERNAME)
EMAIL_HOST_PASSWORD = get_str_env_var('EMAIL_HOST_PASSWORD', MAIL_PASSWORD)
EMAIL_USE_SSL = get_bool_env_var('EMAIL_USE_SSL', MAIL_USE_SSL)
EMAIL_USE_TLS = get_bool_env_var('EMAIL_USE_TLS', MAIL_USE_TLS)

# Security config
SECURITY_BLUEPRINT_NAME = get_str_env_var('SECURITY_BLUEPRINT_NAME', 'security')
SECURITY_URL_PREFIX = get_str_env_var('SECURITY_URL_PREFIX', None)
SECURITY_FLASH_MESSAGES = get_bool_env_var('SECURITY_FLASH_MESSAGES', True)
SECURITY_PASSWORD_HASH = get_str_env_var('SECURITY_PASSWORD_HASH', 'sha512_crypt')
SECURITY_PASSWORD_SALT = get_str_env_var('SECURITY_PASSWORD_SALT', 'password-salt')
SECURITY_LOGIN_URL = get_str_env_var('SECURITY_LOGIN_URL', '/login')
SECURITY_LOGOUT_URL = get_str_env_var('SECURITY_LOGOUT_URL', '/logout')
SECURITY_REGISTER_URL = get_str_env_var('SECURITY_REGISTER_URL', '/register')
SECURITY_RESET_URL = get_str_env_var('SECURITY_RESET_URL', '/reset-password')
SECURITY_CHANGE_URL = get_str_env_var('SECURITY_CHANGE_URL', '/change-password')
SECURITY_CONFIRM_URL = get_str_env_var('SECURITY_CONFIRM_URL', '/confirm-account')
SECURITY_CONFIRM_ERROR_VIEW = get_str_env_var('SECURITY_CONFIRM_ERROR_VIEW', None)
SECURITY_POST_LOGIN_VIEW = get_str_env_var('SECURITY_POST_LOGIN_VIEW', '/')
SECURITY_POST_LOGOUT_VIEW = get_str_env_var('SECURITY_POST_LOGOUT_VIEW', '/login')
SECURITY_POST_REGISTER_VIEW = get_str_env_var('SECURITY_POST_REGISTER_VIEW', '/login')
SECURITY_POST_CONFIRM_VIEW = get_str_env_var('SECURITY_POST_CONFIRM_VIEW', '/login')
SECURITY_POST_RESET_VIEW = get_str_env_var('SECURITY_POST_RESET_VIEW', '/login')
SECURITY_POST_CHANGE_VIEW = get_str_env_var('SECURITY_POST_CHANGE_VIEW', '/')
SECURITY_UNAUTHORIZED_VIEW = get_str_env_var('SECURITY_UNAUTHORIZED_VIEW', lambda: None)
SECURITY_FORGOT_PASSWORD_TEMPLATE = get_str_env_var('SECURITY_FORGOT_PASSWORD_TEMPLATE',
                                                    'security/forgot_password.html')
SECURITY_LOGIN_USER_TEMPLATE = get_str_env_var('SECURITY_LOGIN_USER_TEMPLATE', 'security/login_user.html')
SECURITY_REGISTER_USER_TEMPLATE = get_str_env_var('SECURITY_REGISTER_USER_TEMPLATE', 'security/register_user.html')
SECURITY_RESET_PASSWORD_TEMPLATE = get_str_env_var('SECURITY_RESET_PASSWORD_TEMPLATE', 'security/reset_password.html')
SECURITY_CHANGE_PASSWORD_TEMPLATE = get_str_env_var('SECURITY_CHANGE_PASSWORD_TEMPLATE',
                                                    'security/change_password.html')
SECURITY_SEND_CONFIRMATION_TEMPLATE = get_str_env_var('SECURITY_SEND_CONFIRMATION_TEMPLATE',
                                                      'security/send_confirmation.html')
SECURITY_SEND_LOGIN_TEMPLATE = get_str_env_var('SECURITY_SEND_LOGIN_TEMPLATE', 'security/send_login.html')
SECURITY_CONFIRMABLE = get_bool_env_var('SECURITY_CONFIRMABLE', True)
SECURITY_REGISTERABLE = get_bool_env_var('SECURITY_REGISTERABLE', True)
SECURITY_RECOVERABLE = get_bool_env_var('SECURITY_RECOVERABLE', True)
SECURITY_TRACKABLE = get_bool_env_var('SECURITY_TRACKABLE', True)
SECURITY_PASSWORDLESS = get_bool_env_var('SECURITY_PASSWORDLESS', False)
SECURITY_CHANGEABLE = get_bool_env_var('SECURITY_CHANGEABLE', True)
SECURITY_SEND_REGISTER_EMAIL = get_bool_env_var('SECURITY_SEND_REGISTER_EMAIL', True)
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = get_bool_env_var('SECURITY_SEND_PASSWORD_CHANGE_EMAIL', True)
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = get_bool_env_var('SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL', True)
SECURITY_LOGIN_WITHIN = get_str_env_var('SECURITY_LOGIN_WITHIN', '1 days')
SECURITY_CONFIRM_EMAIL_WITHIN = get_str_env_var('SECURITY_CONFIRM_EMAIL_WITHIN', '5 days')
SECURITY_RESET_PASSWORD_WITHIN = get_str_env_var('SECURITY_RESET_PASSWORD_WITHIN', '5 days')
SECURITY_LOGIN_WITHOUT_CONFIRMATION = get_bool_env_var('SECURITY_LOGIN_WITHOUT_CONFIRMATION', False)
SECURITY_EMAIL_SENDER = get_str_env_var('SECURITY_EMAIL_SENDER', 'no-reply@localhost')
SECURITY_TOKEN_AUTHENTICATION_KEY = get_str_env_var('SECURITY_TOKEN_AUTHENTICATION_KEY', 'auth_token')
SECURITY_TOKEN_AUTHENTICATION_HEADER = get_str_env_var('SECURITY_TOKEN_AUTHENTICATION_HEADER', 'Authentication-Token')
SECURITY_TOKEN_MAX_AGE = get_int_env_var('SECURITY_TOKEN_MAX_AGE', 60 * 60 * 24 * 365)
SECURITY_CONFIRM_SALT = get_str_env_var('SECURITY_CONFIRM_SALT', 'confirm-salt')
SECURITY_RESET_SALT = get_str_env_var('SECURITY_RESET_SALT', 'reset-salt')
SECURITY_LOGIN_SALT = get_str_env_var('SECURITY_LOGIN_SALT', 'login-salt')
SECURITY_CHANGE_SALT = get_str_env_var('SECURITY_CHANGE_SALT', 'change-salt')
SECURITY_REMEMBER_SALT = get_str_env_var('SECURITY_REMEMBER_SALT', 'remember-salt')
SECURITY_DEFAULT_REMEMBER_ME = get_bool_env_var('SECURITY_DEFAULT_REMEMBER_ME', False)
SECURITY_DEFAULT_HTTP_AUTH_REALM = get_str_env_var('SECURITY_DEFAULT_HTTP_AUTH_REALM', 'Login Required')
SECURITY_EMAIL_SUBJECT_REGISTER = get_str_env_var('SECURITY_EMAIL_SUBJECT_REGISTER', 'Welcome!')
SECURITY_EMAIL_SUBJECT_CONFIRM = get_str_env_var('SECURITY_EMAIL_SUBJECT_CONFIRM', 'Please confirm your email')
SECURITY_EMAIL_SUBJECT_PASSWORDLESS = get_str_env_var('SECURITY_EMAIL_SUBJECT_PASSWORDLESS', 'Login instructions')
SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = get_str_env_var('SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE',
                                                         'Your password has been reset')
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = get_str_env_var('SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE',
                                                                'Your password has been changed')
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = get_str_env_var('SECURITY_EMAIL_SUBJECT_PASSWORD_RESET',
                                                        'Password reset instructions')

# Sentry config
SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_TRANSPORT = 'raven.transport.gevent.GeventedHTTPTransport'
SENTRY_SITE_NAME = APP_NAME
SENTRY_USER_ATTRS = [attr.strip()
                     for attr in get_str_env_var('SENTRY_USER_ATTRS', 'first_name, last_name, email').split(',')
                     if attr.strip()]

if __name__ == '__main__':
    print('\n'.join('{}={}'.format(prop, globals()[prop])
                    for prop in sorted(globals().keys())
                    if re.match(r'[A-Z][A-Z0-9_]+', prop)))
