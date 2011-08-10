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

import hashlib
import random
import string
from storm.locals import *

from user import User

class PasswordAuthentication(object):
    __storm_table__ = "PasswordAuthentication"

    id = Int(primary = True)
    userID = Int()
    username = Unicode()
    passwordSalt = Unicode()
    passwordHash = Unicode()
    resetHash = Unicode()
    
    user = Reference(userID, User.id)

    def __init__(self):
        """Empty docstring"""
        pass
    
    def testPassword(self, password):
        """Empty docstring"""
        return self.passwordHash == hashlib.sha512(self.passwordSalt + password).hexdigest()
    
    def password(self, newPassword):
        """Empty docstring"""
        self.passwordSalt = self.__randomString(32)
        self.passwordHash = unicode(hashlib.sha512(self.passwordSalt + newPassword).hexdigest())
    
    def requestReset(self):
        """Empty docstring"""
        self.resetHash = self.__randomString(64)
        return self.resetHash
    
    def isResetHash(self, resetHash):
        """Empty docstring"""
        return self.resetHash == resetHash
    
    def reset(self, resetHash, newPassword):
        """Empty docstring"""
        if resetHash == None:
            raise Exception("Reset Hash is wrong")
        if not self.isResetHash(resetHash):
            raise Exception("Reset Hash is wrong")
        
        self.resetHash = None
        self.password(newPassword)
    
    def __randomString(self, length):
        """Empty docstring"""
        if random.SystemRandom:
            r = random.SystemRandom()
        else:
            r = random
        
        return u"".join([random.choice(string.letters + string.digits) for i in xrange(length)])
