# -*- coding: utf-8 -*-


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
