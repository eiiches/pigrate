# coding: utf-8

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension

setup(name='pigrate',
      version='develop',
      description='Database schema migration tool written in Python',
      author='Eiichi Sato',
      author_email='sato.eiichi@gmail.com',
      url='https://github.com/eiiches/pigrate',
      download_url='https://github.com/eiiches/pigrate/archive/develop.tar.gz',
      keywords=['database', 'schema', 'migration'],
      requires=[],
      packages=['pigrate'],
      scripts=['bin/pigrate'])
