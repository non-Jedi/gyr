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

    def __init__(self, storage_path, config, api):
        self.storage_path = storage_path
        self.config = config
        self.api = api


class Room(Resource):

    def on_get(self, request, response, name=None):
        pass


class Transaction(Resource):

    def on_put(self, request, response, txn_id=None):
        response.status = falcon.HTTP_200
        response.body = json.dumps({})
        # request.stream.read().decode("utf-8") raises an error. Go figure.
        # request.context is a dictionary that comes with the request for some reason
        request.context["body"] = request.stream.read()
        try:
            # body should contain json object where key "events"
            # returns a list of events
            request.context["events"] = json.loads(request.context["body"].decode("utf-8"))["events"]
        except(KeyError, ValueError, UnicodeDecodeError):
            response.status = falcon.HTTP_400
            response.body = "Malformed request body"
            request.context["events"] = []
        for event in request.context["events"]:
            # proc_event may end up as a method of Transaction
            utils.proc_event(event)


class User(Resource):

    def on_get(self, request, response, user_id=None):
        if user_id == self.config['relay_uid']:
            response.status = falcon.HTTP_200
            response.body = json.dumps({})
            self.api.as_register(user_id, self.config['as_token'])
        else:
            response.status = falcon.HTTP_404
            response.body = json.dumps({})
