# vim: set expandtab set ts=4 tw=4

"""Base class for several test cases"""

import unittest

from barabas.database.sqldatabase import create_sqlite_use_only_for_tests

class DatabaseTestCase(unittest.TestCase):
    """A test case that has a database store"""
    def setUp(self):
        """Setup function"""
        self.__database = create_sqlite_use_only_for_tests()
        self.store = self.__database.new_store()
        self.store.install('deploy/sqlite/latest.sql')
