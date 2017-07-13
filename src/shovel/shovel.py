# -*- coding: utf-8 -*-
import os

from shovel.config import Config
from shovel.pit import Pit

DEFAULT_BUCKET = os.environ.get('SHOVEL_DEFAULT_BUCKET')
DEFAULT_ROOT = os.environ.get('SHOVEL_DEFAULT_ROOT') or 'bottomless-pit'


def bury(project, name, version, local_path, force=False):
    """Upload the contents of the target path to the pit."""
    pit = get_default_pit()
    pit.bury(project, name, version, local_path, force)


def dig(project, name, version, local_path):
    """Download the contents of the target dataset from the pit."""
    pit = get_default_pit()
    pit.dig(project, name, version, local_path)


def peek(project=None, name=None, version=None, *, local_path=None):
    pit = get_default_pit()
    return pit.peek(project, name, version, local_path=local_path)


def get_default_config():
    return Config(bucket=DEFAULT_BUCKET, root=DEFAULT_ROOT)


def get_default_pit():
    config = get_default_config()
    return Pit(config.bucket, config.root)
