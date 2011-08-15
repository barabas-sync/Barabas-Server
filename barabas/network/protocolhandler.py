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

import SocketServer
import json
import StringIO

from terminals.base import ProtocolException as ProtocolException
from terminals.handshake import Handshake as HandshakeTerminal

class ProtocolHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        """Empty docstring"""
        print "Opened connection with %s" % str(self.request.getpeername())
        self.__terminal = HandshakeTerminal(self.server)
        self.__running = True
        bfr = ""
        while self.__running:
            msg = bfr
            try:
                msg += self.request.recv(1024)
            
                while not msg.find("\n") > 0:
                    tmp = self.request.recv(1024)
                    if tmp == "":
                        self.__running = False
                        break
                    msg += tmp
                
                if not self.__running:
                    break
            
                (msg, bfr) = msg.split("\n", 1)
                
                print "Received %s from %s" % (msg, str(self.request.getpeername()))
                
                msgString = StringIO.StringIO(msg)
                try:
                    jsonRequest = json.load(msgString)
                    msgString.close()
                except:
                    msgString.close()
                    response = {}
                    response['response'] = 'error'
                    response['code'] = base.Base.BAD_REQUEST
                    response['msg'] = 'Invalid request'
                    self.__send(response)
                    continue
            except Exception, e:
                print e
                self.__running = False
            
            try:
                if hasattr(self.__terminal, jsonRequest['request']):
                    fnc = getattr(self.__terminal, jsonRequest['request'])
                    (response, self.__terminal) = fnc(jsonRequest)
                    self.server.get_database_store().commit()
                    self.__send(response)
                else:
                    raise ProtocolException(terminals.base.Base.METHOD_NOT_ALLOWED, 'Method not allowed')
            except ProtocolException, ex:
                response = {}
                response['response'] = 'error'
                response['code'] = ex.code()
                response['msg'] = ex.msg()
                response['original-request'] = jsonRequest
                self.__send(response)
        self.__terminal.stop()
        print "Closed connection with %s:%s" % self.request.getpeername()
    
    def __send(self, response):
        """Empty docstring"""
        responseIO = StringIO.StringIO()
        json.dump(response, responseIO)
        self.request.send(responseIO.getvalue() + "\n")
