import unittest

import barabas.database.sqldatabase

from barabas.identity.user import User

class TestUser(unittest.TestCase):
    def testCreateUser(self):
        """Empty docstring"""
        return
        user = self.__database.createUser("Nathan", "Samson", "anemail@email.com")
        self.assertEquals("anemail@email.com", user.email())
        self.assertEquals("Nathan", user.firstName())
        self.assertEquals("Samson", user.lastName())
        self.assertNotEquals(None, user.uniqueID())
        self.assertEquals(None, user.lastLoginTime())
        self.assertEquals(datetime.date.today(), user.registrationDate())
        
        userCopy = self.__database.getUser(user.uniqueID())
        self.assertEquals("anemail@email.com", userCopy.email())
        self.assertEquals("Nathan", userCopy.firstName())
        self.assertEquals("Samson", userCopy.lastName())
        self.assertEquals(user.uniqueID(), userCopy.uniqueID())
        self.assertEquals(None, user.lastLoginTime())
        self.assertEquals(datetime.date.today(), userCopy.registrationDate())
        
        user2 =  self.__database.createUser("Other", "User", "otheremail@email.com")
        self.assertNotEquals(userCopy.uniqueID(), user2.uniqueID())
    
    def testCreateUserWithExistingEmail(self):
        """Empty docstring"""
        return
        user = self.__database.createUser("Nathan", "Samson", "anemail@email.com")
        
        self.assertRaises(server.identity.user.EmailInUseError, 
                          self.__database.createUser, "Other", "User", "anemail@email.com")
    
    def testUserLogin(self):
        """Empty docstring"""
        return
        user = self.__database.createUser("Nathan", "Samson", "email@email.com")
        self.assertEquals(None, user.lastLoginTime())
        
        user.login()
        user = self.__database.getUser(user.uniqueID())
        # TODO: Enable test
        #self.assertLessEqual((user.lastLoginDate() - datetime.datetime.now).total_seconds(), 2)
    
        self.assertNotEquals(None, user.lastLoginTime())

    def setUp(self):
        """Empty docstring"""
        self.__database = barabas.database.sqldatabase.create_sqlite_use_only_for_tests().new_store()
        self.__database.install('deploy/sqlite/latest.sql')

    def tearDown(self):
        """Empty docstring"""
        self.__database.close()

if __name__ == '__main__':
    unittest.main()
else:
    def TestSuite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestUser)
