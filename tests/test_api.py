# -*- coding: utf-8 -*-
import pytest


@pytest.mark.integration
def test_fake_int(api_app):
    assert True


def test_fake_unit(api_app):
    assert True
