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


def mxid2relayuser(mxid):
    munge_rules = dict(zip(string.ascii_uppercase, [''.join(("_", i)) for i in string.ascii_lowercase]))
    munge_rules.update({"@": "=40", ":": "=3a"})
    return "".join(("relay__", mxid.translate(str.maketrans(munge_rules))))


def proc_event(event_dict):
    relayed_rooms = get_rooms()
    if event_dict["type"] == "m.room.message" and event_dict["room_id"] in relayed_rooms:
        if event_dict["user_id"] in relayed_rooms[event_dict["room_id"]]["relayed_users"]:
            relay_message(event_dict["content"], event_dict["sender"], relayed_rooms[event_dict["room_id"]]["to"])
    # Following is the list of event types that must be handled
    # m.room.aliases IGNORE
    # m.room.canonical_alias IGNORE
    # m.room.create IGNORE
    # m.room.join_rules IGNORE
    # m.room.member P1
    # m.room.power_levels IGNORE
    # m.room.redaction P2
    # INSTANT MESSAGING
    # m.room.message P1
    # m.room.name P3
    # m.room.topic P3
    # m.room.avatar P3
    # TYPING NOTIFICATION
    # m.typing P2
    # RECEIPTS
    # m.receipt P3
    # PRESENCE
    # m.presence P2


def get_rooms():
    return {"!TmaZBKYIFrIPVGoUYp:localhost":
            {"relayed_users": ["@bob:localhost"],
             "to": ["!UmaZBKYIFrIPVGoUYp:localhost"]}}


def relay_message(content, sender, rooms):
    print("Relaying message \"{0}\" from sender \"{1}\" to rooms \"{2}\"".format(content, sender, rooms))
