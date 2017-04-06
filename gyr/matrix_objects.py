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
    pass


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, api=None):
        self.mxid = mxid
        self.api = api

    def register(self):
        """Registers self.mxid with homeserver."""
        return self.api.register(utils.mxid2localpart(self.mxid))

    def create_room(self, alias=None, is_public=False, invitees=()):
        """Calls /createRoom as self.mxid."""
        return self.api.create_room(alias=alias, is_public=is_public,
                                    invitees=invitees)

    def join(self, room):
        """Joins room id or alias even if it must first be created."""
        raise NotImplementedError("Bug Adam to get on this. He really shouldn't have released like this.")

    def send_location(self, *args, **kwargs):
        """Sends m.location message event."""
        return self.api.send_location(*args, **kwargs)

    def send_message(self, *args, **kwargs):
        """Sends m.room.message with default msgtype m.text."""
        return self.api.send_message(*args, **kwargs)

    def send_emote(self, *args, **kwargs):
        """Sends m.room.message with msgtype m.emote."""
        return self.api.send_emote(*args, **kwargs)

    def send_notice(self, *args, **kwargs):
        """Sends m.room.message with msgtype m.note."""
        return self.api.send_notice(*args, **kwargs)

    def set_room_name(self, *args, **kwargs):
        """Sets room name.

        Args:
            room_id(str): The room ID
            name(str): The new rom name
            timestamp(int): Optional. Set origin_server_ts
        """
        return self.api.set_room_name(*args, **kwargs)

    def set_room_topic(self, *args, **kwargs):
        """Sets room topic.

        Args:
            room_id(str): The room ID
            topic(str): The new room topic
            timestamp(int): Optional. Set origin_server_ts (For application services only)
        """
        return self.api.set_room_topic(*args, **kwargs)

    def leave_room(self, *args, **kwargs):
        """Perform POST /rooms/$room_id/leave

        Args:
            room_id(str): The room ID
        """
        return self.api.leave_room(*args, **kwargs)

    def invite_user(self, *args, **kwargs):
        """Perform POST /rooms/$room_id/invite

        Args:
            room_id(str): The room ID
            user_id(str): The user ID of the invitee
        """
        return self.api.invite_user(*args, **kwargs)

    def kick_user(self, *args, **kwargs):
        """Calls set_membership with membership="leave" for the user_id provided
        """
        return self.api.kick_user(*args, **kwargs)

    def get_membership(self, room_id):
        """Returns membership of user in room_id."""
        return self.api.get_membership(self, room_id, self.mxid)

    def set_membership(self, room_id, membership, **kwargs):
        """Sets membership of self.mxid in room_id.

        Args:
            room_id(str): The room ID
            membership(str): New membership value
            reason(str): The reason
            timestamp(int): Optional. Set origin_server_ts (For application services only)
        """
        return self.api.set_membership(room_id, self.mxid, membership, **kwargs)

    def ban_user(self, *args, **kwargs):
        """Perform POST /rooms/$room_id/ban

        Args:
            room_id(str): The room ID
            user_id(str): The user ID of the banee(sic)
            reason(str): The reason for this ban
        """
        return self.api.ban_user(*args, **kwargs)

    def unban_user(self, *args, **kwargs):
        """Perform POST /rooms/$room_id/unban

        Args:
            room_id(str): The room ID
            user_id(str): The user ID of the banee(sic)
        """
        return self.api.unban_user(*args, **kwargs)
