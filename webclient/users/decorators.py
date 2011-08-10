from django.http import HttpResponseRedirect

class LoginRequired(object):
    def __init__(self, orig_func):
        """Empty docstring"""
        self.__orig_func = orig_func
    
    def __call__(self, *args, **kwargs):
        """Empty docstring"""
        if not args[0].user:
            return HttpResponseRedirect('/')
        return self.__orig_func(*args, **kwargs)
