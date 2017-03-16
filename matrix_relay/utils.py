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
from . import iofs, errors


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


def new_relay_room(data, storage_path):
    """Creates a room and its mappings in the database."""
    src_rm = data.keys()[0]
    save_path = iofs.resolve_path(src_rm, base_path=storage_path)
    iofs.save_data(save_path, data[src_rm])


def new_txn(txn_id, base_path):
    """Returns True if txn hasn't occurred before."""
    # Use "t" as txn_id prefix
    if txn_id in iofs.retrieve_all_data(base_path, "t"):
        return False
    else:
        iofs.save_data(iofs.resolve_path(txn_id, base_path, "t"), {})
        return True


def proc_command(sender, command, storage_path):
    """Checks sender permissions and executes command."""
    # For now we'll assume that all senders have permissions
    com_tok = command.split(" ")
    action = com_tok[1]

    if action == "dump":
        command_data = {com_tok[2]: com_tok[3:]}
        if com_tok[2] not in get_rooms(storage_path):
            new_relay_room(command_data, storage_path)
        else:
            room_path = iofs.resolve_path(com_tok[2], storage_path)
            cur_room_data = iofs.retrieve_data(room_path)
            new_room_data = list(set(cur_room_data + command_data))
            iofs.save_data(room_path, new_room_data)
    else:
        raise errors.RelayNotImplemented(
            "The command you entered hasn't yet been implemented.")


def relay_message(content, sender, rooms, api, storage_path):
    """Sends m.room.message to homeserver.."""
    relayer = create_relayer(sender, storage_path, api)
    for room in rooms:
        api.send_event(room, "m.room.message", new_txn_id(),
                       content=content,
                       params={"user_id": relayer})
