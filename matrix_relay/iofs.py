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
"""This module should be so dead simple it doesn't need unit tests.

Here's where all the code for doing io to the filesystem resides kids.
"""

import json
import os


def retrieve_data(path):
    """Retrieves data from a specified path and deserializes it."""
    with open(path, 'r', encoding="utf8") as f:
        return json.load(f)


def resolve_path(attribute, base_path=os.getcwd(), attr_type=None):
    """Returns the filesystem path to the specified attribute."""
    if attr_type is None:
        attr_type = attribute[0]
    return os.path.join(base_path, attr_type, attribute)


def save_data(path, contents):
    """Serializes data and saves to specified path."""
    _mk_path(os.sep.join(os.path.split(path)[:-1]))
    with open(path, 'w', encoding="utf8") as f:
        json.dump(contents, f)


def retrieve_all_data(base_path, attribute_type):
    """Returns all attributes of a certain type (e.g. "@") as dict)."""
    wd = os.sep.join((base_path, attribute_type))
    data = dict()
    for f in os.listdir(wd):
        data[f] = retrieve_data(os.sep.join((wd, f)))
    return data


def _mk_path(path):
    """Creates directories recursively."""
    if not os.path.exists(path):
        _mk_path(os.sep.join(os.path.split(path)[:-1]))
        os.mkdir(path)
