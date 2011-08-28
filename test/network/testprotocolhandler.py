# vim: set expandtab set ts=4 tw=4

import json
import StringIO
import unittest

from barabas.network.protocolhandler import ProtocolHandler

from test.network.mocks.terminal import MockTerminal
from test.network.mocks.server import MockServer
from test.network.mocks.request import MockRequest

class TestProtocolHandler(unittest.TestCase):
    """A unittest for the protocol handler"""
    
    def setUp(self):
        """Set up the testcase"""
        self.__request = MockRequest()
        self.__server = MockServer('A Server Name')
        ProtocolHandler.start_terminal = MockTerminal
        self.__protocol_handler = ProtocolHandler(self.__request,
                                                  self.__request.getpeername(),
                                                  self.__server)
        self.__protocol_handler.setup()
        self.__protocol_handler.request = self.__request
    
    def assert_responses(self, messages):
        for msg in messages:
            response_msg = self.__request.pop()
            self.assertEqual("\n", response_msg[-1], "Message ends with \\n")
            
            response_json = json.load(StringIO.StringIO(response_msg))
            self.assertEqual(msg, response_json)
         
        self.assertIsNone(self.__request.pop(), "No more messages")
    
    def test_simple_message(self):
        """Test that ensures correct handling of a correct message"""
        self.__request.push('{"request": "mock", "data": "somedata"}\n')
        self.__request.push('{"request": "serverName"}\n')
        
        self.__protocol_handler.handle()
        
        msg1 = {'code': 200,
               'data': {'data': 'somedata', 'request': 'mock'},
               'response': 'mock'}
        
        msg2 = {'code': 200,
               'server-name': self.__server.name(),
               'response': 'serverName'}
        self.assert_responses([msg1, msg2])
    
    def test_handle_new_terminal(self):
        """Tests that the handler correctly runs a new terminal"""
        self.__request.push('{"request": "update"}\n')
        self.__request.push('{"request": "mockUpdated"}\n')
        
        self.__protocol_handler.handle()
        
        msg1 = {'code': 200,
               'response': 'update'}
        
        msg2 = {'code': 200,
               'response': 'mockUpdated',
               'server-name': self.__server.name()}
        self.assert_responses([msg1, msg2])
    
    def test_incomplete_message(self):
        """Test that ensures that when a message is not received in one
            packet it still will be handled correctly."""
        self.__request.push('{"request": "mock",')
        self.__request.push(' "data": "somedata"}\n')
        
        self.__protocol_handler.handle()
        
        msg = {'code': 200,
               'data': {'data': 'somedata', 'request': 'mock'},
               'response': 'mock'}
        self.assert_responses([msg])
    
    def test_packet_contains_two_messages(self):
        """Test that when a packet contains more than one message
            the second one is not discared."""
        msg1 = '{"request": "mock", "data": "somedata"}\n'
        msg2 = '{"request": "mock", "data": "seconddata"}\n'
        self.__request.push(msg1 + msg2)
        
        self.__protocol_handler.handle()
        
        msg1 = {'code': 200,
               'data': {'data': 'somedata', 'request': 'mock'},
               'response': 'mock'}
        
        msg2 = {'code': 200,
                'data': {'data': 'seconddata', 'request': 'mock'},
                'response': 'mock'}
        self.assert_responses([msg1, msg2])
    
    def test_message_invalid_json(self):
        """Test that the handler does the correct thing when invalid json
           is encountered"""
        self.__request.push('ceci ne pas le json\n')
        
        self.__protocol_handler.handle()
        
        msg = {'code': 400,
               'msg': 'Invalid request',
               'original-request': 'ceci ne pas le json',
               'response': 'error'}
        self.assert_responses([msg])
    
    def test_message_does_not_contain_request(self):
        """Test that the handler sends error message when the request
           does not contain a request field"""
        self.__request.push('{"no-request": "mock", "data": "somedata"}\n')
        
        self.__protocol_handler.handle()
        
        msg = {'code': 400,
               'msg': 'Missing request',
               'response': 'error',
               'original-request': {"no-request": "mock", "data": "somedata"}}
        self.assert_responses([msg])
    
    def test_message_invalid_request(self):
        """Message includes invalid request, send error message."""
        self.__request.push('{"request": "notAllowed", "data": "somedata"}\n')
        
        self.__protocol_handler.handle()
        
        msg = {'code': 405,
               'msg': 'Method not allowed',
               'response': 'notAllowed',
               'original-request': {"request": "notAllowed", "data": "somedata"}}
        self.assert_responses([msg])
        
    
if __name__ == '__main__':
    unittest.main()
else:
    def suite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestProtocolHandler)
