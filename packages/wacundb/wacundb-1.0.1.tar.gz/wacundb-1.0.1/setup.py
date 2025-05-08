#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from wacundb import __version__

setup(
  name='wacundb',
  version=__version__,
  author='Huaqing Ye',
  author_email='wacunye@gmail.com',
  url='http://www.leafpy.org/',
  py_modules=['wacundb'],
  description='wacunDB library',
  long_description="wacunDB is a simple library for makeing raw SQL queries to most relational databases.",
  install_requires = ['sqlalchemy\n', 'pymssql\n','pymysql\n'],
  license="MIT license",
  platforms=["any"],
)
