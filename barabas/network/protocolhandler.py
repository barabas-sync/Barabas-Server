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

"""Protocol handler class"""

import SocketServer
import json
import StringIO

from barabas.network.terminals.base import ProtocolException
from barabas.network.terminals.base import Base as BaseTerminal
from barabas.network.terminals.handshake import Handshake as HandshakeTerminal

class ProtocolHandler(SocketServer.BaseRequestHandler):
    """The protocol handler. It receives messages, and send them to the
       correct terminal. The terminal formulates an answer and
       the protocol handler sends it back to the client.
    """
    #pylint:disable-msg=W0201
    # The warnings is about not defining self.__X variables in __init__
    # Overriding __init__ for this class seems to be a bad idea, so we
    # define them in the setup() method.

    start_terminal = HandshakeTerminal

    def setup(self):
        """Setup function"""
        self.__start_terminal = ProtocolHandler.start_terminal
        self.__terminal = None
        self.__running = False
        self.__buffer = ""

    def handle(self):
        """Empty docstring"""
        print "Opened connection with %s" % str(self.request.getpeername())
        self.__terminal = self.__start_terminal(self.server)
        self.__running = True
        while self.__running:
            msg = self.__read_message()
            if (self.__running == False):
                break
            
            print "Received %s from %s" % (msg,
                                           str(self.request.getpeername()))
                
            msg_io = StringIO.StringIO(msg)
            try:
                json_request = json.load(msg_io)
            except ValueError:
                response = {}
                response['response'] = 'error'
                response['code'] = BaseTerminal.BAD_REQUEST
                response['msg'] = 'Invalid request'
                response['original-request'] = msg
                self.__send(response)
                continue
            finally:
                msg_io.close()
            
            try:
                if ('request' not in json_request):
                    raise ProtocolException(BaseTerminal.BAD_REQUEST,
                                            'Missing request')
            
                if hasattr(self.__terminal, json_request['request']):
                    fnc = getattr(self.__terminal, json_request['request'])
                    (response, self.__terminal) = fnc(json_request)
                    self.server.get_database_store().commit()
                    self.__send(response)
                else:
                    response = {}
                    response['response'] = json_request['request']
                    response['code'] = BaseTerminal.METHOD_NOT_ALLOWED
                    response['msg'] = 'Method not allowed'
                    response['original-request'] = json_request
                    self.__send(response)
            except ProtocolException, ex:
                response = {}
                response['response'] = 'error'
                response['code'] = ex.code()
                response['msg'] = ex.msg()
                response['original-request'] = json_request
                self.__send(response)
        self.__terminal.stop()
        print "Closed connection with %s:%s" % self.request.getpeername()
    
    def __read_message(self):
        """Reads a message from the socket"""
        msg = self.__buffer

        while not msg.find("\n") > 0:
            tmp = self.request.recv(1024)
            if tmp == "":
                self.__running = False
                break
            msg += tmp

        if (self.__running == False):
            return

        (msg, self.__buffer) = msg.split("\n", 1)
        return msg

    def __send(self, response):
        """Empty docstring"""
        response_io = StringIO.StringIO()
        json.dump(response, response_io)
        self.request.send(response_io.getvalue() + "\n")
