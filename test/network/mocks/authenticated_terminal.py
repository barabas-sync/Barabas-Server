# vim: set expandtab set ts=4 tw=4

class AuthenticatedTerminal():
    def __init__(self, server, user):
        self.__server = server
        self.__user = user

    def server(self):
        return self.__server

    def user(self):
        return self.__user
