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

import threading
import SocketServer
import tempfile

class Channel(threading.Thread):
    def __init__(self, host, port, connect_ip):
        """Empty docstring"""
        self.__host = host
        self.port = port
        self.connect_ip = connect_ip
        self.__ready = False
        threading.Thread.__init__(self)
    
    def port(self):
        """Empty docstring"""
        return self.__port    
    
    def run(self):
        """Empty docstring"""
        self.server = SocketServer.TCPServer((self.__host, self.port), self.handler)
        self.server.channel = self
        self.server.serve_forever()
    
    def set_ready(self):
        """Empty docstring"""
        self.__ready = True
    
    def is_ready(self):
        """Empty docstring"""
        return self.__ready
    
    def stop(self):
        """Empty docstring"""
        self.server.shutdown()


class DownloadChannel(Channel):
    def __init__(self, host, port, connect_ip):
        """Empty docstring"""
        Channel.__init__(self, host, port, connect_ip)
        self.handler = DownloadChannel.Handler
    
    def open(self):
        """Empty docstring"""
        return self.current_handler.read()
    
    class Handler(SocketServer.BaseRequestHandler):
        def setup(self):
            """Empty docstring"""
            self.server.channel.current_handler = self
            self.file = tempfile.TemporaryFile()
            self.fileLock = threading.RLock()
            self.fileLock.acquire()

        def handle(self):
            """Empty docstring"""
            buf = self.request.recv(1024)
            while buf:
                self.file.write(buf)
                buf = self.request.recv(1024)
            self.fileLock.release()
            self.server.channel.set_ready()

        def read(self):
            """Empty docstring"""
            self.fileLock.acquire()
            self.file.seek(0)
            self.fileLock.release()
            return self.file

class UploadChannel(Channel):
    def __init__(self, host, port, connect_ip, transfer_file):
        """Empty docstring"""
        Channel.__init__(self, host, port, connect_ip)
        self.handler = UploadChannel.Handler
        self.transfer_file = transfer_file
    
    class Handler(SocketServer.BaseRequestHandler):
        def handle(self):
            """Empty docstring"""
            buf = self.server.channel.transfer_file.read(1024)
            while buf:
                self.request.send(buf)
                buf = self.server.channel.transfer_file.read(1024)
            self.server.channel.set_ready()
