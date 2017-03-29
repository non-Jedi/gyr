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


class Resource:
    """Master class for falcon http resources."""

    def __init__(self, handler, hs_api):
        self.handler = handler
        self.hs_api = hs_api
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

    def on_get(self, request, response, name=None):
        """Called when a GET request is sent to /rooms/{room_alias}"""
        response.body = "{}"
        # todo: pass details of request body to self.handler
        # todo: register new room if self.handler returns True


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
        # todo: pass details of request body to self.handler


class User(Resource):
    """Generates objects to respond to GET /users/{user_id}"""

    def on_get(self, request, response, user_id=None):
        """Responds to GET request for users."""
        response.body = "{}"
        # todo: pass details of request body to self.handler
        # todo: register new user if self.handler returns True
