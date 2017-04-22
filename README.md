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

Gyr is a framework for quickly developing [matrix](https://matrix.org)
[application
services](http://matrix.org/docs/spec/application_service/unstable.html) in
python3. It provides a WSGI application and several other utilities for working
with matrix. 

Gyr is designed to be a fairly thin layer of abstraction over application
service api--just enough to make things easy without pushing you so far from the
spec that you get confused.

# Installation

Please install gyr with pip (in a virtualenv if you prefer):

```sh
pip install gyr
```

# Usage

I'll try to show a bunch of functionality here, but see examples directory for
further usage examples.

```python
from gyr import server, matrix_objects

application = server.Application("http://localhost:8008", "foobar")

as_user = matrix_objects.MatrixUser("@example_as:example.com",
                                    application.create_api)
room = as_user.create_room(alias="#foo:example.com", is_public=True)

def rm_hndlr(room_id):
    # Gyr will create a user for you if this returns true!
    return False
    
def user_hndlr(user_id):
    # Gyr will create the room for you if this returns true!
    return False
    
def txn_hndlr(events):
    for event in events:
    	room.send_notice(
	    "Received event type {} in room {} from user {}".format(event.type,
	                                                            event.room,
								    event.user)
	)
    return True
	
application.add_handlers(room_handler=rm_hndlr, transaction_handler=txn_hndlr,
                         user_handler=user_hndlr)
```

Save as example.py. Then from the commandline:

```sh
gunicorn example:application
```

# Status

Very alpha! Most of the main functionality I'd envisioned is present, however
there's poor to non-existent documentation and no unit tests. Contributions are
welcome.

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
