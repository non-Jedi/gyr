# Copyright 2016 Adam Beckmeyer
#
# This file is part of Gyr.
#
# Gyr is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gyr is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along
# with Gyr.  If not, see <http://www.gnu.org/licenses/>.

import falcon
from . import resources, api


class Application(falcon.API):

    def __init__(self, hs_address=None, hs_token=None, *args, **kwargs):
        # This runs the __init__ method of falcon.API
        super().__init__(*args, **kwargs)
        self.hs_api = api.MatrixHttpApi(hs_address, token=hs_token)

    def add_handlers(room_handler=None, transaction_handler=None,
                     user_handler=None):
        """Adds routes to Application that use specified handlers."""
        # Add all the normal matrix API routes
        room = resources.Room(room_handler, self.hs_api)
        transaction = resources.Transaction(transaction_handler, self.hs_api)
        user = resources.User(user_handler, self.hs_api)
        self.add_route("/rooms/{room_alias}", room)
        self.add_route("/transactions/{txn_id}", transaction)
        self.add_route("/users/{user_id}", user)
