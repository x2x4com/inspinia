# -*- coding: utf-8 -*-
import pytest


@pytest.mark.integration
def test_fake_int(frontend_app):
    assert True


def test_fake_unit(frontend_app):
    assert True
