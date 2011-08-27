# vim: set expandtab set ts=4 tw=4

"""A mock request class"""

class MockRequest():
    """A mock request class"""
    
    def __init__(self):
        self._in_msgs = []
        self._out_msgs = []
    
    def push(self, msg):
        self._in_msgs.append(msg)
    
    def pop(self):
        if len(self._out_msgs) == 0:
            return None
        return self._out_msgs.pop(0) 
    
    # Mocked implementations follow
    def recv(self, length):
        """Receives data from the stream. The length is ignored.
           We know the caller should call this with large numbers, we only
           return small strings
        """
        if len(self._in_msgs) == 0:
            return ""
        return self._in_msgs.pop(0)
    
    def send(self, send):
        """Send data over the stream. The data is appended to the out messages
        """
        self._out_msgs.append(send)
        return len(send)
    
    def getpeername(self):
        """Returns the peer name"""
        return ('1.2.3.4', 1234)
