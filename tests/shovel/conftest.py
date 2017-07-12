# -*- coding: utf-8 -*-
from moto import mock_s3

import pytest

from shovel import s3, shovel


@pytest.fixture(autouse=True)
def default_bucket():
    """
    This fixture sets up the defaut bucket with moto.

    This fixture is called once per test. Combined with autouse, this means you can just use boto
    in any test and this test will ensure the bucket is present and boto is suitably mocked out.
    Nesting moto doesn't seem to work well.
    """
    config = shovel.get_default_config()

    with mock_s3():
        s3_client = s3.get_s3_client()
        s3_client.create_bucket(Bucket=config.bucket)

        yield


@pytest.fixture
def hello_data(tmpdir):
    data_folder_name = "data"
    data_dir = tmpdir.mkdir(data_folder_name)

    hello = data_dir.join('hello.txt')
    hello.write("Hello World")
    with open(hello.strpath, 'r') as f:
        assert f.read() == "Hello World"
    yield data_dir
