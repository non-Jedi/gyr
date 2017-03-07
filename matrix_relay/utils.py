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

from string import ascii_lowercase, ascii_uppercase
import uuid
from . import iofs


def create_relayer(user_id, base_path, api):
    """Registers user_id if necessary and returns mxid localpart."""
    localpart = mxid2relayuser(user_id)
    # Can abstract over this to save filesystem access by caching
    if user_id not in get_users(base_path):
        api.as_register(localpart)
        # No info about user to save in current design
        iofs.save_data(iofs.resolve_path(user_id, base_path), {})
    return localpart


def get_rooms(base_path):
    """Returns a dict mapping rooms and users to other rooms."""
    rooms = iofs.retrieve_all_data(base_path, "!")
    rooms.update(iofs.retrieve_all_data(base_path, "#"))
    return rooms


def get_users(base_path):
    """Returns a dict of all users the AS is aware of."""
    return iofs.retrieve_all_data(base_path, "@")


def new_txn_id():
    """Returns a unique txn id."""
    return str(uuid.uuid1())


def mxid2relayuser(mxid):
    """Returns a localpart str based on a mxid."""
    # mxid localparts must not contain capital letters.
    sub_lower = ["".join(("_", i)) for i in ascii_lowercase]
    munge_rules = dict(zip(ascii_uppercase, sub_lower))
    # mxid localparts cannot contain @ or :
    munge_rules.update({"@": "=40", ":": "=3a"})
    return "".join(("relay_", mxid.translate(str.maketrans(munge_rules))))


def new_txn(txn_id, base_path):
    """Returns True if txn hasn't occurred before."""
    # Use "t" as txn_id prefix
    if txn_id in iofs.retrieve_all_data(base_path, "t"):
        return False
    else:
        iofs.save_data(iofs.resolve_path(txn_id, base_path, "t"), {})
        return True


def relay_message(content, sender, rooms, api, storage_path):
    """Sends m.room.message to homeserver.."""
    relayer = create_relayer(sender, storage_path, api)
    print("Relaying message \"{0}\" from sender \"{1}\" to rooms \"{2}\"".format(content, sender, rooms))
    for room in rooms:
        # This is all well and good, but how do I choose the sender?
        # Usually the HS would identify sender by token.
        api.send_event(room, "m.room.message", new_txn_id(),
                       content=content,
                       params={"user_id": relayer})
