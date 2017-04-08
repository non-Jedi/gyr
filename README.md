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

# Status

Pre-alpha! Breaking changes happen on a weekly to daily basis, and the
developer(s) mostly don't notice at all since this isn't being used for
anything yet.

# Projects Using Gyr

None for now! Check back later.

# Modules

## gyr.server

`server` provides the WSGI application class. An instance of
gyr.server.Application functions as the WSGI app and will automatically
parse the request and call any handlers provided to the Application
instance.

## gyr.api

`api` provides a helpful wrapper for
[matrix-python-sdk](https://github.com/matrix-org/matrix-python-sdk)'s
api, changing the parts of the api that are different for application
services until such time as similiar changes are merged upstream. Pull
requests for these changes have been submitted, and some changes already
merged into master.

For working with the api, I recommend using the wrappers built around
specific objects which are available in gyr.matrix_objects.

## gyr.matrix_objects

`matrix_objects` provides helpful wrapper classes around matrix users,
events and rooms. It is not designed to be easily used for the normal
client-server api but should provide most necessary functionality for
the manipulation of users and rooms that an application service might
need to do.

Pull requests enriching the functionality of these classes are very
welcome.

# Gyr Internals

Gyr builds on [falcon](https://falconframework.org) to create its WSGI
application class. For sending http requests, Gyr uses
[requests](https://python-requests.org).
