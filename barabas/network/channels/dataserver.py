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

import random
import string
import SocketServer
import threading

class DataServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    SECRET_KEY_LENGTH = 128

    class DataHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            secret_key = ""
            verified = False
            while len(secret_key) < DataServer.SECRET_KEY_LENGTH:
                secret_key += self.request.recv(DataServer.SECRET_KEY_LENGTH - len(secret_key))
                if len(secret_key) == 0:
                    return
            
            channel = self.server.get_channel(secret_key)
            if channel != None:
                channel.execute(self.request)
                

    class ChannelInfo:
        def __init__(self, connect_ip, port, secret):
            self.connect_ip = connect_ip
            self.port = port
            self.secret = secret

    def __init__(self, host, port, connect_ip):
        self.__lock = threading.Lock()
        self.__host = host
        self.__port = port
        self.__connect_ip = connect_ip
        self.__channels = {}
        SocketServer.TCPServer.__init__(self, (host, port), DataServer.DataHandler)
    
    def get_channel(self, key):
        try:
            self.__lock.acquire()
            if key in self.__channels:
                handler = self.__channels[key]
                del self.__channels[key]
                return handler
            else:
                return None
        finally:
            self.__lock.release()
    
    def open_channel(self, channel_handler):
        try:
            self.__lock.acquire()
            secret = self.__create_key()
            self.__channels[secret] = channel_handler
            return DataServer.ChannelInfo(self.__connect_ip, self.__port, secret), channel_handler
        finally:
            self.__lock.release()
    
    def __create_key(self):
        def rndstr():
          return ''.join(random.choice(string.letters + string.digits)
                         for i in xrange(DataServer.SECRET_KEY_LENGTH))  
    
        key = rndstr()
        while key in self.__channels:
            key = rndstr()
        return key
