# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import fs
import pkg_resources

# Add the local code directory to the `fs` module path
fs.__path__.insert(0, os.path.realpath(
    os.path.join(__file__, '..', '..', 'fs')))
fs.opener.__path__.insert(0, os.path.realpath(
    os.path.join(__file__, '..', '..', 'fs', 'opener')))

# Add additional openers to the entry points
pkg_resources.get_entry_map('fs', 'fs.opener')['youtube'] = \
    pkg_resources.EntryPoint.parse(
        'youtube = fs.opener.youtubefs:YouTubeOpener',
        dist=pkg_resources.get_distribution('fs')
    )
