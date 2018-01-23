from __future__ import absolute_import
from __future__ import unicode_literals

import io
import json
import unittest

import six
from fs import ResourceType
from fs import errors
# from fs.opener import open_fs
from fs.youtube import YoutubeFS
from six import text_type


class TestYoutubeFS(unittest.TestCase):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/playlist?list=PLYlZ5VtcfgitfPyMGkZsYkhLm-eOZeQpY'
        self.url = url
        return YoutubeFS(url)

    @classmethod
    def destroy_fs(self, fs):
        """
        Destroy a FS object.

        :param fs: A FS instance previously opened by
            `~fs.test.FSTestCases.make_fs`.

        """
        fs.close()

    def setUp(self):
        self.fs = self.make_fs()

    def tearDown(self):
        self.destroy_fs(self.fs)
        del self.fs

    def assert_exists(self, path):
        """Assert a path exists.

        Arguments:
            path (str): A path on the filesystem.

        """
        self.assertTrue(self.fs.exists(path))

    def assert_not_exists(self, path):
        """Assert a path does not exist.

        Arguments:
            path (str): A path on the filesystem.

        """
        self.assertFalse(self.fs.exists(path))

    def assert_isfile(self, path):
        """Assert a path is a file.

        Arguments:
            path (str): A path on the filesystem.

        """
        self.assertTrue(self.fs.isfile(path))

    def assert_isdir(self, path):
        """Assert a path is a directory.

        Arguments:
            path (str): A path on the filesystem.

        """
        self.assertTrue(self.fs.isdir(path))

    def assert_bytes(self, path, contents):
        """Assert a file contains the given bytes.

        Arguments:
            path (str): A path on the filesystem.
            contents (bytes): Bytes to compare.

        """
        assert isinstance(contents, bytes)
        data = self.fs.getbytes(path)
        self.assertEqual(data, contents)
        self.assertIsInstance(data, bytes)

    def assert_text(self, path, contents):
        """Assert a file contains the given text.

        Arguments:
            path (str): A path on the filesystem.
            contents (str): Text to compare.

        """
        assert isinstance(contents, text_type)
        with self.fs.open(path, 'rt') as f:
            data = f.read()
        self.assertEqual(data, contents)
        self.assertIsInstance(data, text_type)

    def test_listdir(self):
        # Check listing directory that doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.listdir('foobar')

        # Check aliases for root
        filelist = self.fs.listdir('/')
        self.assertEqual(self.fs.listdir('.'), filelist)
        self.assertEqual(self.fs.listdir('./'), filelist)

        six.assertCountEqual(self,
                             self.fs.listdir('./'),
                             filelist)

        # Check paths are unicode strings
        for name in self.fs.listdir('/'):
            self.assertIsInstance(name, text_type)

        with self.assertRaises(errors.DirectoryExpected):
            self.fs.listdir('/%s' % filelist[0])

    def test_str(self):
        self.assertIsInstance(self.fs.__str__(), text_type)

    def test_getinfo(self):
        # Test special case of root directory
        # Root directory has a name of ''
        root_info = self.fs.getinfo('/')
        self.assertEqual(root_info.name, '')
        self.assertTrue(root_info.is_dir)

        # Take an existing file
        testfile = self.fs.listdir(u'/')[0]

        # Check basic namespace
        info = self.fs.getinfo(testfile).raw
        self.assertIsInstance(info['basic']['name'], text_type)
        self.assertEqual(info['basic']['name'], testfile)
        self.assertFalse(info['basic']['is_dir'])

        # Get the info
        info = self.fs.getinfo(testfile, namespaces=['details']).raw
        self.assertIsInstance(info, dict)
        # self.assertEqual(info['details']['size'], 3)
        self.assertEqual(info['details']['type'], int(ResourceType.file))

        # Test getdetails
        self.assertEqual(info, self.fs.getdetails(testfile).raw)

        # Raw info should be serializable
        json.dumps(info)

        # Non existant namespace is not an error
        no_info = self.fs.getinfo(testfile, '__nosuchnamespace__').raw
        self.assertIsInstance(no_info, dict)
        self.assertEqual(
            no_info['basic'],
            {'name': testfile, 'is_dir': False}
        )

        # Check a number of standard namespaces
        # FS objects may not support all these, but we can at least
        # invoke the code
        self.fs.getinfo(testfile, namespaces=['access', 'stat', 'details'])

        mediainfo = self.fs.getinfo(testfile, 'mediaproxy.media').raw
        self.assertEqual(
            mediainfo['mediaproxy.media']['type'],
            'video'
        )

        with self.assertRaises(errors.ResourceNotFound):
            self.fs.getinfo('__notexists__')


    def test_openbin(self):
        testfile = self.fs.listdir(u'/')[0]

        # Read a binary file
        with self.fs.openbin(testfile, 'rb') as read_file:
            repr(read_file)
            text_type(read_file)
            self.assertIsInstance(read_file, io.IOBase)
            self.assertTrue(read_file.readable())
            self.assertFalse(read_file.writable())
            self.assertFalse(read_file.closed)
            self.assertTrue(read_file.seekable())

            data = read_file.read(100)
            read_file.seek(10)
            assert read_file.tell() == 10
            data_part = read_file.read(90)
            read_file.seek(-10, whence=1)
            assert read_file.tell() == 90
            with self.assertRaises(errors.Unsupported):
                read_file.seek(10, whence=2)
            with self.assertRaises(errors.Unsupported):
                read_file.seek(10, whence=10)

        # Test Close
        tfo = self.fs.openbin(testfile, 'rb')
        tfo.close()

        with self.assertRaises(errors.Unsupported):
            self.fs.openbin(testfile, 'wb')

        assert len(data) == 100
        assert data_part == data[10:]
        self.assertTrue(read_file.closed)

        # Check disallow text mode
        with self.assertRaises(ValueError):
            with self.fs.openbin(testfile, 'rt') as read_file:
                pass

        # Check errors
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('foo.bin')

        # Open from missing dir
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('/foo/bar/test.txt')

        # Opening a file in a directory which doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('/egg/bar')

        # Opening with a invalid mode
        with self.assertRaises(ValueError):
            self.fs.openbin('foo.bin', 'h')

class TestYoutubeFS_Single(TestYoutubeFS):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/watch?v=cpPG0bKHYKc'
        self.url = url
        return YoutubeFS(url, playlist=False)


class TestYoutubeFS_Unseekable(TestYoutubeFS):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/watch?v=cpPG0bKHYKc'
        self.url = url
        return YoutubeFS(url, playlist=False, seekable=False)

    def test_openbin(self):
        testfile = self.fs.listdir(u'/')[0]

        # Read a binary file
        with self.fs.openbin(testfile, 'rb') as read_file:
            repr(read_file)
            text_type(read_file)
            self.assertIsInstance(read_file, io.IOBase)
            self.assertTrue(read_file.readable())
            self.assertFalse(read_file.writable())
            self.assertFalse(read_file.closed)
            data = read_file.read(100)
            self.assertFalse(read_file.seekable())
            with self.assertRaises(errors.Unsupported):
                read_file.seek(10)

        assert len(data) == 100
        self.assertTrue(read_file.closed)

        # Check disallow text mode
        with self.assertRaises(ValueError):
            with self.fs.openbin(testfile, 'rt') as read_file:
                pass

        # Check errors
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('foo.bin')

        # Open from missing dir
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('/foo/bar/test.txt')

        # Opening a file in a directory which doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('/egg/bar')

        # Opening with a invalid mode
        with self.assertRaises(ValueError):
            self.fs.openbin('foo.bin', 'h')

    def test_unsupported(self):
        with self.assertRaises(errors.Unsupported):
            self.fs.makedir('test')

        with self.assertRaises(errors.Unsupported):
            self.fs.remove('test')

        with self.assertRaises(errors.Unsupported):
            self.fs.removedir('test')

        with self.assertRaises(errors.Unsupported):
            self.fs.setinfo('test')


class TestYoutubeFS_SpecialChars1(TestYoutubeFS):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/watch?v=Y6qc88nhR28'
        self.url = url
        return YoutubeFS(url, playlist=False, seekable=False)

class TestYoutubeFS_SpecialChars2(TestYoutubeFS):

    def make_fs(self):
        # Return an instance of your FS object here
        url = u'https://www.youtube.com/watch?v=AOCBQ-Ut0QQ'
        self.url = url
        return YoutubeFS(url, playlist=False, seekable=False)