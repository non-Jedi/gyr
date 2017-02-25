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

import requests
import json
from time import sleep
from . import errors


class MatrixHttpApi:
    """Contains raw Matrix http api calls."""

    def __init__(self, base_url, token=None):
        """Setup the http api."""

        self.base_url = base_url
        self.token = token
        self.client_api_path = "/_matrix/client/r0"

        self.session = requests.Session()
        self.session.mount(self.base_url, requests.adapters.HTTPAdapter())

    def _request(self, request_type, api_path, content=None, header=None, params=None):
        """Sends HTTP request."""
        if request_type not in ("GET", "PUT", "POST"):
            raise requests.exceptions.HTTPError("Invalid http method: {0}".format(request_type))
        full_path = self.base_url + api_path

        if header is None:
            header = dict()
        if "Content-Type" not in header:
            header["Content-Type"] = "application/json"
        if header["Content-Type"] == "application/json":
            content = json.dumps(content)

        if params is None:
            params = dict()
        if "access_token" not in params:
            params["access_token"] = self.token

        while True:
            http_response = self.session.request(
                request_type, full_path, headers=header,
                params=params, data=content, verify=False)

            if http_response.status_code == 429:
                sleep(http_response.json()["retry_after_ms"] / 1000)
            else:
                break

        return http_response

    def as_register(self, username, as_token=None):
        """Calls the register endpoint as an application server."""
        if not as_token:
            as_token = self.token
        content = {"type": "m.login.application_service",
                   "username": username}
        return self._request("POST", self.client_api_path + "/register", content=content,
                             params={"access_token": as_token})

    def send_event(self, room_id, event_type, txn_id=None,
                   content=None, params=None):
        """Sends a state event to the homeserver."""
        if not content:
            content = dict()

        if txn_id:
            api_path = "".join((self.client_api_path, "/",
                                "/".join((room_id, "send", event_type, txn_id))))
        else:
            api_path = "".join((self.client_api_path, "/",
                                "/".join((room_id, "state", event_type))))

        response = self._request("PUT", api_path, content,
                                 params=params)
        if not response.status_code == 200:
            raise errors.HomeServerResponseError(
                "Homeserver did not return 200.")
        return response
