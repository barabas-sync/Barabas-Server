# vim: set expandtab set ts=4 tw=4

"""Test case for the handshake terminal"""

import unittest

from barabas.network.terminals.base import ProtocolException
from barabas.network.terminals.handshake import Handshake as HandshakeTerminal
from barabas.network.terminals.login import Login as LoginTerminal

from test.network.mocks.server import MockServer

class TestHandshakeTerminal(unittest.TestCase):
    """ Test case for the handshake terminal """
    def setUp(self):
        """Setup functions"""
        self.server = MockServer()
        self.terminal = HandshakeTerminal(self.server)

    def test_correct_handshake(self):
        """A correct handshake"""

        request = {'request': 'handshake',
                   'version': 1,
                   'login-modules': ['user-password', 'some-other']}
        (response, terminal) = self.terminal.handshake(request)

        expected_response = {'response': 'handshake',
                             'code': 200,
                             'login-modules': ['user-password']}
        self.assertEqual(expected_response, response)
        self.assertIsInstance(terminal, LoginTerminal)

    def test_incorrect_version_handshake(self):
        """Handshake with incorrect version"""
        request = {'request': 'handshake',
                   'version': 3,
                   'login-modules': ['user-password', 'some-other']}
        with self.assertRaises(ProtocolException) as context_manager:
            self.terminal.handshake(request)

        self.assertEqual(505, context_manager.exception.code())
        self.assertEqual('Version not supported',
                         context_manager.exception.msg())

    def test_no_login_modules(self):
        """Handshake without login modules"""
        request = {'request': 'handshake',
                   'version': 1,
                   'login-modules': []}
        with self.assertRaises(ProtocolException) as context_manager:
            self.terminal.handshake(request)

        self.assertEqual(520, context_manager.exception.code())
        self.assertEqual('No matching login modules',
                         context_manager.exception.msg())

    def test_incompatible_login_modules(self):
        """Handshake with only incompatible login modules"""
        request = {'request': 'handshake',
                   'version': 1,
                   'login-modules': ['only-incompatible']}
        with self.assertRaises(ProtocolException) as context_manager:
            self.terminal.handshake(request)

        self.assertEqual(520, context_manager.exception.code())
        self.assertEqual('No matching login modules',
                         context_manager.exception.msg())

if __name__ == '__main__':
    unittest.main()
else:
    def suite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestHandshakeTerminal)
