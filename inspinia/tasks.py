# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from .core import mail
from .factory import create_celery_app

celery = create_celery_app()


@celery.task
def send_security_email(msg):
    mail.send(msg)
