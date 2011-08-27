# vim: set expandtab set ts=4 tw=4

import io
import hashlib

from barabas.objects.syncedfileversion import SyncedFileVersion

class StringIOStorage:
    """A Mock Storage. It stores everything in memory and does not need
       configuration
    """
    def __init__(self):
        """Empty docstring"""
        self.__strings = {}
    
    def save(self, input_file):
        """Empty docstring"""
        string = input_file.read()
        calculated_hash = unicode(hashlib.sha1(string.encode()).hexdigest())
        self.__strings[calculated_hash] = string
        return calculated_hash
    
    def open(self, fptr):
        """Empty docstring"""
        return io.StringIO(self.__strings[fptr])
