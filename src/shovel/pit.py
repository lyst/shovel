# -*- coding: utf-8 -*-
from shovel import exceptions, s3


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
        self.bucket = bucket
        self.root = root

    def bury(self, project, name, version, working_path):
        """Upload the contents of the target path to the pit."""
        _version_parser(version)
        if self.list_contents(project, name, version):
            raise exceptions.VersionExists

        s3.put_objects(working_path, self.bucket, self.root, project, name, version)

    def dig(self, project, name, version, working_path):
        """Download the contents of the target dataset from the pit."""
        _version_parser(version)
        if not self.list_contents(project, name, version):
            raise exceptions.VersionDoesNotExist

        s3.get_objects(working_path, self.bucket, self.root, project, name, version)

    def list_projects(self):
        """Return list of projects"""
        return list(s3.list_nodes(self.bucket, self.root))

    def list_datasets(self, project):
        """Return list of datasets for specified project"""
        return list(s3.list_nodes(self.bucket, self.root, project))

    def list_versions(self, project, dataset):
        """Return list of versions for specified dataset"""
        return sorted(s3.list_nodes(self.bucket, self.root, project, dataset), key=_version_parser)

    def list_contents(self, project, dataset, version):
        """Return list of versions for specified dataset"""
        return list(s3.list_objects(self.bucket, self.root, project, dataset, version))
