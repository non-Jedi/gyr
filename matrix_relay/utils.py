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

import string
import uuid


def create_relayer(user_id):
    """Registers user_id if necessary and returns mxid localpart."""
    if user_id[0] == "@":
        return user_id[1:].split(sep=":")[0]
    else:
        return user_id.split(sep=":")[0]


def get_rooms():
    """Returns a dict mapping rooms and users to other rooms."""
    return {"!TmaZBKYIFrIPVGoUYp:localhost":
            {"users": ["@bob:localhost"],
             "to": ["!UmaZBKYIFrIPVGoUYp:localhost"]}}


def new_txn_id():
    """Returns a unique txn id."""
    return str(uuid.uuid1())


def mxid2relayuser(mxid):
    """Returns a localpart str based on a mxid."""
    munge_rules = dict(zip(string.ascii_uppercase, [''.join(("_", i)) for i in string.ascii_lowercase]))
    munge_rules.update({"@": "=40", ":": "=3a"})
    return "".join(("relay__", mxid.translate(str.maketrans(munge_rules))))


def new_txn(txn_id):
    """Checks whether txn has occurred yet and logs it if it hasn't."""
    return True


def relay_message(content, sender, rooms, api):
    """Sends m.room.message to homeserver.."""
    relayer = create_relayer(sender)
    print("Relaying message \"{0}\" from sender \"{1}\" to rooms \"{2}\"".format(content, sender, rooms))
    for room in rooms:
        # This is all well and good, but how do I choose the sender?
        # Usually the HS would identify sender by token.
        api.send_event(room, "m.room.message", new_txn_id(),
                       content=content,
                       params={"user_id": relayer})
