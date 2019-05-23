# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from textwrap import dedent

from shovel import shovel


class Shovel(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='High level library for storing and retrieving datasets from cloud stores',
            usage=dedent(
                """
                shovel <command> [<args>]

                There are two common commands provided by Shovel:
                    shovel bury <LOCAL_DIRECTORY> <PROJECT> <DATASET> <VERSION> [--force]
                        Upload a dataset to the default pit

                    shovel dig <LOCAL_DIRECTORY> <PROJECT> <DATASET> <VERSION>
                        Download a dataset from the default pit
                """))
        parser.add_argument('command', help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            parser.print_help()
            sys.exit(1)

        getattr(self, args.command)()

    @staticmethod
    def bury():
        parser = argparse.ArgumentParser(
            description='Upload a dataset to the default pit',
            usage="shovel bury local_directory project dataset [--force]",
        )
        parser.add_argument('local_directory')
        parser.add_argument('project')
        parser.add_argument('dataset')
        parser.add_argument('version')
        parser.add_argument('--force', dest='force', action='store_true',
                            help='upload dataset version even if it exists already')

        args = parser.parse_args(sys.argv[2:])

        version = shovel.bury(
            args.local_directory, args.project, args.dataset, args.version, args.force)

        logger = logging.getLogger(__name__)
        logger.info('Created {}/{}/{}'.format(args.project, args.dataset, version))

    @staticmethod
    def dig():
        parser = argparse.ArgumentParser(
            description='Download a dataset from the default pit',
            usage="shovel dig project dataset version",
        )
        parser.add_argument('local_directory')
        parser.add_argument('project')
        parser.add_argument('dataset')
        parser.add_argument('version')
        args = parser.parse_args(sys.argv[2:])

        shovel.dig(args.local_directory, args.project, args.dataset, args.version)


def main():
    Shovel()
