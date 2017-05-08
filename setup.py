# Copyright 2016 Adam Beckmeyer
#
# This file is part of Gyr.
#
# Gyr is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gyr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with Gyr.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import os.path

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gyr',
    author='Adam Beckmeyer',
    author_email='adam_git@thebeckmeyers.xyz',
    description='A python framework for building matrix application services',
    long_description=long_description,
    version='0.2.0',
    url='https://github.com/non-Jedi/gyr',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Communications :: Chat',
        'Programming Language :: Python :: 3',
    ],
    keywords='matrix chat falcon WSGI application-service',
    packages=find_packages(),
    package_data={'': ['LICENSE', 'README.md']},
    install_requires=[
        'falcon',
        'requests',
        'matrix-client>=0.0.6'
    ],
)
