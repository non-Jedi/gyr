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

from . import utils
from . import iofs


class MatrixUser:
    """Represents matrix user account."""

    def __init__(self, mxid, storage_path=None, api=None, data=None):
        self.mxid = mxid
        self.localpart, self.domain = mxid.strip("@").split(":")
        # Storage_path is only applicable if using iofs backend
        self.storage_path = storage_path
        self.api = api
        self.data = data

    def load(self, mxid):
        """loads data from iofs database."""
        self.mxid = mxid
        self.localpart, self.domain = mxid.strip("@").split(":")

        mxid_path = iofs.resolve_path(mxid, self.storage_path)
        self.data = iofs.retrieve_data(mxid_path)

    def send_message(self, content, rooms):
        """Sends m.room.message using self.api."""
        for room in rooms:
            self.api.send_event(room, "m.room.message", utils.new_txn_id(),
                                content=content,
                                params={"user_id": self.localpart})
