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

from string import ascii_lowercase, digits
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


def is_full_mxid(user_string):
    """Returns True if a string is a valid mxid."""
    if not user_string[0] == "@":
        return False
    parts = user_string[1:].split(":")
    localpart_chars = ascii_lowercase + digits + "._-="
    if not (len(parts) == 2 and all([i in localpart_chars for i in parts[0]])):
        return False
    return True


def mxid2localpart(mxid):
    """Returns the localpart of a valid mxid."""
    return mxid.strip("@").split(":")[0]


def new_data(data, full_storage_path):
    """Creates a database object at storage_path."""
    iofs.save_data(full_storage_path, data)