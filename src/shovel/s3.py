# -*- coding: utf-8 -*-
import os

from boto3 import client as boto_client

from shovel import exceptions, local

DEFAULT_DELIMITER = '/'


def get_s3_client():
    return boto_client('s3')


def get_prefix(root, *path, delimiter):
    return delimiter.join([root, *path, ''])


def list_nodes(bucket, root, *path, delimiter=DEFAULT_DELIMITER):
    """Return iterator of node names"""
    client = get_s3_client()
    paginator = client.get_paginator('list_objects_v2')

    prefix = get_prefix(root, *path, delimiter=delimiter)

    for result in paginator.paginate(Bucket=bucket, Delimiter=delimiter, Prefix=prefix):
        if result.get('CommonPrefixes') is not None:
            for l in result.get('CommonPrefixes'):
                yield l['Prefix'][len(prefix):].rstrip(delimiter)


def list_objects(bucket, root, *path, delimiter=DEFAULT_DELIMITER):
    """Return iterator of node names"""
    client = get_s3_client()

    prefix = get_prefix(root, *path, delimiter=delimiter)

    results = client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' not in results:
        return

    for result in results['Contents']:
        yield result['Key'][len(prefix):].strip(delimiter)


def download_tree(bucket, prefix, local_path):
    if os.path.exists(local_path):
        raise exceptions.FileExists

    client = get_s3_client()

    n = len(prefix)

    items = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    keys = [i['Key'] for i in items['Contents']]

    for key in keys:
        assert key[:n] == prefix, "key should start with prefix, {} / {}".format(prefix, key)
        suffix = key[n:].lstrip('/')
        local_filename = local.get_local_filename(local_path, suffix)
        local.ensure_dir_exists(local_filename)

        if os.path.exists(local_filename):
            raise exceptions.FileExists
        client.download_file(bucket, key, local_filename)


def put_objects(local_path, bucket, root, *path, delimiter=DEFAULT_DELIMITER):
    client = get_s3_client()

    prefix = get_prefix(root, *path, delimiter=delimiter)
    local_objects = local.list_local(local_path)
    for local_key, local_filename in local_objects:
        key = prefix + local_key
        client.upload_file(local_filename, bucket, key)


def get_objects(local_path, bucket, root, *path, delimiter=DEFAULT_DELIMITER):
    prefix = get_prefix(root, *path, delimiter=delimiter)
    download_tree(bucket, prefix, local_path)
