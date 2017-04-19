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
from matrix_client.api import MatrixHttpApi, MATRIX_V2_API_PATH


class MatrixASHttpAPI(MatrixHttpApi):
    """Wraps MatrixHttpApi to allow AS identity assertion.

    Usage:
        matrix = MatrixASHttpAPI("https://matrix.org",
                                 identity="@matrix:matrix.org",
                                 token="foobar")
        response = matrix.sync()
        response = matrix.send_message("!roomid:matrix.org",
                                       "Hello!")
    """

    def __init__(self, *args, identity=None, **kwargs):
        super(MatrixASHttpAPI, self).__init__(*args, **kwargs)
        self.identity = identity

    def _send(self, *args, **kwargs):
        if "query_params" not in kwargs:
            kwargs["query_params"] = {}
        if self.identity:
            kwargs["query_params"]["user_id"] = self.identity

        return super(MatrixASHttpAPI, self)._send(*args, **kwargs)

    def register(self, username):
        """Performs /register with type: m.login.application_service

        Args:
            username(str): Username to register.
        """
        content = {
            "type": "m.login.application_service",
            "username": username,
        }
        return self._send("POST", "/register", content,
                          api_path=MATRIX_V2_API_PATH)

    def get_joined_rooms(self):
        """Performs GET /joined_rooms."""
        return self._send("GET", "/joined_rooms")
