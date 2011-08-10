#! /usr/bin/env python
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


import SocketServer
import threading

from lib.network.protocolhandler import ProtocolHandler
from lib.database.postgresql import PostgreSQL
from lib.network.channels.simplechannelmanager import SimpleChannelManager
from lib.simplestoragemanager import SimpleStorageManager

class BarabasServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    __database_stores = {}

    def __init__(self, host, port = 2188):
        self.__database = PostgreSQL(hostname='localhost',
                                     username='barabas',
                                     database_name='barabasdb',
                                     password='barabaspw')
        self.__channel_manager = SimpleChannelManager(host, xrange(50000, 50010))
        self.__channel_manager.start()
        self.__storage_manager = SimpleStorageManager('./datafiles')
        SocketServer.TCPServer.__init__(self, (host, port),
                                        ProtocolHandler)
    
    def get_database_store(self):
        current_thread = threading.current_thread()
        if (threading.current_thread() not in BarabasServer.__database_stores):
            BarabasServer.__database_stores[current_thread] = \
                self.__database.new_store()
        return BarabasServer.__database_stores[current_thread]
            
    
    def get_channel_manager(self):
        return self.__channel_manager
    
    def get_storage_manager(self):
        return self.__storage_manager
        
    
    def shutdown(self):
        SocketServer.TCPServer.shutdown(self)
        self.__channel_manager.stop()

if __name__ == "__main__":
    s = BarabasServer('0.0.0.0')

    try:
        s.serve_forever()
    except KeyboardInterrupt, e:
        s.shutdown()
    except Exception, e:
        print "An unexpected error occured"
        print e
        exit(1)

    print "Goodbye..."

    exit(0)
