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

from storm.locals import create_database

from sqldatabase import SQLDatabase

class PostgreSQL(SQLDatabase):
    def __init__(self, username, password, hostname, database_name, port = 5432):
        args = {'username': username,
                'password': password,
                'hostname': hostname,
                'port': port,
                'database_name': database_name}
        SQLDatabase.__init__(self, create_database('postgres://%(username)s:%(password)s@%(hostname)s:%(port)d/%(database_name)s' % args))

            
