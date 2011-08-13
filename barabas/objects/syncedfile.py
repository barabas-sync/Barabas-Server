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

from ..identity.user import User
from syncedfileversion import SyncedFileVersion
from logentry import LogEntry

class FileTag(object):
    __storm_table__ = "FileTag"
    __storm_primary__ = "fileID", "tagName"
    
    fileID = Int()
    tagName = Unicode()
    
    def __init__(self, name):
        """Empty docstring"""
        self.tagName = name

class SyncedFile(object):
    __storm_table__ = "SyncedFile"
    ID = Int(primary = True)
    ownerId = Int()
    fileName = Unicode()
    owner = Reference(ownerId, User.id)
    mimetype = Unicode()
    versions = ReferenceSet(ID, SyncedFileVersion.syncedFileID)
    __tags = ReferenceSet(ID, FileTag.fileID)

    def __init__(self, fileName, owner = None):
        """Empty docstring"""
        self.fileName = unicode(fileName)
        self.owner = owner
    
    def findWithTags(store, user, tags):
        """Empty docstring"""
        return store.find(SyncedFile, 
                    SyncedFile.ID.is_in(
                         Select(SyncedFile.ID, 
                                      where=And(FileTag.tagName.is_in(tags), 
                                                FileTag.fileID == SyncedFile.ID,
                                                SyncedFile.owner == user),
                                      group_by=SyncedFile.ID,
                                      having=Count(FileTag.fileID) == len(tags))))
    findWithTags = staticmethod(findWithTags)
    
    def tag(self, name):
        """Empty docstring"""
        name = unicode(name)
        store = Store.of(self)
        if (store is not None):
            tag = store.find(FileTag, (FileTag.tagName == name) & (FileTag.fileID == self.ID)).one()

            if tag is None:
                tag = FileTag(name)
                self.__tags.add(tag)
                
                log_entry = LogEntry(file=self,
                                     is_new=True,
                                     tag_name=name)
                store.add(log_entry)
            store.commit()
        else:
            pass
    
    def untag(self, name):
        """Empty docstring"""
        name = unicode(name)
        store = Store.of(self)
        if (store is not None):
            tag = store.find(FileTag, (FileTag.tagName == name) & (FileTag.fileID == self.ID)).one()

            if tag is not None:
                store.remove(tag)
            store.commit()
        else:
            pass
    
    def tags(self):
        """Empty docstring"""
        return [tag.tagName for tag in self.__tags]
    
    def add_version(self, file_version):
        """A a version and corresponding log entry to the store"""
        
        self.versions.add(file_version)
        store = Store.of(self)
        log_entry = LogEntry(file=self,
                             is_new=True,
                             version=file_version,
                             version_name=file_version.name,
                             time_edited=file_version.timeEdited)
        store.add(log_entry)
    
    def add_to_store(self, store):
        """Empty docstring"""
        store.add(self)
        
        log_entry = LogEntry(file=self,
                             is_new=True,
                             file_name=self.fileName,
                             mimetype=self.mimetype)
        store.add(log_entry)

SyncedFileVersion.syncedfile = Reference(SyncedFileVersion.syncedFileID, SyncedFile.ID)
LogEntry.file = Reference(LogEntry.fileID, SyncedFile.ID)
