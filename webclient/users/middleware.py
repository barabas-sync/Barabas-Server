import webserver
from  lib.identity.user import User
from lib.identity.passwordauthentication import PasswordAuthentication

class AuthenticationMiddleware:
    def process_request(self, request):
        if (request.session and 'userid' in request.session):
            db = webserver.WebServer.database()
            request.user = db.find(User, User.id == request.session['userid']).one()
        else:
            request.user = None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    
    def process_response(self, request, response):
        return response
    
    def process_exception(self, request, exception):
        return None
