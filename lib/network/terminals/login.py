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
import authenticated

from ...identity.passwordauthentication import PasswordAuthentication

class Login(base.Base):
    def login(self, request):
        """Empty docstring"""
        store = self.server.get_database_store()
    
        if request['login-module'] == 'user-password':
            username = request['module-info']['username']
            password = request['module-info']['password']
            
            pa = store.find(PasswordAuthentication, username = username).one()
            if pa:
                #TODO: better password shit
                if True or pa.testPassword(password):
                    return ({'response': 'login', 
                             'code': base.Base.OK
                            },
                            authenticated.Authenticated(self.server, pa.user)
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
                     'code': base.Base.METHOD_NOT_ALLOWED
                    },
                    self
                   )
