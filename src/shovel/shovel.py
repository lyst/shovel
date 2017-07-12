# -*- coding: utf-8 -*-
import os

from shovel.config import Config
from shovel.pit import Pit

DEFAULT_BUCKET = os.environ.get('SHOVEL_DEFAULT_BUCKET')
DEFAULT_ROOT = os.environ.get('SHOVEL_DEFAULT_ROOT') or 'bottomless-pit'


def bury(project, name, version, local_path):
    pit = get_default_pit()
    pit.bury(project, name, version, local_path)


def dig(project, name, version, local_path):
    pit = get_default_pit()
    pit.dig(project, name, version, local_path)


def peek(project, name):
    pit = get_default_pit()
    versions = pit.list_versions(project, name)
    return {
        version: pit.list_contents(project, name, version)
        for version in versions
    }


def get_default_config():
    return Config(bucket=DEFAULT_BUCKET, root=DEFAULT_BUCKET)


def get_default_pit():
    config = get_default_config()
    return Pit(config.bucket, config.root)
