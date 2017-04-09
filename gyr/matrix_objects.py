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

from . import utils


class Event:
    """Represents a matrix event sent by the HS.

    Usage:
        event = Event(json, api_factory)
    """

    def __init__(self, json, api_factory):
        """Instantiates Event instance.

        Args:
            json(dict): Event json from homeserver.
            api_factory(func): Creates api for calling homeserver.
        """
        self.json = json
        self.api_factory = api_factory

    @property
    def user(self):
        """Creates a User object when requested."""
        try:
            return self._user
        except AttributeError:
            if "sender" in self.json:
                mxid = self.json["sender"]
            else:
                mxid = self.json["user_id"]
            self._user = MatrixUser(mxid, self.api_factory(mxid))
            return self._user

    @property
    def room(self):
        """Creates a Room object when requested."""
        try:
            return self._room
        except AttributeError:
            room_id = self.json["room_id"]
            self._room = MatrixRoom(room_id, self.api_factory())
            return self._room

    @property
    def type(self):
        """Returns the type of event."""
        return self.json["type"]

    @property
    def content(self):
        """Returns content of event."""
        return self.json["content"]

    @property
    def timestamp(self):
        """Returns the timestamp in milliseconds."""
        return self.json["origin_server_ts"]

    @property
    def id(self):
        """Returns the event id."""
        return self.json["room_id"]


class EventStream:
    """Iterable representing a stream of events sent by the HS.

    Usage:
        events = EventStream(event_list, api)
        [print(i.user) for i in events]
        """

    def __init__(self, json, api_factory):
        """Instantiates EventStream instance.

        Args:
            json(list): List from deserializing txn from homeserver.
            api_factory(func): Generates http api when passed mxid.
        """
        self.json = json
        self._index = 0
        self.api_factory = api_factory

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self._json):
            self._index = 0
            raise StopIteration
        else:
            self._index += 1
            return Event(self.json[self._index], self.api_factory)


class MatrixRoom:
    """Represents matrix room."""

    def __init__(self, room_id, api):
        """Instantiates MatrixRoom object.

        Args:
            room_id(str): Matrix room id (e.g. !1234567:example.com)
            api(MatrixASHttpAPI): Api for calls to the server.
        """
        self.room_id = room_id
        self.api = api


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, api):
        """Instantiates MatrixUser object.

        Args:
            mxid(str): User id (e.g. @me:example.createRoom)
            api(MatrixASHttpAPI): Api for calls to the server.
        """
        self.mxid = mxid
        self.api = api
        self.rooms = {}

    def register(self):
        """Registers self.mxid with homeserver."""
        # Shouldn't send user_id param with registration
        self.api.identity = None
        response = self.api.register(utils.mxid2localpart(self.mxid))
        self.api.identity = self.mxid
        return response

    def create_room(self, alias=None, is_public=False, invitees=()):
        """Calls /createRoom as self.mxid."""
        response = self.api.create_room(alias=alias, is_public=is_public,
                                        invitees=invitees)
        return self._mkroom(response["room_id"])

    def join(self, room_str):
        """Joins room id or alias even if it must first be created."""
        response = self.api.join_room(room_str)
        return self._mkroom(response["room_id"])

    def _mkroom(self, room_id):
        self.rooms[room_id] = MatrixRoom(room_id, self.api)
        return self.rooms[room_id]

    @property
    def displayname(self):
        """Queries the server to return current displayname."""
        return self.api.get_display_name(self.mxid)

    @displayname.setter
    def displayname(self, new_displayname):
        """PUTs new displayname to server."""
        self.api.set_display_name(self.mxid, new_displayname)

    @property
    def avatar_url(self):
        """Gets current avatar url from server."""
        return self.api.get_avatar_url(self.mxid)

    @avatar_url.setter
    def avatar_url(self, new_url):
        """PUTs new avatar url to server."""
        self.api.set_avatar_url(self.mxid, new_url)
