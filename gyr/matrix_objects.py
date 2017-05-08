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
        event = Event(json, Api)
    """

    def __init__(self, json, Api):
        """Instantiates Event instance.

        Args:
            json(dict): Event json from homeserver.
            Api(func): Creates api for calling homeserver.
        """
        self.json = json
        self.Api = Api

        self.type = json["type"]
        self.content = json["content"]
        self.timestamp = json["origin_server_ts"]
        self.id = json["room_id"]

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
            self._user = MatrixUser(mxid, self.Api(identity=mxid))
            return self._user

    @property
    def room(self):
        """Creates a Room object when requested."""
        try:
            return self._room
        except AttributeError:
            room_id = self.json["room_id"]
            self._room = MatrixRoom(room_id, self.Api)
            return self._room


class EventStream:
    """Iterable representing a stream of events sent by the HS.

    Usage:
        events = EventStream(event_list, api)
        [print(i.user) for i in events]
        """

    def __init__(self, json, Api):
        """Instantiates EventStream instance.

        Args:
            json(list): List from deserializing txn from homeserver.
            Api(func): Generates http api when passed identity=mxid.
        """
        self.json = json
        self._index = 0
        self.Api = Api

    def __iter__(self):
        return self

    def __next__(self):
        if self._index == len(self.json):
            self._index = 0
            raise StopIteration
        else:
            self._index += 1
            return Event(self.json[self._index - 1], self.Api)


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

    def _handle_request_exception(self, e):
        if e.original_exception.code == 403:
            # This sequence seeks to establish all necessary permissions
            self.api.register()
            self.api.join_room(self.room_id)
        else:
            raise e

    @utils.intent
    def send_text(self, text):
        self.api.send_message(self.room_id, text)

    @utils.intent
    def send_html(self, html, body=None):
        raise NotImplementedError("Use MatrixRoom.api for now.")

    @utils.intent
    def send_emote(self, text):
        self.api.send_emote(self.room_id, text)

    @utils.intent
    def send_notice(self, text):
        self.api.send_notice(self.room_id, text)

    @utils.intent
    def send_file(self, url, file_object, **extra_information):
        raise NotImplementedError("Methods need to be implemented in api.")

    @utils.intent
    def send_location(self, body, geo_uri, thumbnail_url=None,
                      thumbnail_info={}):
        self.api.send_location(self.room_id, geo_uri, body)

    @utils.intent
    def invite(self, user_id):
        self.api.invite_user(self.room_id, user_id)

    @utils.intent
    def kick(self, user_id, reason=""):
        self.api.kick_user(self.room_id, user_id, reason=reason)

    @utils.intent
    def ban(self, user_id, reason=""):
        self.api.ban_user(self.room_id, user_id, reason=reason)

    @utils.intent
    def unban(self, user_id):
        self.api.unban_user(self.room_id, user_id)

    @utils.intent  # Seems silly to make sure room joined just to leave...
    def leave(self):
        self.api.leave_room(self.room_id)

    @property
    def name(self):
        return self.api.get_room_name(self.room_id)["name"]

    @name.setter
    def name(self, new_name):
        self.api.set_room_name(self.room_id, new_name)

    @property
    def topic(self):
        return self.api.get_room_topic(self.room_id)["topic"]

    @topic.setter
    def topic(self, new_topic):
        self.api.set_room_topic(self.room_id, new_topic)

    @property
    def aliases(self):
        raise NotImplementedError(
            "Getting state event m.room.aliases not yet implemented upstream"
        )

    @utils.intent
    def add_alias(self, new_alias):
        self.api.set_room_alias(self.room_id, new_alias)

    def rm_alias(self, alias):
        self.api.remove_room_alias(alias)

    @property
    def members(self):
        return self.api.get_room_members(self.room_id)


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, Api):
        """Instantiates MatrixUser object.

        Args:
            mxid(str): User id (e.g. @me:example.createRoom)
            Api(func): Generates api for calls to the server.
        """
        self.mxid = mxid
        self.user_api = Api(identity=mxid)
        self.api = Api()
        self._rooms = {}

    def _handle_request_exception(self, e):
        # Basically just make sure that the ghost user has been registered
        if e.original_exception.code == 403:
            self.register()
        else:
            raise e

    def register(self):
        """Registers self.mxid with homeserver."""
        # Shouldn't send user_id param with registration
        return self.api.register(utils.mxid2localpart(self.mxid))

    @utils.intent
    def create_room(self, alias=None, is_public=False, invitees=()):
        """Calls /createRoom as self.mxid."""
        response = self.user_api.create_room(alias=alias, is_public=is_public,
                                             invitees=invitees)
        return self._mkroom(response["room_id"])

    @utils.intent
    def join(self, room_str):
        """Joins room id or alias even if it must first be created."""
        response = self.user_api.join_room(room_str)
        return self._mkroom(response["room_id"])

    def _mkroom(self, room_id):
        self._rooms[room_id] = MatrixRoom(room_id, self.user_api)
        return self._rooms[room_id]

    @property
    def displayname(self):
        """Queries the server to return current displayname."""
        return self.api.get_display_name(self.mxid)

    @displayname.setter
    @utils.intent
    def displayname(self, new_displayname):
        """PUTs new displayname to server."""
        self.user_api.set_display_name(self.mxid, new_displayname)

    @property
    @utils.intent
    def avatar_url(self):
        """Gets current avatar url from server."""
        return self.api.get_avatar_url(self.mxid)

    @avatar_url.setter
    @utils.intent
    def avatar_url(self, new_url):
        """PUTs new avatar url to server."""
        self.user_api.set_avatar_url(self.mxid, new_url)

    @property
    def rooms(self):
        """Refreshes room list if empty and returns it."""
        if not self._rooms:
            self.refresh_rooms()
        return self._rooms

    @utils.intent
    def refresh_rooms(self):
        """Calls GET /joined_rooms to refresh rooms list."""
        for room_id in self.user_api.get_joined_rooms()["joined_rooms"]:
            self._rooms[room_id] = MatrixRoom(room_id, self.user_api)
