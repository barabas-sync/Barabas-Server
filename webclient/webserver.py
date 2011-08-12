import sys
sys.path.append('..')

from barabas.database.sqldatabase import create_postgresql
from barabas.simplestoragemanager import SimpleStorageManager

class WebServer:
    __database = None
    __storage = None
    __store = None
    
    class Callable:
        def __init__(self, call):
            """Empty docstring"""
            self.__call__ = call
    

    @classmethod
    def database(cls):
        """Empty docstring"""
        if (cls.__database == None):
            cls.__database = PostgreSQL(hostname='localhost',
                                        username='barabas',
                                        database_name='barabasdb',
                                        password='barabaspw')
            cls.__store = cls.__database.new_store()
        return cls.__store
    
    @classmethod
    def storage(cls):
        """Empty docstring"""
        if (WebServer.__storage == None):
            WebServer.__storage = SimpleStorageManager("../datafiles/")
        return WebServer.__storage
