# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def api_app():
    from flask_template.main import api_app
    api_app.config['TESTING'] = True
    return api_app.test_client()


@pytest.fixture
def frontend_app():
    from flask_template.main import frontend_app
    frontend_app.config['TESTING'] = True
    return frontend_app.test_client()
