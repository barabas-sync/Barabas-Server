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

"""Login terminal"""

import barabas.network.terminals.base as base
import barabas.network.terminals.authenticated as authenticated

from barabas.identity.passwordauthentication import PasswordAuthentication

class Login(base.Base):
    """Login terminal"""
    def __init__(self, server,
                 authenticated_terminal=authenticated.Authenticated):
        """Constructor"""
        base.Base.__init__(self, server)
        self.__authenticated_terminal = authenticated_terminal

    def login(self, request):
        """Login method."""
        store = self.server.get_database_store()
    
        if request['login-module'] == 'user-password':
            username = unicode(request['module-info']['username'])
            password = request['module-info']['password']
            
            password_auth = store.find(PasswordAuthentication,
                                       username = username).one()
            if password_auth:
                if password_auth.testPassword(password):
                    return ({'response': 'login', 
                             'code': base.Base.OK
                            },
                            self.__authenticated_terminal(self.server,
                                                          password_auth.user)
                           )
                else:
                    return ({'response': 'login',
                             'code': base.Base.USER_NOT_FOUND,
                             'msg': 'Wrong username or password'
                            },
                            self
                           )
            else:
                return ({'response': 'login',
                          'code': base.Base.USER_NOT_FOUND,
                          'msg': 'Wrong username or password'
                        },
                        self
                       )
        else:
            return ({'response': 'login', 
                     'code': base.Base.METHOD_NOT_ALLOWED,
                     'msg': 'Login module not supported'
                    },
                    self
                   )
