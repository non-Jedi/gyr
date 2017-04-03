# Copyright 2016 Adam Beckmeyer
#
# This file is part of Gyr.
#
# Gyr is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Gyr is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gyr.  If not, see <http://www.gnu.org/licenses/>.

import falcon
import json
from . import utils
from .matrix_objects import EventStream


class Resource:
    """Master class for falcon http resources."""

    def __init__(self, handler, api_factory):
        self.handler = handler
        self.api_factory = api_factory
        # Api used directly by Room and User resources
        self.api = api_factory()
        # Place to track occurences of e.g. a certain txn_id
        self.tracker = [None] * 20

    def _is_new(self, identifier):
        """Returns True if identifier hasn't been seen before."""
        if identifier in self.tracker:
            return False
        else:
            self.tracker.append(identifier)
            self.tracker.pop(0)
            return True


class Room(Resource):
    """Generates objects to respond to GET /rooms/{room_alias}."""

    def on_get(self, request, response, room_alias=None):
        """Called when a GET request is sent to /rooms/{room_alias}"""
        response.body = "{}"
        if self.handler(room_alias):
            response.status = falcon.HTTP_200
            self.api.create_room(alias=room_alias)
        else:
            response.status = falcon.HTTP_404


class Transaction(Resource):
    """Generates objects to respond to PUT /transactions/{txn_id}"""

    def on_put(self, request, response, txn_id=None):
        """Responds to PUT request containing events."""
        response.body = "{}"

        # Check whether repeat txn_id
        if not self._is_new(txn_id):
            response.status = falcon.HTTP_200
            return

        request.context["body"] = request.stream.read()
        try:
            events = json.loads(request.context["body"].decode("utf-8"))["events"]
        except(KeyError, ValueError, UnicodeDecodeError):
            response.status = falcon.HTTP_400
            response.body = "Malformed request body"
            return

        if self.handler(EventStream(events, self.api_factory)):
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_400


class User(Resource):
    """Generates objects to respond to GET /users/{user_id}"""

    def on_get(self, request, response, user_id=None):
        """Responds to GET request for users."""
        response.body = "{}"
        if self.handler(user_id):
            response.status = falcon.HTTP_200
            self.api.register(utils.mxid2localpart(user_id))
        else:
            response.status = falcon.HTTP_404
