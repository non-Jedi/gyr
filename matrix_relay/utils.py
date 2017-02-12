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


def get_rooms():
    """Returns a dict mapping rooms and users to other rooms."""
    return {"!TmaZBKYIFrIPVGoUYp:localhost":
            {"users": ["@bob:localhost"],
             "to": ["!UmaZBKYIFrIPVGoUYp:localhost"]}}


def mxid2relayuser(mxid):
    """Returns a localpart str based on a mxid."""
    munge_rules = dict(zip(string.ascii_uppercase, [''.join(("_", i)) for i in string.ascii_lowercase]))
    munge_rules.update({"@": "=40", ":": "=3a"})
    return "".join(("relay__", mxid.translate(str.maketrans(munge_rules))))


def new_txn(txn_id):
    """Checks whether txn has occurred yet and logs it if it hasn't."""
    return True


def relay_message(content, sender, rooms):
    """Sends m.room.message to homeserver using api.py."""
    print("Relaying message \"{0}\" from sender \"{1}\" to rooms \"{2}\"".format(content, sender, rooms))
