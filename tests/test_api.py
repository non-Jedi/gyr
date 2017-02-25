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

from .context import matrix_relay
import matrix_relay.api
import responses
import json


api = matrix_relay.api.MatrixHttpApi("https://localhost:8448",
                                     token="example_token")


@responses.activate
def test_as_register():
    endpoint = "https://localhost:8448/_matrix/client/r0/register"
    responses.add(responses.POST,
                  endpoint, body="{}", status=200,
                  content_type="application_json")
    resp1 = api.as_register("username")
    resp2 = api.as_register("username", "sample_token")
    assert resp1.json() == {}
    assert resp2.json() == {}
    assert len(responses.calls) == 2
    assert responses.calls[0].request.url == endpoint + "?access_token=example_token"
    assert responses.calls[1].request.url == endpoint + "?access_token=sample_token"
    assert json.loads(responses.calls[0].request.body)["username"] == "username"
    assert json.loads(responses.calls[1].request.body)["type"] == "m.login.application_service"
