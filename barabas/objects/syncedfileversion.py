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

import datetime
from storm.locals import *

from logentry import LogEntry

class SyncedFileVersion(object):
    __storm_table__ = "SyncedFileVersion"
    ID = Int(primary = True)
    syncedFileID = Int()
    timeEdited = DateTime()
    timeStored = DateTime()
    filePointer = Unicode()
    name = Unicode()

    def __init__(self, inputFile, name, editTime, storage):
        """Empty docstring"""
        self.__data = inputFile
        self.timeEdited = editTime
        self.name = name
        self.__storage = storage
    
    def open(self, storage):
        """Empty docstring"""
        return storage.open(self.filePointer)
    
    def __storm_loaded__(self):
        """Empty docstring"""
        self.__storage = None
    
    def __storm_pre_flush__(self):
        """Empty docstring"""
        if self.__storage:
            self.timeStored = datetime.datetime.now()
            self.filePointer = self.__storage.save(self.__data)
        else:    
            raise Exception("No storage connected to the version")

LogEntry.version = Reference(LogEntry.versionID, SyncedFileVersion.ID)
