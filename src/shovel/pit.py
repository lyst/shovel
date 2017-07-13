# -*- coding: utf-8 -*-
from shovel import exceptions, local, s3


def _version_parser(version):
    error_msg = 'versions should be in the format f"v{int(version[1:])}"'
    if version[0] != 'v':
        raise exceptions.VersionError(error_msg, version)
    try:
        return int(version[1:])
    except ValueError:
        raise exceptions.VersionError(error_msg, version)


def _get_latest_version(versions):
    return max(versions, key=_version_parser)


class Pit(object):
    def __init__(self, bucket, root):
        if bucket is None:
            raise ValueError("Bucket must not be None (Did you set SHOVEL_DEFAULT_BUCKET?)")
        if root is None:
            raise ValueError("Root must not be None (Did you set SHOVEL_DEFAULT_ROOT?)")
        self.bucket = bucket
        self.root = root

    def bury(self, project, name, version, working_path, force=False, ignore_exists=False):
        """Upload the contents of the target path to the pit."""
        if force and ignore_exists:
            raise ValueError("force and ignore_exists cannot both be True")
        _version_parser(version)
        if not force and self._list_contents(project, name, version):
            if ignore_exists:
                return
            raise exceptions.VersionExists

        s3.put_objects(working_path, self.bucket, self.root, project, name, version)

    def dig(self, project, name, version, working_path):
        """Download the contents of the target dataset from the pit."""
        _version_parser(version)
        if not self._list_contents(project, name, version):
            raise exceptions.VersionDoesNotExist

        s3.get_objects(working_path, self.bucket, self.root, project, name, version)

    def peek(self, project=None, name=None, version=None, *, local_path=None):
        if project is None:
            return self._list_projects()
        if name is None:
            return self._list_datasets(project)
        if version is None:
            return self._list_versions(project, name)
        if local_path is None:
            return self._list_contents(project, name, version)

        # if all args are provided, check they match
        remote_files = self._list_contents(project, name, version)
        local_files = [fname for fname, path in local.list_local(local_path)]

        if sorted(local_files) != sorted(remote_files):
            raise exceptions.OutOfSync(local_files, remote_files)

        return remote_files

    def _list_projects(self):
        """Return list of projects"""
        return list(s3.list_nodes(self.bucket, self.root))

    def _list_datasets(self, project):
        """Return list of datasets for specified project"""
        return list(s3.list_nodes(self.bucket, self.root, project))

    def _list_versions(self, project, dataset):
        """Return list of versions for specified dataset"""
        return sorted(s3.list_nodes(self.bucket, self.root, project, dataset), key=_version_parser)

    def _list_contents(self, project, dataset, version):
        """Return list of versions for specified dataset"""
        return list(s3.list_objects(self.bucket, self.root, project, dataset, version))
