# -*- coding: utf-8 -*-
import os

import pytest


@pytest.fixture(autouse=True)
def force_no_aws_creds():
    """
    Ensure boto is mocked by moto, so nothing talks to S3, but if this goes wrong, it is preferable if
    the test framework doesn't start writing real data. This will enforce that.
    """
    os.environ['SHOVEL_DEFAULT_BUCKET'] = 'test_bucket'
    os.environ['SHOVEL_DEFAULT_ROOT'] = 'test_root'

    assert os.environ.get('AWS_ACCESS_KEY_ID') == 'foobar_key', f"AWS_ACCESS_KEY_ID should be mocked by moto"
    assert os.environ.get('AWS_SECRET_ACCESS_KEY') == 'foobar_secret', "AWS_SECRET_ACCESS_KEY must not be set"
    assert os.environ.get('SHOVEL_DEFAULT_BUCKET') == 'test_bucket'
    assert os.environ.get('SHOVEL_DEFAULT_ROOT') == 'test_root'
