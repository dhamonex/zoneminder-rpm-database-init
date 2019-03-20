#!/usr/bin/python
from distutils.core import setup

setup(name="zm_database_init",
  version='3.3.1',
  description="A script for ZoneMinder database initialization and upgrade",
  author='Dirk Hartmann',
  author_email="monex@liquid-co.de",
  url="https://github.com/dhamonex/zoneminder-rpm-database-init",
  packages=["zm_dbinit"],
  package_dir={"zm_dbinit": "src/zm_dbinit"},
  scripts=["src/scripts/zm_database_init"],
  data_files=[("/etc", ["config/zm_database_init.conf"])],
  classifiers=["Development Status :: 4 - Beta", 
    "Environment :: Console",
    "License :: GPLv2",
    "Programming Language :: Python"]
)
