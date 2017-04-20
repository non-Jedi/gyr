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

from gyr.server import Application
from gyr.matrix_objects import MatrixUser


application = Application("http://localhost:8008", "foobar")

example_mxid = "@_example_user:local"
example_user = MatrixUser(example_mxid, application.create_api)


def room_handler(room_alias):
    return False


def user_handler(user_id):
    return user_id == example_mxid


def transaction_handler(event_stream):
    for event in event_stream:

        if (event.type == "m.room.member" and
                event.json["content"] == {"membership": "invite"} and
                event.json["state_key"] == example_mxid):
            example_user.join(event.json["room_id"])

        elif (event.type == "m.room.message" and
              event.json["content"]["msgtype"] == "m.text"):
            user_room = example_user.rooms[event.json["room_id"]]
            user_room.send_notice(event.json["content"]["body"])

    return True


application.add_handlers(room_handler=room_handler,
                         transaction_handler=transaction_handler,
                         user_handler=user_handler)
