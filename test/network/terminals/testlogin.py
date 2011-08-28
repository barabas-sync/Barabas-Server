# vim: set expandtab set ts=4 tw=4

"""Test case for the login terminal"""

import test.testcase

from barabas.network.terminals.base import ProtocolException
from barabas.network.terminals.login import Login as LoginTerminal

from barabas.identity.user import User
from barabas.identity.passwordauthentication import PasswordAuthentication

from test.network.mocks.server import MockServer
from test.network.mocks.authenticated_terminal import AuthenticatedTerminal

class TestLoginTerminal(test.testcase.DatabaseTestCase):
    """ Test case for the login terminal """
    def setUp(self):
        """Setup functions"""
        test.testcase.DatabaseTestCase.setUp(self)
        self.server = MockServer(store=self.store)
        self.terminal = LoginTerminal(self.server,
                                      authenticated_terminal=AuthenticatedTerminal)

        user1 = User(u"Me", u"Meme", u"me@meme.org")
        password1 = PasswordAuthentication()
        password1.user = user1
        password1.username = u"me.meme"
        password1.password("secure-password")
        self.store.add(user1)
        self.store.add(password1)
        self.user_me = user1

    def test_login_user_password(self):
        """Correct login"""
        request = {'request': 'login',
                   'login-module': 'user-password',
                   'module-info': {'username': u'me.meme',
                                   'password': 'secure-password'}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 200}
        self.assertEqual(expected_response, response)
        self.assertIsInstance(terminal, AuthenticatedTerminal)
        self.assertEqual(self.user_me, terminal.user())
        self.assertEqual(self.server, terminal.server())

    def test_incorrect_password(self):
        """Incorrect password"""
        request = {'request': 'login',
                   'login-module': 'user-password',
                   'module-info': {'username': u'me.meme',
                                   'password': 'wrong-password'}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 1000,
                             'msg': 'Wrong username or password'}
        self.assertEqual(expected_response, response)
        self.assertEqual(self.terminal, terminal)

    def test_incorrect_username(self):
        """Incorrect username"""
        request = {'request': 'login',
                   'login-module': 'user-password',
                   'module-info': {'username': u'no-exits',
                                   'password': 'secure-password'}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 1000,
                             'msg': 'Wrong username or password'}
        self.assertEqual(expected_response, response)
        self.assertEqual(self.terminal, terminal)

    def test_empty_username(self):
        """Test empty username. Github bug #6"""
        request = {'request': 'login',
                   'login-module': 'user-password',
                   'module-info': {'username': '',
                                   'password': 'secure-password'}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 1000,
                             'msg': 'Wrong username or password'}
        self.assertEqual(expected_response, response)
        self.assertEqual(self.terminal, terminal)

    def test_empty_password(self):
        """Test empty password."""
        request = {'request': 'login',
                   'login-module': 'user-password',
                   'module-info': {'username': 'me.meme',
                                   'password': ''}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 1000,
                             'msg': 'Wrong username or password'}
        self.assertEqual(expected_response, response)
        self.assertEqual(self.terminal, terminal)

    def test_incorrect_login_module(self):
        """Test login with incorrect login module"""
        request = {'request': 'login',
                   'login-module': 'non-exissting-module',
                   'module-info': {'username': 'me.meme',
                                   'password': ''}}
        (response, terminal) = self.terminal.login(request)

        expected_response = {'response': 'login',
                             'code': 405,
                             'msg': 'Login module not supported'}
        self.assertEqual(expected_response, response)
        self.assertEqual(self.terminal, terminal)

if __name__ == '__main__':
    unittest.main()
else:
    def suite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestLoginTerminal)
