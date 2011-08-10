# vim: set expandtab set ts=4 tw=4
#
# This file is part of Barabas Server.
#
# Copyright (C) 2011 Nathan Samson
# Barabas Server is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Barabas Server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Barabas Server.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from storm.locals import *

class User(object):
    __storm_table__ = "User"
    
    id = Int(primary=True)
    firstName = Unicode()
    lastName = Unicode()
    email = Unicode() #TODO: Make this unique
    lastLoginTime = DateTime()
    registrationDate = Date()

    def __init__(self, firstName, lastName, email):
        """Empty docstring"""
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    
    def login(self):
        """Empty docstring"""
        self.lastLoginTime = datetime.datetime.now()

class EmailInUseError(Exception):
    pass
