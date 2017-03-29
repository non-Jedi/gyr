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
from matrix_client.api import MatrixHttpApi


class MatrixASHttpAPI(MatrixHttpApi):
    """Wraps methods of MatrixHttpApi to use AS identity assertion.

    Usage:
        matrixAS = MatrixASHttpAPI("@ex:matrix.org", "https://matrix.org", token="foobar")
        response = matrixAS.sync()
        response = matrixAS.send_message("!roomid:matrix.org", "Hello!")

        matrixAS.user_id = "@ex2:matrix.org"
        response = matrixAS.sync()
    """

    def __init__(self, user_id, *args, **kwargs):
        """Construct and configure the HTTP API.

        Args:
            user_id (str): The desired user ID to act as.
            *args: Arguments to pass to MatrixHttpApi's __init__ method.
            **kwargs: Keyword arguments to pass to MatrixHttpApi's __init__ method.
        """
        # Runs the __init__method of MatrixHttpApi
        super(MatrixASHttpAPI, self).__init__(*args, **kwargs)
        self.user_id = user_id

    def _send(self, *args, **kwargs):
        if "query_params" not in kwargs:
            kwargs["query_params"] = dict()
        kwargs["query_params"]["user_id"] = self.user_id
        super(MatrixASHttpAPI, self)._send(*args, **kwargs)

    def register(self):
        """Performs /register using AS admin permissions."""
        content = {"user": self.user_id.strip("@").split(":")[0],
                   "type": "m.login.application_service"}
        return super(MatrixASHttpAPI, self)._send("POST", "/register", content)
