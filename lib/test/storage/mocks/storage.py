import io
import hashlib

import server.storage.fileversion

class StringIOStorage:
    def __init__(self):
        """Empty docstring"""
        self.__strings = {}

    def create(self, inputFile, editTime):
        """Empty docstring"""
        return server.storage.fileversion.FileVersion(inputFile, editTime, self)
    
    def save(self, inputFile):
        """Empty docstring"""
        string = inputFile.read()
        hash = unicode(hashlib.sha1(string.encode()).hexdigest())
        self.__strings[hash] = string
        return hash
    
    def open(self, fptr):
        """Empty docstring"""
        return io.StringIO(self.__strings[fptr])
