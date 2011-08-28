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

"""Handshake terminal class"""

import barabas.network.terminals.base as base
import barabas.network.terminals.login as login

class Handshake(base.Base):
    """Handhsake terminal"""
    def __init__(self, server):
        """Constructor"""
        base.Base.__init__(self, server)
        self.__supported_versions = [1]
        self.__versions = [1]
        self.__supported_login_modules = ['user-password']

    def handshake(self, request):
        """Response for the handshake message. The handshake message
           negotiates the protocol version and supported login modules.
        """
        version_found = False
        for version in self.__versions:
            if version == request['version']:
                version_found = True
                break
        
        if not version_found:
            raise base.ProtocolException(base.Base.VERSION_NOT_SUPPORTED,
                                         'Version not supported')

        login_modules = list(set(self.__supported_login_modules) &
                             set(request['login-modules']))
        if (len(login_modules) == 0):
            raise base.ProtocolException(base.Base.LOGINMODULE_NOT_SUPPORTED,
                                         'No matching login modules')
        else:
            return ({'response': 'handshake', 
                     'code': base.Base.OK,
                     'login-modules': login_modules
                    }, 
                    login.Login(self.server)
                   )
