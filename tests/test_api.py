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

import time
from .context import matrix_relay
import matrix_relay.api
import responses
import json
from urllib.parse import quote, urlparse, parse_qs


api = matrix_relay.api.MatrixHttpApi("https://localhost:8448",
                                     token="example_token")
base_url = "https://localhost:8448/_matrix/client/r0/"


@responses.activate
def test_as_register():
    endpoint = base_url + "register"
    responses.add(responses.POST, endpoint, body="{}", status=200,
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


@responses.activate
def test_send_event():
    room_id = "!636q39766251@example.com"
    params = {"user_id": ["@test:example.com"],
              "access_token": ["test_token"]}
    # tests endpoint without transaction id as 0
    event_type_0 = "m.room.name"
    endpoint_0 = base_url + quote("rooms/" + room_id + "/state/" + event_type_0)
    content_0 = {"name": "test_name"}
    responses.add(responses.PUT, endpoint_0, body="{}", status=200,
                  content_type="application_json")
    resp0 = api.send_event(room_id, event_type_0, content=content_0,
                           params=params)
    assert resp0.json() == {}
    assert len(responses.calls) == 1
    # parse the url to get the params as a dict
    req0_qs = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert req0_qs == params
    # body should be the same as content we called send_event with
    assert json.loads(responses.calls[0].request.body) == content_0

    event_type_1 = "m.room.message"
    txn_id_1 = str(123456)
    endpoint_1 = base_url + quote("rooms/" + room_id + "/send/" + event_type_1 + "/" + txn_id_1)
    content_1 = {"msgtype": "m.text", "body": "Hello!"}
    responses.add(responses.PUT, endpoint_1, body="{}", status=200,
                  content_type="application_json")
    resp1 = api.send_event(room_id, event_type_1, content=content_1,
                           params=params, txn_id=txn_id_1)
    assert resp1.json() == {}
    assert len(responses.calls) == 2
    req1_qs = parse_qs(urlparse(responses.calls[1].request.url).query)
    assert req1_qs == params
    assert json.loads(responses.calls[1].request.body) == content_1


@responses.activate
def test_429_behavior(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda s: None)
    event_type = "m.room.name"
    room_id = "!636q39766251@example.com"
    params = {"user_id": ["@test:example.com"],
              "access_token": ["test_token"]}
    content = {"name": "test_name"}
    endpoint = base_url + quote("rooms/" + room_id + "/state/" + event_type)
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(responses.PUT, endpoint, body='{"retry_after_ms": 1000}',
                 status=429, content_type="application_json")
        rsps.add(responses.PUT, endpoint, body='{}', status=200,
                 content_type="application_json")
        resp = api.send_event(room_id, event_type, content=content,
                              params=params)
        assert resp.status_code == 200
        assert len(rsps.calls) == 2
        assert rsps.calls[0].response.status_code == 429
        assert rsps.calls[1].response.status_code == 200
        assert rsps.calls[0].request.body == rsps.calls[1].request.body
        assert rsps.calls[0].request.url == rsps.calls[1].request.url
