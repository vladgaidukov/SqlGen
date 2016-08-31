#!/usr/bin/env python
from os.path import join, dirname
from distutils.core import Extension
from setuptools import setup
 
setup(name='SqlGen',
 version='0.1',
 description='MySql no script connector',
 author='Vlad Gaidukov',
 author_email='master@meliar.ru',
 install_requires=['mysql-connector'],
 py_modules = ['sqlgen'],
 long_description=open(join(dirname(__file__), 'README.md')).read(),
)