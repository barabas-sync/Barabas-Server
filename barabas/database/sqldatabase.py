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

from storm.locals import create_database, Store

class SQLDatabase:
    class SQLStore(Store):
        def install(self, fl):
            """Empty docstring"""
            fp = open(fl)
            queries = fp.read().split("\n\n")
            for q in queries:
                self.execute(q)
            fp.close()

    def __init__(self, database):
        """Empty docstring"""
        self.__database = database
    
    def new_store(self):
        """Empty docstring"""
        return SQLDatabase.SQLStore(self.__database)
    
def create_postgresql(host, name, username, password, port = 5432):
    """Empty docstring"""
    args = (username, password, host, port, name)
    return SQLDatabase(create_database('postgres://%s:%s@%s:%s/%s' % args))

def create_mysql(host, name, username, password, port = 3306):
    """Create a MySQL Database Connection"""
    args = (username, password, host, port, name)
    return SQLDatabase(create_database('mysql://%s:%s@%s:%s/%s' % args))

def create_sqlite_use_only_for_tests():
    return SQLDatabase(create_database('sqlite:'))
