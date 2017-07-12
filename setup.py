# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='shovel',
    version='0.1.0',
    description='Moving data to and from the Data Science Bottomless Pit',
    author='Lyst Data Science',
    author_email='devs@lyst.com',
    packages=['shovel'],
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['shovel=shovel.cli:main']},
    zip_safe=False,
    install_requires=[
        'boto3'
    ],
)
