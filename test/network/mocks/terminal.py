# vim: set expandtab set ts=4 tw=4

class _UpdatedMockTerminal():
    """An updated mock terminal"""
    
    def __init__(self, server):
        """Constructor"""
        self._server = server
    
    def mockUpdated(self, data):
        return ({'response': 'mockUpdated',
                 'code': 200,
                 'server-name': self._server.name()}, self)

    def stop(self):
        """The client or server stopped the connection."""
        pass

class MockTerminal():
    def __init__(self, server):
        """Constructor"""
        self._server = server

    def mock(self, data):
        return ({'response': 'mock',
                 'code': 200,
                 'data': data}, self)

    def serverName(self, data):
        return ({'response': 'serverName',
                 'code': 200,
                 'server-name': self._server.name()}, self)
    
    def update(self, data):
        return ({'response': 'update',
                 'code': 200}, _UpdatedMockTerminal(self._server))

    def stop(self):
        """The client or server stopped the connection."""
        pass
