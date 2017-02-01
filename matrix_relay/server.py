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

import os
import json
import falcon
from . import resources

# Load configuration
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_path = os.path.join(dir_path, 'config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

api = application = falcon.API()

room = resources.Room(None, config)
transaction = resources.Transaction(None, config)
user = resources.User(None, config)
api.add_route("/rooms/{room_alias}", room)
api.add_route("/transactions/{txn_id}", transaction)
api.add_route("/users/{user_id}", user)
