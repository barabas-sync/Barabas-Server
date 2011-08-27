import unittest
import datetime
import io

import barabas.database.sqldatabase
from barabas.identity.user import User
from barabas.objects.syncedfile import SyncedFile
from barabas.objects.syncedfileversion import SyncedFileVersion

import mocks.storage

class TestSyncedFile(unittest.TestCase):
    def setUp(self):
        """Empty docstring"""
        self.__database = barabas.database.sqldatabase.create_sqlite_use_only_for_tests().new_store()
        self.__database.install('deploy/sqlite/latest.sql')
        self.__fileManager = mocks.storage.StringIOStorage()
        self.__storage = self.__fileManager
        self.__user1 = User(u'Nathan', u'Samson', u'email@ameil.com')
        self.__user2 = User(u'Other', u'User', u'email2@email.com')

	def tearDown(self):
		"""Empty docstring"""
		self.__database.close()        
    
    def testCreate(self):
        """Empty docstring"""
        file = SyncedFile("afilename.txt", self.__user1)
        self.assertEqual("afilename.txt", file.fileName)
        self.__database.add(file)

        sf = self.__database.find(SyncedFile, SyncedFile.fileName == u"afilename.txt").one()
        self.assertEqual(sf.owner, self.__user1)
        
    def testCreateNameCollision(self):
        """Empty docstring"""
        file1 = SyncedFile("readme.txt", self.__user1) # Readme for project X
        self.__database.add(file1)
        self.__database.flush()
        file1.tag("Project X")
        
        file2 = SyncedFile("readme.txt", self.__user1) # Readme for project Y
        self.__database.add(file2)
        file2.tag("Project Y")
        
        self.assertNotEqual(file1.ID, file2.ID)
    
    def testTag(self):
        """Empty docstring"""
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
        """Empty docstring"""
        file1 = SyncedFile("someFile.png", self.__user1)
        file1.tag("Some-Tag")
    
    def testUntag(self):
        """Empty docstring"""
        file1 = SyncedFile("someFile", self.__user1)
        self.__database.add(file1)
        
        file1.tag("Some-Tag")
        
        self.assertEquals(["Some-Tag"], file1.tags())
        file1.untag("Some-Tag")
        self.assertEquals([], file1.tags())
    
    def testUntagTwice(self):
        """Empty docstring"""
        (aFile, bFile) = self._insertCommonData()
        
        aFile.untag("Work")
        aFile.untag("Work")
        self.assertEquals(["Project X", "TODO"], aFile.tags())
        self.assertEquals(["Work"], bFile.tags())
    
    def testTagTwice(self):
        """Empty docstring"""
        (aFile, bFile) = self._insertCommonData()
        aFile.tag("Work")
        
        self.assertEquals(["Project X", "TODO", "Work"], aFile.tags())
        self.assertEquals(["Work"], bFile.tags())

    def testFindFilesWithOneTag(self):
        """Empty docstring"""
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"Work", ))]
        fileNames.sort()
        self.assertEqual([u"aFileName", u"bFileName"], fileNames)
    
    def testFindFilesWithMoreTags(self):
        """Empty docstring"""
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"Work", u"Project X"))]
        fileNames.sort()
        self.assertEqual(["aFileName"], fileNames)
    
    def testFindFilesWithTags(self):
        """Empty docstring"""
        self._insertCommonData()
        
        fileNames = [sf.fileName for sf in SyncedFile.findWithTags(self.__database, self.__user1, (u"TODO", u"Project X"))]
        fileNames.sort()
        self.assertEqual(["aFileName"], fileNames)
    
    def testVersions(self):
        """Empty docstring"""
        file1 = SyncedFile("versionedfile", self.__user1)
        self.__database.add(file1)
        
        self.assertEquals(0, file1.versions.count())
        
        inputFile = io.StringIO(u"This is the first version of the file")
        fileVersion = SyncedFileVersion(inputFile, u"Some Versions Name", 
                                        u"2009-10-11T12:13:14",
                                        self.__storage)
        file1.versions.add(fileVersion)
        self.__database.flush()
        inputFile.close()
        
        firstVersion = file1.versions.order_by(barabas.objects.syncedfileversion.SyncedFileVersion.timeEdited).one()
        
        self.assertEqual(firstVersion.timeEdited, u"2009-10-11T12:13:14")
        # TODO: use this test with python 3.2?
        #self.assertLessEqual((datetime.datetime.now() - firstVersion.timeStored()).total_seconds(), 2)
        
        filed = firstVersion.open(self.__fileManager)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        inputFile = io.StringIO(u"This is the second version of the file")
        fileVersion = SyncedFileVersion(inputFile, u"Some Other Versions Name", 
                                        u"2009-10-11T13:13:14",
                                        self.__storage)
        file1.versions.add(fileVersion)
        self.__database.flush()
        inputFile.close()
        
        (firstVersion, secondVersion) = file1.versions.order_by(barabas.objects.syncedfileversion.SyncedFileVersion.timeEdited)
        filed = secondVersion.open(self.__fileManager)
        self.assertEqual("This is the second version of the file", filed.read())
        filed.close()
        
        filed = firstVersion.open(self.__fileManager)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        
    def testStoreFile(self):
        """Empty docstring"""
        syncedFile = SyncedFile("aFileName", self.__user1)
        self.__database.add(syncedFile)
        self.__database.flush()
        
        inputFile = io.StringIO(u"Some String IO")
        version1 = SyncedFileVersion(inputFile, u"Some Versions Name",
                                     u"1911-11-11T11:11:11", self.__storage)
        syncedFile.versions.add(version1)
        self.__database.flush()
        inputFile.close()
        
        inputFile2 = io.StringIO(u"Some Other String IO")
        version2 = SyncedFileVersion(inputFile2, u"Some Other Versions Name", 
                                     u"2000-11-11T11:11:11", self.__storage)
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
        """Empty docstring"""
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
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestSyncedFile)
