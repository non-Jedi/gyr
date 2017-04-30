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


class GyrException(Exception):
    pass


class HttpRequestError(GyrException):
    """Wraps exceptions raised when making http requests to matrix server."""

    def __init__(self, msg, original_exception):
        super(HttpRequestError, self).__init__(
            "{}: {}".format(msg, original_exception)
        )
        self.original_exception = original_exception


class MatrixError(GyrException):

    def __init__(self, msg, original_exception):
        super(MatrixError, self).__init__(
            "{}. {}".format(msg, original_exception)
        )
        self.original_exception = original_exception
