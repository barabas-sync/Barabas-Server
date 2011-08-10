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
import time
import random

from simplechannel import DownloadChannel, UploadChannel

class SimpleChannelManager(threading.Thread):
    CLEANUP_INTERVAL = 2.0

    def __init__(self, host, port_range):
        """Empty docstring"""
        self.__host = host
        self.__port_range = port_range
        self.__used_ports = set()
        self.__running_channels = []
        self.__running = False
        threading.Thread.__init__(self)
    
    def new_download_channel(self):
        """Empty docstring"""
        port = self.__find_port()
        channel = DownloadChannel(self.__host, port)
        self.__running_channels.append(channel)
        return channel
    
    def new_upload_channel(self, file_data):
        """Empty docstring"""
        port = self.__find_port()
        channel = UploadChannel(self.__host, port, file_data)
        self.__running_channels.append(channel)
        return channel
    
    def stop(self):
        """Empty docstring"""
        self.__running = False
    
    def run(self):
        """Empty docstring"""
        self.__running = True
        while self.__running:
            for channel in self.__running_channels:
                if channel.is_ready():
                    channel.stop()
                    self.__used_ports.discard(channel.port)
                    self.__running_channels.remove(channel)
                    print "Stopped %s" % (channel.port, )
            time.sleep(SimpleChannelManager.CLEANUP_INTERVAL)
    
    def __find_port(self):
        """Empty docstring"""
        port = random.choice(self.__port_range)
        while port in self.__used_ports:
            port = random.choice(self.__port_range)
        
        self.__used_ports.add(port)
        return port
