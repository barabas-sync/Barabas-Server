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

class Base():
    OK = 200
    BAD_REQUEST = 400
    FILE_NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_IMPLEMENTED = 501
    VERSION_NOT_SUPPORTED = 505
    LOGINMODULE_NOT_SUPPORTED = 520
    USER_NOT_FOUND = 1000

    def __init__(self, server):
        """Empty docstring"""
        self.server = server
    
    def stop(self):
        print "BASE STOP"
        pass

class ProtocolException(Exception):
    def __init__(self, code, msg):
        """Empty docstring"""
        Exception.__init__(self, 'Protocol Exception = ' + str(code) + ': ' + msg)
        self.__code = code
        self.__msg = msg
    
    def code(self):
        """Empty docstring"""
        return self.__code
    
    def msg(self):
        """Empty docstring"""
        return self.__msg
