#!/usr/bin/python
from distutils.core import setup

setup(name="zm_database_init",
  version='2.0.0',
  description="A script for ZoneMinder database initialization and upgrade",
  author='Dirk Hartmann',
  author_email="monex@liquid-co.de",
  url="https://gitorious.org/zoneminder-rpm-database-init",
  packages=['zm_dbinit', 'distutils.command'],
)