# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import unittest

import fs
import fs.errors


class TestYoutubeOpener(unittest.TestCase):

    def test_open_plist_by_id(self):
        x = fs.open_fs('youtube://PLYlZ5VtcfgitfPyMGkZsYkhLm-eOZeQpY')
        x.close()

    def test_open_file_by_id(self):
        y = fs.open_fs('youtube://cpPG0bKHYKc')
        y.close()

    def test_open_plist_by_id(self):
        x = fs.open_fs('youtube://https://www.youtube.com/playlist?list=PLYlZ5VtcfgitfPyMGkZsYkhLm-eOZeQpY')
        x.close()

    def test_open_file_by_url(self):
        y = fs.open_fs('youtube://https://www.youtube.com/watch?v=cpPG0bKHYKc')
        y.close()

    def test_open_not_exist(self):
        with self.assertRaises(IOError):
            y = fs.open_fs('youtube://https://www.youtube.com/watch?v=cpPG1bKHYKc')

    def test_open_wrongid(self):
        with self.assertRaises(ValueError):
            y = fs.open_fs('youtube://12345')
