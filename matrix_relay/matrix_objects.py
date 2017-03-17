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

from . import utils
from . import iofs


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, storage_path, api):
        self.mxid = mxid
        self.localpart, self.domain = mxid.strip("@").split(":")
        self.storage_path = storage_path
        self.api = api

    def create_relayer(self, storage_path=None, api=None):
        """Creates MatrixUser representing "relayer" of current user."""
        # This method exists because why wouldn't we want recursive classes?
        if not storage_path:
            storage_path = self.storage_path
        if not api:
            api = self.api

        relayer_mxid = "@" + utils.mxid2relayuser(self.mxid) + ":_._"
        self.relayer = MatrixUser(relayer_mxid, storage_path, api)
        # The database is canonical source for whether registered
        if self.mxid not in utils.get_users(self.storage_path):
            self.api.as_register(self.relayer.localpart)
            user_path = iofs.resolve_path(self.mxid, self.storage_path)
            iofs.save_data(user_path, self.relayer.mxid)
        else:
            self.load(self.mxid)

    def load(self, mxid):
        """Changes object to reflect mxid from db."""
        self.mxid = mxid
        self.localpart, self.domain = mxid.strip("@").split(":")

        mxid_path = iofs.resolve_path(mxid, self.storage_path)
        mxid_data = iofs.retrieve_data(mxid_path)
        # Data should be simple string with relayer mxid
        self.relayer = MatrixUser(mxid_data, self.storage_path, self.api)

    def relay_message(self, content, rooms):
        """Uses self.relayer to send message to HS."""
        self.relayer.send_message(content, rooms)
        # Does the message need to be saved to db? Don't think so...

    def send_message(self, content, rooms):
        """Sends m.room.message using self.api."""
        for room in rooms:
            self.api.send_event(room, "m.room.message", utils.new_txn_id(),
                                content=content,
                                params={"user_id": self.localpart})
