import collections
import datetime

import base
from base import ProtocolException
from ...objects.syncedfile import SyncedFile
from ...objects.syncedfileversion import SyncedFileVersion
from ...objects.logentry import LogEntry

class Authenticated(base.Base):
    class IDList():
        def __init__(self):
            """Empty docstring"""
            self.__currentSmallestFree = 1
            self.__dict = {}
        
        def append(self, el):
            """Empty docstring"""
            newID = self.__currentSmallestFree
            self.__dict[newID] = el
            freeKey = newID
            while freeKey in self.__dict:
                freeKey += 1
            self.__currentSmallestFree = freeKey
            return newID
        
        def pop(self, key):
            """Empty docstring"""
            value = self.__dict[key]
            del self.__dict[key]
            #if key < self.__currentSmallestFree:
            #    self.__currentSmallestFree = key
            return value
        
        def __getitem__(self, key):
            """Empty docstring"""
            return self.__dict[key]
        
        def has(self, key):
            """Empty docstring"""
            return key in self.__dict
        
        def __iter__(self):
        	return self.__dict.__iter__()
    
    NewVersion = collections.namedtuple('NewVersion', ['synced_file',
                                                       'download_handler',
                                                        'name',
                                                        'time_edited'])

    def __init__(self, server, user):
        """Empty docstring"""
        base.Base.__init__(self, server)
        self.store = server.get_database_store()
        self.__user = user
        self.__version_commit_list   = Authenticated.IDList()

    def newFile(self, request):
        """Empty docstring"""
        file_name = request['file-name']
        mimetype = request['mimetype']
        
        synced_file = SyncedFile(file_name, self.__user)
        synced_file.mimetype = mimetype
        synced_file.add_to_store(self.store)
        self.store.commit()
        
        response = {
                    'response': 'newFile',
                    'code': base.Base.OK,
                    'file-id': synced_file.ID
                   }
        
        return (response, self)
        
    
    def requestVersion(self, request):
        """Empty docstring"""
        synced_file = self.store.find(SyncedFile,
                                      ID=request['file-id'],
                                      owner=self.__user).one()
        if not synced_file:
            raise ProtocolException(base.Base.FILE_NOT_FOUND, 'File not found')
        
        new_channel, chandler = self.server.get_channel_manager().new_download_channel()
        new_version = Authenticated.NewVersion(synced_file=synced_file,
                                               download_handler=chandler,
                                               name=request['version-name'],
                                               time_edited=request['datetime-edited'])
        commit_id = self.__version_commit_list.append(new_version)
        
        response = {'response': 'requestVersion',
                    'code': base.Base.OK,
                    'commit-id': commit_id,
                    'channel-info': {
                                     'host': new_channel.connect_ip,
                                     'port': new_channel.port,
                                     'secret': new_channel.secret
                                    }
                   }
    
        return (response, self)
    
    def commitVersion(self, request):
        """Empty docstring"""
        commit_id = request['commit-id']
        if not self.__version_commit_list.has(commit_id):
            raise ProtocolException(base.Base.BAD_REQUEST, 'Commit ID not valid')
        
        
        new_version = self.__version_commit_list.pop(commit_id)
        storage_manager = self.server.get_storage_manager()
        synced_file = new_version.synced_file
        filedata = new_version.download_handler.open()
        synced_file_version = SyncedFileVersion(filedata,
                                                new_version.name,
                                                new_version.time_edited,
                                                storage_manager)
        synced_file.add_version(synced_file_version)
        self.store.commit() # Make sure the file version is stored
        #TODO: is their a reason we only close the data here?
        filedata.close()
        
        response = {
                    'response': 'commitVersion',
                    'code': base.Base.OK,
                    'version-id': synced_file_version.ID
                   }
        
        return (response, self)
    
    def requestDownload(self, request):
        """Empty docstring"""
        synced_file_version = self.store.find(SyncedFileVersion,
                                              ID=request['version-id']).one()
        
        if synced_file_version == None or synced_file_version.syncedfile.owner != self.__user:
            raise ProtocolException(base.Base.FILE_NOT_FOUND, 'File not found') 
            
        file_data = synced_file_version.open(self.server.get_storage_manager())
        new_channel, channel_handler = self.server.get_channel_manager().new_upload_channel(file_data)
        
        response = {'response': 'requestDownload',
                    'code': base.Base.OK,
                    'channel-info': {
                                     'host': new_channel.connect_ip,
                                     'port': new_channel.port,
                                     'secret': new_channel.secret
                                    }
                   }
    
        return (response, self)
    
    def tag(self, request):
        """Empty docstring"""
        synced_file = self.store.find(SyncedFile,
                                      ID=request['file-id'],
                                      owner=self.__user).one()
        if not synced_file:
            raise ProtocolException(base.Base.FILE_NOT_FOUND, 'File not found')
        
        synced_file.tag(request['tag'])
        self.store.commit()
        
        response = {
                    'response': 'tag',
                    'code': base.Base.OK
                   }
        
        return (response, self)
    
    def untag(self, request):
        """Empty docstring"""
        synced_file = self.store.find(SyncedFile,
                                      ID=request['file-id'],
                                      owner=self.__user).one()
        if not synced_file:
            raise ProtocolException(base.Base.FILE_NOT_FOUND, 'File not found')
        
        synced_file.untag(request['tag'])
        self.store.commit()
        
        response = {
                    'response': 'untag',
                    'code': base.Base.OK
                   }
        
        return (response, self)

    def downloadLog(self, request):
        """Empty docstring"""
        def log_entry(entry):
            """Empty docstring"""
            if (entry.tagName == None and entry.versionID == None and entry.isNew == True):
                return {'type': 'new-file',
                        'log-id': entry.ID,
                        'id': entry.fileID,
                        'name': entry.fileName,
                        'mimetype': entry.mimetype
                       }
            elif (entry.tagName != None and entry.isNew):
                return {'type': 'tag', 
                        'log-id': entry.ID,
                        'id': entry.fileID,
                        'tag': entry.tagName
                       }
            elif (entry.tagName != None and not entry.isNew):
                return {'type': 'untag', 
                        'log-id': entry.ID,
                        'id': entry.fileID,
                        'tag': entry.tagName
                       }
            elif (entry.versionID != None and entry.isNew):
                return {'type': 'new-version', 
                        'log-id': entry.ID,
                        'id': entry.fileID,
                        'version-id': entry.versionID,
                        'version-name': entry.versionName,
                        'version-timeedited': entry.timeEdited
                       }
            return {'type': 'unknown'}
    
        entries = [log_entry(entry) for entry in self.store.find(
                                        LogEntry,
                                        SyncedFile.ID == LogEntry.fileID,
                                        SyncedFile.owner == self.__user,
                                        LogEntry.ID > request['latest-entry'])]
        return ({'response': 'downloadLog',
                 'code': base.Base.OK,
                 'entries': entries
                },
                self
               )
