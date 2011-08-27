# vim: set expandtab set ts=4 tw=4

import unittest
import io

from barabas.database.sqldatabase import create_sqlite_use_only_for_tests
from barabas.identity.user import User
from barabas.objects.syncedfile import SyncedFile
from barabas.objects.syncedfileversion import SyncedFileVersion

import mocks.storage

class TestSyncedFile(unittest.TestCase):
    def setUp(self):
        """Empty docstring"""
        self.__database = create_sqlite_use_only_for_tests().new_store()
        self.__database.install('deploy/sqlite/latest.sql')
        self.__storage = mocks.storage.StringIOStorage()
        self.__user1 = User(u'Nathan', u'Samson', u'email@ameil.com')
        self.__user2 = User(u'Other', u'User', u'email2@email.com')

    def tearDown(self):
        """Empty docstring"""
        self.__database.close()        

    def test_create(self):
        """Empty docstring"""
        a_file = SyncedFile("afilename.txt", self.__user1)
        self.assertEqual("afilename.txt", a_file.fileName)
        self.__database.add(a_file)

        sf = self.__database.find(SyncedFile,
                SyncedFile.fileName == u"afilename.txt").one()
        self.assertEqual(sf.owner, self.__user1)
        
    def test_create_name_collision(self):
        """Empty docstring"""
        file1 = SyncedFile("readme.txt", self.__user1) # Readme for project X
        self.__database.add(file1)
        self.__database.flush()
        file1.tag("Project X")
        
        file2 = SyncedFile("readme.txt", self.__user1) # Readme for project Y
        self.__database.add(file2)
        file2.tag("Project Y")
        
        self.assertNotEqual(file1.ID, file2.ID)
    
    def test_tag(self):
        """Empty docstring"""
        file1 = SyncedFile("someFunnyFile.png", self.__user1)
        self.__database.add(file1)
        self.__database.flush()
        file1.tag("Cartoon")
        file1.tag("Funny")
        
        file1_copy = self.__database.find(SyncedFile,
                SyncedFile.fileName == u'someFunnyFile.png').one()
        tags = file1_copy.tags()

        self.assertTrue("Cartoon" in tags)
        self.assertTrue("Funny" in tags)
        
        file1_copy.tag("Humour")
        self.assertTrue("Humour" in file1_copy.tags())
    
    def test_tag_before_save(self):
        """Empty docstring"""
        file1 = SyncedFile("someFile.png", self.__user1)
        file1.tag("Some-Tag")
    
    def test_untag(self):
        """Empty docstring"""
        file1 = SyncedFile("someFile", self.__user1)
        self.__database.add(file1)
        
        file1.tag("Some-Tag")
        
        self.assertEquals(["Some-Tag"], file1.tags())
        file1.untag("Some-Tag")
        self.assertEquals([], file1.tags())
    
    def test_untag_twice(self):
        """Empty docstring"""
        (file_a, file_b) = self._insert_common_data()
        
        file_a.untag("Work")
        file_a.untag("Work")
        self.assertEquals(["Project X", "TODO"], file_a.tags())
        self.assertEquals(["Work"], file_b.tags())
    
    def test_tag_twice(self):
        """Empty docstring"""
        (file_a, file_b) = self._insert_common_data()
        file_a.tag("Work")
        
        self.assertEquals(["Project X", "TODO", "Work"], file_a.tags())
        self.assertEquals(["Work"], file_b.tags())

    def test_find_files_with_one_tag(self):
        """Empty docstring"""
        self._insert_common_data()
        
        file_names = [sf.fileName for sf in
                SyncedFile.findWithTags(self.__database,
                                        self.__user1, (u"Work", ))]
        file_names.sort()
        self.assertEqual([u"aFileName", u"bFileName"], file_names)
    
    def test_find_files_with_more_tags(self):
        """Empty docstring"""
        self._insert_common_data()
        
        file_names = [sf.fileName for sf in
                SyncedFile.findWithTags(self.__database,
                                        self.__user1, (u"Work", u"Project X"))]
        file_names.sort()
        self.assertEqual(["aFileName"], file_names)
    
    def test_find_files_with_tags(self):
        """Empty docstring"""
        self._insert_common_data()
        
        file_names = [sf.fileName for sf in
                SyncedFile.findWithTags(self.__database,
                                        self.__user1, (u"TODO", u"Project X"))]
        file_names.sort()
        self.assertEqual(["aFileName"], file_names)
    
    def test_versions(self):
        """Empty docstring"""
        file1 = SyncedFile("versionedfile", self.__user1)
        self.__database.add(file1)
        
        self.assertEquals(0, file1.versions.count())
        
        input_file = io.StringIO(u"This is the first version of the file")
        file_version = SyncedFileVersion(input_file, u"Some Versions Name", 
                                        u"2009-10-11T12:13:14",
                                        self.__storage)
        file1.versions.add(file_version)
        self.__database.flush()
        input_file.close()
        
        versions = file1.versions.order_by(SyncedFileVersion.timeEdited)
        first_version = versions.one()
        
        self.assertEqual(first_version.timeEdited, u"2009-10-11T12:13:14")
        # TODO: use this test with python 3.2?
        #self.assertLessEqual((datetime.datetime.now() - 
        #       first_version.timeStored()).total_seconds(), 2)
        
        filed = first_version.open(self.__storage)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        input_file = io.StringIO(u"This is the second version of the file")
        file_version = SyncedFileVersion(input_file, u"Some Other Name", 
                                        u"2009-10-11T13:13:14",
                                        self.__storage)
        file1.versions.add(file_version)
        self.__database.flush()
        input_file.close()
        
        (first_version, second_version) = \
                file1.versions.order_by(SyncedFileVersion.timeEdited)
        filed = second_version.open(self.__storage)
        self.assertEqual("This is the second version of the file", filed.read())
        filed.close()
        
        filed = first_version.open(self.__storage)
        self.assertEqual("This is the first version of the file", filed.read())
        filed.close()
        
        
    def test_store_file(self):
        """Empty docstring"""
        synced_file = SyncedFile("aFileName", self.__user1)
        self.__database.add(synced_file)
        self.__database.flush()
        
        input_file = io.StringIO(u"Some String IO")
        version1 = SyncedFileVersion(input_file, u"Some Versions Name",
                                     u"1911-11-11T11:11:11", self.__storage)
        synced_file.versions.add(version1)
        self.__database.flush()
        input_file.close()
        
        input_file2 = io.StringIO(u"Some Other String IO")
        version2 = SyncedFileVersion(input_file2, u"Some Other Versions Name", 
                                     u"2000-11-11T11:11:11", self.__storage)
        synced_file.versions.add(version2)
        self.__database.flush()
        input_file2.close()
        
        (version_1x, version_2x) = synced_file.versions
        
        self.assertEqual(version_1x.timeEdited, version1.timeEdited)
        self.assertEqual(version_1x.timeStored, version1.timeStored)
        self.assertEqual(version_1x.ID, version1.ID)
        self.assertEqual(version_1x.filePointer, version1.filePointer)
        filedata = version_1x.open(self.__storage)
        self.assertEqual("Some String IO", filedata.read())
        filedata.close()
        
        self.assertNotEqual(version_1x.ID, version_2x.ID)        
    
    def _insert_common_data(self):
        """Empty docstring"""
        file_a = SyncedFile("aFileName", self.__user1)
        self.__database.add(file_a)

        file_b = SyncedFile("bFileName", self.__user1)
        self.__database.add(file_b)
        
        file_c = SyncedFile("cFileName", self.__user2)
        self.__database.add(file_c)

        file_a.tag(u"TODO")
        file_a.tag(u"Work")
        file_a.tag(u"Project X")

        file_b.tag(u"Work")
        
        file_c.tag(u"TODO")
        file_c.tag(u"Project X")

        return (file_a, file_b)

if __name__ == '__main__':
    unittest.main()
else:
    def TestSuite():
        """Empty docstring"""
        return unittest.TestLoader().loadTestsFromTestCase(TestSyncedFile)
