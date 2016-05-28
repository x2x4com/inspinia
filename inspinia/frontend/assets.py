# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask_assets import Bundle, Environment

# Vendor css bundle. Linked first in all endpoints.
css_vendor = Bundle('css/bootstrap.min.css',
                    'css/font-awesome.min.css',
                    filters='cssmin', output='css/vendor.min.css')

# Plugin css bundle. Linked after the vendor bundle.
css_plugins = Bundle('css/animate.css',
                     filters='cssmin', output='css/plugins.min.css')

# Application css bundle. Linked after the plugin bundle.
css_app = Bundle(Bundle('less/app.less', filters='less', output='css/app.css', debug=False),
                 filters='cssmin', output='css/style.min.css')

# Vendor js bundle. Linked first in all endpoints at the end of the page body.
js_vendor = Bundle('js/jquery.js',
                   'js/bootstrap.min.js',
                   filters='jsmin', output='js/vendor.min.js')

# Plugin js bundle. Linked after the vendor bundle.
js_plugins = Bundle('js/plugins/slimscroll/jquery.slimscroll.min.js',
                    'js/plugins/pace/pace.min.js',
                    filters='jsmin', output='js/plugins.min.js')

# Application js bundle. Linked after the plugin bundle.
js_main = Bundle('js/app.js', filters='jsmin', output='js/app.min.js')


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_vendor', css_vendor)
    webassets.register('css_plugins', css_plugins)
    webassets.register('css_app', css_app)
    webassets.register('js_vendor', js_vendor)
    webassets.register('js_plugins', js_plugins)
    webassets.register('js_main', js_main)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
