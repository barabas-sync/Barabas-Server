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


class DownloadChannel():
    def __init__(self):
        """Constructor"""
        self.file = tempfile.TemporaryFile()
        self.fileLock = threading.Lock()

    def execute(self, socket):
        """ Execute what has to be done in the channel.
            Reads information from the socket and store it in a temporary file.
        """
        try:
            self.fileLock.acquire()
            buf = socket.recv(1024)
            while buf:
                self.file.write(buf)
                buf = socket.recv(1024)
        finally:
            self.fileLock.release()

    def open(self):
        """Open the downloaded file. Once closed the file will be deleted."""
        try:
            self.fileLock.acquire()
            self.file.seek(0)
            return self.file
        finally:
            self.fileLock.release()

class UploadChannel():
    def __init__(self, transfer_file):
        """Constructor"""
        self.transfer_file = transfer_file
    
    def execute(self, socket):
        """Execute the upload. Reads data from the channel and send it."""
        buf = self.transfer_file.read(1024)
        while buf:
            socket.send(buf)
            buf = self.transfer_file.read(1024)

