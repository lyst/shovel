# -*- coding: utf-8 -*-
import os

from shovel import exceptions


def list_local(local_path):
    n = len(local_path)
    for dirpath, dirnames, filenames in os.walk(local_path):
        for filename in filenames:
            if filename.startswith('.'):
                continue

            local_key = os.path.join(dirpath, filename)[n:].lstrip('/')
            local_filename = os.path.join(local_path, local_key)
            yield local_key, local_filename


def get_local_filename(local_path, sufix):
    return os.path.join(local_path, sufix)


def ensure_dir_exists(local_path):
    try:
        os.makedirs(os.path.dirname(local_path))
    except FileExistsError:
        raise exceptions.FileExists
