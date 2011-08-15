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

import base
import login

class Handshake(base.Base):
    def handshake(self, request):
        """Empty docstring"""
        self.__versions = [1]
        self.__loginModules = ['user-password']

        serverIndex = 0
        
        while (serverIndex < len(self.__versions) and 
               self.__versions[serverIndex] > request['version']):
            serverIndex += 1
        
        if serverIndex >= len(self.__versions):
            raise base.ProtocolException(base.Base.VERSION_NOT_SUPPORTED, 'Version not supported')

        loginModules = list(set(self.__loginModules) & set(request['login-modules']))
        if (len(loginModules) == 0):
            raise base.ProtocolException(base.Base.LOGINMODULE_NOT_SUPPORTED, 'No matching login modules')
        else:
            return ({'response': 'handshake', 
                     'code': base.Base.OK,
                     'login-modules': loginModules
                    }, 
                    login.Login(self.server)
                   )
