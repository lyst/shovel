# -*- coding: utf-8 -*-
import os

import pytest


@pytest.fixture(autouse=True)
def force_no_aws_creds():
    """
    boto is mocked by moto, so nothing talks to S3, but if this goes wrong, it is preferable if
    the test framework doesn't start writing real data. This will enforce that.
    """
    assert os.environ.get('AWS_ACCESS_KEY_ID') is '', "AWS_ACCESS_KEY_ID must not be set"
    assert os.environ.get('AWS_SECRET_ACCESS_KEY') is '', "AWS_SECRET_ACCESS_KEY must not be set"
    assert os.environ.get('SHOVEL_DEFAULT_BUCKET') == 'test_bucket'
    assert os.environ.get('SHOVEL_DEFAULT_ROOT') == 'test_root'
