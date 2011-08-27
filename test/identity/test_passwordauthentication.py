import unittest

import barabas.database.sqldatabase

from barabas.identity.passwordauthentication import PasswordAuthentication
from barabas.identity.user import User

class TestPasswordAuth(unittest.TestCase):
    def testStorePasswordAuth(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        pa = self.__database.find(PasswordAuthentication, PasswordAuthentication.username == u'nathan').one()
        self.assertTrue(pa.testPassword("theSuperHardPassword"))
        self.assertFalse(pa.testPassword("theSuperWrongPassword"))
    
    def testChangePassword(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        pa.password("theNewPassword")
        self.assertTrue(pa.testPassword("theNewPassword"))
        self.assertFalse(pa.testPassword("theSuperHardPassword"))
    
    def testRequestReset(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        hsh = pa.requestReset()
        self.assertTrue(pa.isResetHash(hsh))
        self.assertFalse(pa.isResetHash("...."))
        self.assertTrue(pa.testPassword("theSuperHardPassword"))
    
    def testReset(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        hsh = pa.requestReset()
        pa.reset(hsh, "newPassword")
        self.assertTrue(pa.testPassword("newPassword"))
    
    def testResetWithWrongHash(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        hsh = pa.requestReset()
        self.assertRaises(Exception, pa.reset, "wrong hash", "newPassword")
        self.assertFalse(pa.testPassword("newPass"))
    
    def testResetWithNoRequest(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathan'
        pa.user = self.__user
        pa.password("theSuperHardPassword")
        self.__database.add(pa)
        
        self.assertRaises(Exception, pa.reset, None, "newPass")
        self.assertFalse(pa.testPassword("newPass"))
    
    def testStorePassword(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.username = u'nathansamson'
        pa.password("mePassword")
        self.__database.add(pa)
        self.__database.flush()
        
        pa = self.__database.find(PasswordAuthentication, PasswordAuthentication.username == u"nathansamson").one()
        self.assertTrue(pa.testPassword("mePassword"))
    
    def testSavePassword(self):
        """Empty docstring"""
        pa = PasswordAuthentication()
        pa.user = self.__user
        pa.username = u'nathansamson'
        pa.password("mePassword")
        self.__database.add(pa)
        
        pa = self.__database.find(PasswordAuthentication, PasswordAuthentication.username == u"nathansamson").one()
        hsh = pa.requestReset()
        self.__database.flush()
        
        pa = self.__database.find(PasswordAuthentication, PasswordAuthentication.username == u"nathansamson").one()
        pa.reset(hsh, "newPassword")
        self.__database.flush()
        
        pa = self.__database.find(PasswordAuthentication, PasswordAuthentication.username == u"nathansamson").one()
        self.assertTrue(pa.testPassword("newPassword"))
    
    def setUp(self):
        """Empty docstring"""
        self.__database = barabas.database.sqldatabase.create_sqlite_use_only_for_tests().new_store()
        self.__database.install('deploy/sqlite/latest.sql')
        self.__user = User(u'Nathan', u'Samson', u'anemail@company.com')
    
    def tearDown(self):
        """Empty docstring"""
        self.__database.close()
    
if __name__ == '__main__':
    unittest.main()
else:
    def TestSuite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestPasswordAuth)
