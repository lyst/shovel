# -*- coding: utf-8 -*-
from textwrap import dedent


class VersionError(ValueError):
    pass


class VersionExists(ValueError):
    pass


class VersionDoesNotExist(ValueError):
    pass


class DatasetExists(ValueError):
    pass


class FileExists(ValueError):
    pass


class OutOfSync(ValueError):
    def __init__(self, local_files, remote_files):
        only_local = sorted(set(local_files) - set(remote_files))
        only_remote = sorted(set(remote_files) - set(local_files))
        local_and_remote = sorted(set(remote_files) & set(local_files))
        msg = dedent(f"""
            Local and remote not in sync.
            Only local: {only_local}
            Only remote: {only_remote}
            In both: {local_and_remote}
            """).strip()
        super().__init__(msg)
