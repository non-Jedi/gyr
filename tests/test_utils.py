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

from .context import matrix_relay, CallCounter
from matrix_relay import utils
from matrix_relay import api as api_module
from matrix_relay import iofs
from matrix_relay.server import config
import uuid

api = api_module.MatrixHttpApi("https://localhost:8448")


def test_create_new_relayer(monkeypatch):
    monkeypatch.setattr(api, "as_register", lambda s: None)
    monkeypatch.setattr(iofs, "save_data", lambda p, d: None)
    monkeypatch.setattr(iofs, "retrieve_all_data", lambda p, t: [])

    lp = utils.create_relayer("@test:example.com", ".", api)
    assert lp == "relay_=40test=3aexample.com"


def test_create_old_relayer(monkeypatch):
    monkeypatch.setattr(iofs, "retrieve_all_data",
                        lambda p, t: {"@test:example.com": {}})

    lp = utils.create_relayer("@test:example.com", "/crazy/path", api)
    assert lp == "relay_=40test=3aexample.com"


def test_get_rooms(monkeypatch):
    def gad(p, t):
        if t == "!":
            return {"$14328055551tzaee:example.com": {1: 2}}
        elif t == "#":
            return {"#test:example.com": {3: 4}}
    monkeypatch.setattr(iofs, "retrieve_all_data", gad)

    rooms = utils.get_rooms("/example/path")
    assert len(rooms.keys()) == 2
    assert rooms["$14328055551tzaee:example.com"] == {1: 2}
    assert rooms["#test:example.com"] == {3: 4}


def test_get_users(monkeypatch):
    def gad(p, t):
        return {"@A:example.com": 1, "@B:exampleish.com": 2}
    monkeypatch.setattr(iofs, "retrieve_all_data", gad)

    users = utils.get_users("/example/path")
    assert len(users.keys()) == 2
    assert users["@A:example.com"] == 1
    assert users["@B:exampleish.com"] == 2


def test_new_txn_id():
    txn_id1 = utils.new_txn_id()
    txn_id2 = utils.new_txn_id()
    assert type(txn_id1) == type(txn_id2) == type(str())
    assert txn_id1 != txn_id2


def test_new_new_txn(monkeypatch):
    count_rad = CallCounter(return_value=[])
    monkeypatch.setattr(iofs, "retrieve_all_data", count_rad.inc)
    count_sd = CallCounter()
    monkeypatch.setattr(iofs, "save_data", count_sd.inc)
    count_rp = CallCounter()
    monkeypatch.setattr(iofs, "resolve_path", count_rp.inc)
    w = utils.new_txn("random_string", "/path/to/nowhere")
    assert count_rad.count == 1
    assert count_sd.count == 1
    assert w


def test_old_new_txn(monkeypatch):
    monkeypatch.setattr(iofs, "retrieve_all_data",
                        lambda p, t: {"txn_id_string": {}})
    # shouldn't need to save data if an old txn_id
    monkeypatch.delattr(iofs, "save_data")
    # using uuid to assure that this isn't a real path.
    w = utils.new_txn("txn_id_string", "/path/to/nowhere" + str(uuid.uuid4()) + "/nowhere")
    assert not w


def test_relay_message(monkeypatch):
    mcontent = {"msgtype": "m.text", "body": "hello"}
    msender = "@test:example.com"
    mrooms = ["#room1:example.com", "#room2:matrix.org"]
    mpath = "/path/to/nowhere" + str(uuid.uuid4()) + "/here"
    localpart = "realy_=40test=3aexample.com"

    count_cr = CallCounter(return_value=localpart)
    monkeypatch.setattr(utils, "create_relayer", count_cr.inc)
    count_se = CallCounter()
    monkeypatch.setattr(api, "send_event", count_se.inc)
    monkeypatch.setattr(utils, "new_txn_id", lambda: 5)

    utils.relay_message(mcontent, msender, mrooms, api, mpath)
    assert count_cr.count == 1
    assert count_se.count == 2
    assert count_se.args[1] == (mrooms[0], "m.room.message", 5)
    assert count_se.args[2] == (mrooms[1], "m.room.message", 5)
    assert count_se.kwargs[1] == count_se.kwargs[2]
    assert count_se.kwargs[1] == {"content": mcontent,
                                  "params": {"user_id": localpart}}


def test_send_bot_msg(monkeypatch):
    tmsg = "This is my test message!"
    troom = "#room:example.com"
    tsender = config["sender_localpart"]

    count_se = CallCounter()
    monkeypatch.setattr(api, "send_event", count_se.inc)
    monkeypatch.setattr(utils, "new_txn_id", lambda: 6)

    utils.send_bot_msg(tmsg, troom)

    assert count_se.count == 1
    assert count_se.args[1] == (troom, "m.room.message", 6)
    assert count_se.kwargs[1] == {"content": {"msgtype": "m.notice", "body": tmsg},
                                  "params": {"user_id": tsender}}
