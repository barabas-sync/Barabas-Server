import unittest
import datetime
import io
import storm.locals

from server.identity.user import User
from server.storage.syncedfile import SyncedFile
import server.test.storage.mocks.storage
from server.storage.errors import NotSavedError

class TestSyncedFile(unittest.TestCase):
    def setUp(self):
        self.__database = server.database.sqlitedatabase.SQLiteDatabase(":memory:")
        self.__database.install('server/database/sql/sqlite/v1.sql')
        self.__database.install('server/database/sql/sqlite/v2.sql')
        self.__fileManager = server.test.storage.mocks.storage.StringIOStorage()
        self.__user1 = User(u'Nathan', u'Samson', u'email@ameil.com')
        self.__user2 = User(u'Other', u'User', u'email2@email.com')
    
    def tearDown(self):
        self.__database.close()    
    
    def testCreate(self):
        file = SyncedFile("afilename.txt", self.__user1)
        self.assertEqual("afilename.txt", file.fileName)
        self.__database.add(file)

        sf = self.__database.find(SyncedFile, SyncedFile.fileName == u"afilename.txt").one()
        self.assertEqual(sf.owner, self.__user1)
        
    def testCreateNameCollision(self):
        file1 = SyncedFile("readme.txt", self.__user1) # Readme for project X
        self.__database.add(file1)
        self.__database.flush()
        file1.tag("Project X")
        
        file2 = SyncedFile("readme.txt", self.__user1) # Readme for project Y
        self.__database.add(file2)
        file2.tag("Project Y")
        
        self.assertNotEqual(file1.ID, file2.ID)
    
    def testTag(self):
        file1 = SyncedFile("someFunnyFile.png", self.__user1)
        self.__database.add(file1)
        self.__database.flush()
        file1.tag("Cartoon")
        file1.tag("Funny")
        
        file1Copy = self.__database.find(SyncedFile, SyncedFile.fileName == u'someFunnyFile.png').one()
        tags = file1Copy.tags()

        self.assertTrue("Cartoon" in tags)
        self.assertTrue("Funny" in tags)
        
        file1Copy.tag("Humour")
        self.assertTrue("Humour" in file1Copy.tags())
    
    def testTagBeforeSave(self):
        file1 = SyncedFile("someFile.png", self.__user1)
        file1.tag("Some-Tag")
    
    def testUntag(self):
        file1 = SyncedFile("someFile", self.__user1)
        self.__database.add(file1)
        
        file1.tag("Some-Tag")
        
        self.assertEquals(["Some-Tag"], file1.tags())
        file1.untag("Some-Tag")
        self.assertEquals([], file1.tags())
    
    def testUntagTwice(self):
        (aFile, bFile) = self._insertCommonData()
        
        aFile.untag("Work")
        aFile.untag("Work")
        self.assertEquals(["Project X", "TODO"], aFile.tags())
        self.assertEquals(["Work"], bFile.tags())
    
    def testTagTwice(self):
        (aFile, bFile) = self._insertCommonData()
        aFile.tag("Work")
        
        self.assertEquals(["Project X", "TODO", "Work"], aFile.tags())
        self.assertEquals(["Work"], bFile.tags())

    def testFindFilesWithOneTag(self):
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"Work", ))]
        fileNames.sort()
        self.assertEqual([u"aFileName", u"bFileName"], fileNames)
    
    def testFindFilesWithMoreTags(self):
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"Work", u"Project X"))]
        fileNames.sort()
        self.assertEqual(["aFileName"], fileNames)
    
    def testFindFilesWithTags(self):
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"TODO", u"Project X"))]
        fileNames.sort()
        self.assertEqual(["aFileName"], fileNames)
    
    def testVersions(self):
        file1 = SyncedFile("versionedfile", self.__user1)
        self.__database.add(file1)
        
        self.assertEquals(0, file1.versions.count())
        
        editTime = datetime.datetime(2009, 10,11, 12, 13, 14)
        inputFile = io.StringIO("This is the first version of the file")
        fileVersion = self.__fileManager.create(inputFile, editTime)
        file1.versions.add(fileVersion)
        self.__database.flush()
        inputFile.close()
        
        firstVersion = file1.versions.order_by(server.storage.fileversion.FileVersion.timeEdited).first()
        
        self.assertEqual(firstVersion.timeEdited, editTime)
        # TODO: use this test with python 3.2?
        #self.assertLessEqual((datetime.datetime.now() - firstVersion.timeStored()).total_seconds(), 2)
        
        filed = firstVersion.open(self.__fileManager)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        inputFile = io.StringIO("This is the second version of the file")
        fileVersion = self.__fileManager.create(inputFile, editTime)
        file1.versions.add(fileVersion)
        self.__database.flush()
        inputFile.close()
        
        (firstVersion, secondVersion) = file1.versions.order_by(server.storage.fileversion.FileVersion.timeEdited)
        filed = secondVersion.open(self.__fileManager)
        self.assertEqual("This is the second version of the file", filed.read())
        filed.close()
        
        filed = firstVersion.open(self.__fileManager)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        
    def testStoreFile(self):
        syncedFile = SyncedFile("aFileName", self.__user1)
        self.__database.add(syncedFile)
        self.__database.flush()
        
        editTime = datetime.datetime(1911, 11, 11, 11, 11, 11)
        inputFile = io.StringIO("Some String IO")
        version1 = self.__fileManager.create(inputFile, editTime)
        syncedFile.versions.add(version1)
        self.__database.flush()
        inputFile.close()
        
        inputFile2 = io.StringIO("Some Other String IO")
        editTime2 = datetime.datetime(2000, 11, 11, 11, 11, 11)
        version2 = self.__fileManager.create(inputFile2, editTime2)
        syncedFile.versions.add(version2)
        self.__database.flush()
        inputFile2.close()
        
        (version1X, version2X) = syncedFile.versions
        
        self.assertEqual(version1X.timeEdited, version1.timeEdited)
        self.assertEqual(version1X.timeStored, version1.timeStored)
        self.assertEqual(version1X.ID, version1.ID)
        self.assertEqual(version1X.filePointer, version1.filePointer)
        filedata = version1X.open(self.__fileManager)
        self.assertEqual("Some String IO", filedata.read())
        filedata.close()
        
        self.assertNotEqual(version1X.ID, version2X.ID)        
    
    def _insertCommonData(self):
        aFile = SyncedFile("aFileName", self.__user1)
        self.__database.add(aFile)

        bFile = SyncedFile("bFileName", self.__user1)
        self.__database.add(bFile)
        
        cFile = SyncedFile("cFileName", self.__user2)
        self.__database.add(cFile)

        aFile.tag(u"TODO")
        aFile.tag(u"Work")
        aFile.tag(u"Project X")

        bFile.tag(u"Work")
        
        cFile.tag(u"TODO")
        cFile.tag(u"Project X")

        return (aFile, bFile)

if __name__ == '__main__':
    unittest.main()
else:
    def TestSuite():
        return unittest.TestLoader().loadTestsFromTestCase(TestSyncedFile)
