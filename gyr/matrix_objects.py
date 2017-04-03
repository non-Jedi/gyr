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

from .api import MatrixASHttpAPI


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
            self._user = MatrixUser(self.json["user_id"], self.api_factory)
            return self._user

    @property
    def room(self):
        """Creates a Room object when requested."""
        try:
            return self._room
        except AttributeError:
            self._room = MatrixRoom(self.json["room_id"], self.api_factory)
            return self._room


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
        """
        self._json = json
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
            return Event(self._json[self._index], self.api_factory)


class MatrixRoom:
    """Represents matrix room."""
    pass


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, api_factory):
        self.mxid = mxid
        if api:
            self.api = api
        else:
            self.api = MatrixASHttpAPI()

    def send_message(self, content, rooms):
        """Sends m.room.message using self.api."""
        for room in rooms:
            pass

    def fetch_disp_name(self):
        """Uses self.api to fetch display name and set as self.disp_name."""
        pass

    def set_disp_name(self, new_name):
        """Uses self.api to set display name."""
        self.display_name = new_name

    def join_room(self, room):
        """Uses self.api to join a matrix room."""
        pass

    def leave_room(self, room):
        """Uses self.api to leave a matrix room."""
        pass

    def invite(self, mxid, room):
        """Uses self.api to invite mxid to room."""
        pass

    def redact(self, event_id):
        """Uses self.api to redact a matrix event."""
        pass
