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

import storm
from storm.locals import *

class LogEntry(object):
    __storm_table__ = "HistoryLog"
    __storm_primary__ = "ID"

    ID = Int(primary = True)
    fileID = Int()
    isNew = Bool()
    
    fileName = Unicode()
    mimetype = Unicode()
    
    tagName = Unicode()
    
    versionID = Int()
    versionName = Unicode()
    timeEdited = DateTime()
    
    def __init__(self,
                 file,
                 is_new,
                 file_name=None,
                 mimetype=None,
                 tag_name=None,
                 version=None,
                 version_name=None,
                 time_edited=None):
        # self.file and self.version are defined (respectively)
        # by SyncedFile and SyncedFileVersion
        self.file = file
        self.isNew = is_new
        self.fileName = file_name
        self.tagName = tag_name
        self.version = version
        self.versionName = version_name
        self.timeEdited = time_edited
