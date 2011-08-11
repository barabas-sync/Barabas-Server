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


import ConfigParser
import SocketServer
import sys
import threading

from barabas.network.protocolhandler import ProtocolHandler
from barabas.network.channels.simplechannelmanager import SimpleChannelManager
from barabas.simplestoragemanager import SimpleStorageManager

class BarabasServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    __database_stores = {}

    def __init__(self, host, port, config):
        """Empty docstring"""
        
        
        self.__load_database(config)
        self.__channel_manager = SimpleChannelManager(
            host,
            xrange(config.getint('Server', 'data_port_min'),
                   config.getint('Server', 'data_port_max')),
            self.__get_public_ip(config))
        self.__channel_manager.start()
        self.__load_storage_manager(config)
        SocketServer.TCPServer.__init__(self, (host, port),
                                        ProtocolHandler)
    
    def get_database_store(self):
        """Empty docstring"""
        current_thread = threading.current_thread()
        if (threading.current_thread() not in BarabasServer.__database_stores):
            BarabasServer.__database_stores[current_thread] = \
                self.__database.new_store()
        return BarabasServer.__database_stores[current_thread]
    
    def get_channel_manager(self):
        """Empty docstring"""
        return self.__channel_manager
    
    def get_storage_manager(self):
        """Empty docstring"""
        return self.__storage_manager
    
    def shutdown(self):
        """Empty docstring"""
        SocketServer.TCPServer.shutdown(self)
        self.__channel_manager.stop()
    
    
    def __load_database(self, config):
        """Load the database with info from the configuration file"""
        module = config.get('Database', 'module')
        __import__(module)
        constructor_name = config.get('Database', 'constructor')
        constructor = sys.modules[module].__dict__[constructor_name]
        
        args = {}
        for (name, value) in config.items('Database'):
            if name not in ['module', 'constructor']:
                args[name] = value
        
        self.__database = constructor(**args)

    def __load_storage_manager(self, config):
        """Load the storage manager with info from the configuration file"""
        module = config.get('Storage', 'module')
        __import__(module)
        constructor_name = config.get('Storage', 'constructor')
        constructor = sys.modules[module].__dict__[constructor_name]
        
        args = {}
        for (name, value) in config.items('Storage'):
            if name not in ['module', 'constructor']:
                args[name] = value
        
        self.__storage_manager = constructor(**args)
        
    def __get_public_ip(self, config):
        """Returns the Public IP as defined in the config file.
        
           Can return None if te public IP is the same as the IP where
           clients connect to. Cases where the server is behind NAT are able
           to return None. Cases where the server is behind a Load Balancer
           that is not sticky (Thank you Amazon) have to return something.
        """
        
        if config.has_option('Server', 'public_ip'):
            return config.get('Server', 'public_ip')
        elif config.has_option('Server', 'public_ip_module'):
            module = config.get('Server', 'public_ip_module')
            __import__(module)
            function_name = config.get('Server', 'public_ip_function')
            return sys.modules[module].__dict__[function_name]()
        else:
            return None

if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read('barabas-server.cfg')

    s = BarabasServer(config.get("Server", "listen_address"),
                      config.getint("Server", "listen_port"),
                      config)

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
