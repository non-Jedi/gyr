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
from matrix_relay import utils
from matrix_relay import api as api_module
from matrix_relay import iofs

api = api_module.MatrixHttpApi("https://localhost:8448")


def test_create_relayer(monkeypatch):
    monkeypatch.setattr(api, "as_register", lambda s: None)
    monkeypatch.setattr(iofs, "save_data", lambda p, d: None)
    monkeypatch.setattr(iofs, "retrieve_all_data", lambda p, t: [])
    lp = utils.create_relayer("@test:example.com", ".", api)
    assert lp == "relay_=40test=3aexample.com"
