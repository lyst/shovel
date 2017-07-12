# -*- coding: utf-8 -*-
import pytest

from shovel import exceptions, shovel


def test_shove_hello(hello_data):
    """
    Bury a "Hello World" text file into the default pit and dig it up again.
    """
    shovel.bury('test_project', 'test_dataset', 'v0', str(hello_data))
    assert len(hello_data.listdir()) == 1

    hello_data.remove()
    assert not hello_data.exists()

    shovel.dig('test_project', 'test_dataset', 'v0', str(hello_data))
    assert hello_data.exists()

    assert hello_data.join('hello.txt').exists()
    assert hello_data.join('hello.txt').read() == 'Hello World'


def test_shove_twice(hello_data):
    """
    bury a "Hello World" text file in the default pit and try to bury it again.
    """
    shovel.bury('test_project', 'test_dataset', 'v0', str(hello_data))
    with pytest.raises(exceptions.VersionExists):
        shovel.bury('test_project', 'test_dataset', 'v0', str(hello_data))


def test_dig_absent_data(hello_data):
    """
    Dig from a newly initialised bucket, wrong project, wrong dataset, wrong version.
    """
    project = 'test_project'
    dataset = 'test_dataset'
    version = 'v0'

    # Bucket just initialised
    with pytest.raises(exceptions.VersionDoesNotExist):
        shovel.dig(project, dataset, version, str(hello_data))
    shovel.bury(project, dataset, version, str(hello_data))
    hello_data.remove()
    shovel.dig(project, dataset, version, str(hello_data))

    # Missing project
    with pytest.raises(exceptions.VersionDoesNotExist):
        shovel.dig(project + '_x', dataset, version, str(hello_data))
    shovel.bury(project + '_x', dataset, version, str(hello_data))
    hello_data.remove()
    shovel.dig(project + '_x', dataset, version, str(hello_data))

    # Missing dataset
    with pytest.raises(exceptions.VersionDoesNotExist):
        shovel.dig(project, dataset + '_x', version, str(hello_data))
    shovel.bury(project, dataset + '_x', version, str(hello_data))
    hello_data.remove()
    shovel.dig(project, dataset + '_x', version, str(hello_data))

    # Missing version
    with pytest.raises(exceptions.VersionDoesNotExist):
        shovel.dig(project, dataset, 'v1', str(hello_data))
    shovel.bury(project, dataset, 'v1', str(hello_data))
    hello_data.remove()
    shovel.dig(project, dataset, 'v1', str(hello_data))


def test_download_when_file_exists(hello_data):
    """
    Diging a dataset into a location that already has files should fail.
    """
    shovel.bury('test_project', 'test_dataset', 'v0', str(hello_data))
    with pytest.raises(exceptions.FileExists):
        shovel.dig('test_project', 'test_dataset', 'v0', str(hello_data))
