import unittest
import server.database.sqlitedatabase

from server.identity.user import User

class TestUser(unittest.TestCase):
    def testCreateUser(self):
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
        return
        user = self.__database.createUser("Nathan", "Samson", "anemail@email.com")
        
        self.assertRaises(server.identity.user.EmailInUseError, 
                          self.__database.createUser, "Other", "User", "anemail@email.com")
    
    def testUserLogin(self):
        return
        user = self.__database.createUser("Nathan", "Samson", "email@email.com")
        self.assertEquals(None, user.lastLoginTime())
        
        user.login()
        user = self.__database.getUser(user.uniqueID())
        # TODO: Enable test
        #self.assertLessEqual((user.lastLoginDate() - datetime.datetime.now).total_seconds(), 2)
    
        self.assertNotEquals(None, user.lastLoginTime())

if __name__ == '__main__':
    unittest.main()
else:
    def TestSuite():
        return unittest.TestLoader().loadTestsFromTestCase(TestUser)
