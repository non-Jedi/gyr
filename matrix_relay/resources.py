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

import json
import falcon
from . import utils


class Resource:
    """Master class for falcon http resources."""

    def __init__(self, storage_path, config, api):
        self.storage_path = storage_path
        self.config = config
        self.api = api


class Room(Resource):
    """Generates objects to respond to GET /rooms/{room_alias}."""

    def on_get(self, request, response, name=None):
        """Called when a GET request is sent to /rooms/{room_alias}"""
        pass


class Transaction(Resource):
    """Generates objects to respond to PUT /transactions/{txn_id}"""

    def on_put(self, request, response, txn_id=None):
        """Responds to PUT request containing events."""
        # Unless there's a problem with the request, return 200
        response.status = falcon.HTTP_200
        response.body = "{}"
        # For duplicate txns, method should not complete
        if not utils.new_txn(txn_id):
            return
        # request.context is a dictionary for some reason
        request.context["body"] = request.stream.read()
        try:
            # Request body contains json object with key "events"
            request.context["events"] = json.loads(request.context["body"].decode("utf-8"))["events"]
        except(KeyError, ValueError, UnicodeDecodeError):
            response.status = falcon.HTTP_400
            response.body = "Malformed request body"
            request.context["events"] = list()
        for event in request.context["events"]:
            # Method rather than function for access to AS token
            self.proc_event(event)

    def proc_event(self, event):
        """Relays events based on event type and room."""
        # Retrieve the latest canonical rooms to be relayed
        relayed = utils.get_rooms()
        if event["room_id"] in relayed:
            # for code brevity:
            room = event["room_id"]
            if event["type"] == "m.room.message":
                if event["user_id"] in relayed[room]["users"]:
                    utils.relay_message(event["content"],
                                        event["user_id"],
                                        relayed[room]["to"],
                                        self.api)
        else:
            # Check for commands to relay bridge here?
            pass
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


class User(Resource):
    """Generates objects to respond to GET /users/{user_id}"""

    def on_get(self, request, response, user_id=None):
        """Responds to GET request for users."""
        if user_id == self.config['relay_uid']:
            response.status = falcon.HTTP_200
            response.body = json.dumps({})
            self.api.as_register(user_id, self.config['as_token'])
        else:
            response.status = falcon.HTTP_404
            response.body = json.dumps({})
