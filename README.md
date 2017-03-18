<!---

Copyright 2016 Adam Beckmeyer

This file is part of Gyr.

Gyr is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Gyr is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Gyr. If not, see <http://www.gnu.org/licenses/>.  

--> 

# Gyr

Gyr is a framework for developing [matrix](https://matrix.org) [application
services](http://matrix.org/docs/spec/application_service/unstable.html). It
provides a WSGI application and several other utilities for working with
matrix. It's designed to be a fairly thin layer of abstraction over
application service api.

# Projects Using Gyr

None for now! Check back later.

# Modules

## gyr.server

Server provides the WSGI application class. An instance of
gyr.server.Application functions as the WSGI app and will automatically
parse the request and call any handlers provided to the Application
instance.

## gyr.api

Api provides a convenience class for working with the parts of the [matrix
client-server api](http://matrix.org/docs/spec/client_server/r0.2.0.html)
which are different for an application service than for a normal client (see
the [AS
spec](http://matrix.org/docs/spec/application_service/unstable.html#client-server-api-extensions)).
For working with other parts of the client-server api, we recommend using
[matrix-python-sdk](https://github.com/matrix-org/matrix-python-sdk).

# Gyr Internals

Gyr builds on [falcon](https://falconframework.org) to create its WSGI
application class. For sending http requests, Gyr uses
[requests](https://python-requests.org).
