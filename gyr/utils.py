# Copyright 2016 Adam Beckmeyer
#
# This file is part of Gyr.
#
# Gyr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Gyr is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gyr.  If not, see
# <http://www.gnu.org/licenses/>.

import uuid
from . import iofs


def get_rooms(base_path):
    """Returns a dict of data stored about all rooms the AS is aware of."""
    rooms = iofs.retrieve_all_data(base_path, "!")
    rooms.update(iofs.retrieve_all_data(base_path, "#"))
    return rooms


def get_users(base_path):
    """Returns a dict of data stored about all users the AS is aware of."""
    return iofs.retrieve_all_data(base_path, "@")


def gen_txn_id():
    """Returns a new, unique txn id."""
    return str(uuid.uuid1())


def new_data(data, full_storage_path):
    """Creates a database object at storage_path."""
    iofs.save_data(full_storage_path, data)
