# vim: set expandtab set ts=4 tw=4

"""A mock server class"""

class _MockStore():
    """A mock store class"""
    
    def commit(self):
        """ The commit method """
        pass

class MockServer():
    """Mock server class"""
    
    def __init__(self, name="", store=None):
        """Constructor"""
        self.__name = name
        if store == None:
            store = _MockStore()
        self.__store = store
    
    def name(self):
        """Returns the name of the server"""
        return self.__name
    
    def get_database_store(self):
        """" Returns the database store. """
        return self.__store
