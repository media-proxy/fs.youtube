# fs.youtube

[![PyPI version](https://badge.fury.io/py/fs.youtube.svg)](https://pypi.python.org/pypi/fs.youtube) [![Build Status](https://travis-ci.org/merlink01/fs.youtube.svg?branch=master)](https://travis-ci.org/merlink01/fs.youtube) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/94a05423f81a4e79ac9defcff802a753)](https://www.codacy.com/app/merlink01/fs.youtube?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=merlink01/fs.youtube&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/merlink01/fs.youtube/branch/master/graph/badge.svg)](https://codecov.io/gh/merlink01/fs.youtube)


A PyFilesystem2 implementation for accessing YouTube Videos and Playlists


Installation
------------

Install directly from PyPI, using [pip](<https://pip.pypa.io/>):

    pip install fs.youtube

Usage
-----

### Opener

Use ``fs.open_fs`` to open a filesystem with an Youtube
[FS URL](<https://pyfilesystem2.readthedocs.io/en/latest/openers.html>):

```python
import fs
yt_fs = fs.open_fs('youtube://youtubeplaylistid')
```

The opener can use either use the YouTube Playlist ID or the whole Youtube URL.

Also Single Youtube Videos are supported.

### Constructor

```python
import fs.youtube
yt_fs = fs.youtube.YoutubeFS(
        url, playlist=True, seekable=True
        )
```

with each argument explained below:

``url``
  The Playlist/Video URL or simly use the YouTube ID 

``playlist``
  If the ID or URL is one Video only, set this to False

``seekable``
  Use a seekable implementation to move inside the videofile.

Once created, the ``YoutubeFS`` filesystem behaves like any other filesystem
(see the [Pyfilesystem2 documentation](<https://pyfilesystem2.readthedocs.io>)).

Feedback
--------

Found a bug ? Have an enhancement request ? Head over to the
[GitHub issue tracker](<https://github.com/merlink01/fs.youtube/issues>) of the
project if you need to report or ask something. If you are filling in on a bug,
please include as much information as you can about the issue, and try to
recreate the same bug in a simple, easily reproductible situation.

See also
--------

* [fs](<https://github.com/Pyfilesystem/pyfilesystem2>), the core Pyfilesystem2 library
* [Index of Filesystems](<https://www.pyfilesystem.org/page/index-of-filesystems/>), a list of PyFilesystem 2 implementations
