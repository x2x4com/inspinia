# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from inspinia import api, frontend

frontend_app = frontend.create_app()
api_app = api.create_app()

app = DispatcherMiddleware(frontend_app, {'/api': api_app})

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app, use_reloader=True, use_debugger=True)
