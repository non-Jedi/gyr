# Copyright 2016 Adam Beckmeyer
# 
# This file is part of Matrix Relay.
# 
# Matrix Relay is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Matrix Relay is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Matrix Relay.  If not, see
# <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get long description from README
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description= f.read()

setup(
    name = 'matrix relay',
    version = '0.0.0.dev0',
    url = 'https://github.com/non-Jedi/matrix_relay',
    author = 'Adam Beckmeyer',
    license = 'GPLv3',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',],
    packages = ['matrix_relay'],
    package_dir = {'matrix_relay': 'matrix_relay'},
    install_requires= [
                      ],
    entry_points= {
        'console_scripts': [
          'matrix_relay = matrix_relay.relay_cli:main'
        ]
    },
    )
