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

from dataserver import DataServer
from simplechannel import DownloadChannel, UploadChannel

class SimpleChannelManager(threading.Thread):
    def __init__(self, host, port, connect_ip):
        """Empty docstring"""
        self.__server = DataServer(host, port, connect_ip)
        self.__server_thread = threading.Thread(target=self.__server.serve_forever)
        threading.Thread.__init__(self)
    
    def new_download_channel(self):
        """Empty docstring"""
        return self.__server.open_channel(DownloadChannel())
    
    def new_upload_channel(self, file_data):
        """Empty docstring"""
        return self.__server.open_channel(UploadChannel(file_data))
    
    def stop(self):
        """Empty docstring"""
        self.__server.shutdown()
    
    def run(self):
        """Empty docstring"""
        self.__server_thread.start()
