# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

import os

from flask_assets import ManageAssets
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from .core import db
from .main import frontend_app
from .users.manage import user_manager, role_manager

migrate = Migrate(frontend_app, db, directory=os.path.join(os.path.dirname(__file__), 'migrations'))
manager = Manager(frontend_app)

manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets())
manager.add_command('users', user_manager)
manager.add_command('roles', role_manager)

if __name__ == '__main__':
    manager.run()
