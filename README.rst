fs.youtube
==========

.. image:: https://badge.fury.io/py/fs.youtube.svg
    :target: https://badge.fury.io/py/fs.youtube

.. image:: https://travis-ci.org/media-proxy/fs.youtube.svg?branch=master
    :target: https://travis-ci.org/media-proxy/fs.youtube
    
.. image:: https://api.codacy.com/project/badge/Grade/c8331c97a4054df88cc79878c615cdb2
    :target: https://www.codacy.com/app/media-proxy/fs.youtube?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=media-proxy/fs.youtube&amp;utm_campaign=Badge_Grade
    
.. image:: https://codecov.io/gh/media-proxy/fs.youtube/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/media-proxy/fs.youtube
    
.. image:: https://pyup.io/repos/github/media-proxy/fs.youtube/shield.svg
    :target: https://pyup.io/repos/github/media-proxy/fs.youtube/

A PyFilesystem2 implementation for accessing YouTube Videos and
Playlists

Installation
------------

Install directly from PyPI, using `pip <https://pip.pypa.io/>`__:

::

    pip install fs.youtube

Usage
-----

Opener
~~~~~~

Use ``fs.open_fs`` to open a filesystem with an Youtube `FS
URL <https://pyfilesystem2.readthedocs.io/en/latest/openers.html>`__:

.. code:: python

    import fs
    yt_fs = fs.open_fs('youtube://youtubeplaylistid')

The opener can use either use the YouTube Playlist ID or the whole
Youtube URL.

Also Single Youtube Videos are supported.

Constructor
~~~~~~~~~~~

.. code:: python

    import fs.youtube
    yt_fs = fs.youtube.YoutubeFS(
            url, playlist=True, seekable=True
            )

with each argument explained below:

``url`` The Playlist/Video URL or simly use the YouTube ID

``playlist`` If the ID or URL is one Video only, set this to False

``seekable`` Use a seekable implementation to move inside the videofile.

Once created, the ``YoutubeFS`` filesystem behaves like any other
filesystem (see the `Pyfilesystem2
documentation <https://pyfilesystem2.readthedocs.io>`__).

Feedback
--------

Found a bug ? Have an enhancement request ? Head over to the `GitHub
issue tracker <https://github.com/media-proxy/fs.youtube/issues>`__ of
the project if you need to report or ask something. If you are filling
in on a bug, please include as much information as you can about the
issue, and try to recreate the same bug in a simple, easily
reproductible situation.

See also
--------

-  `fs <https://github.com/Pyfilesystem/pyfilesystem2>`__, the core
   Pyfilesystem2 library
-  `Index of
   Filesystems <https://www.pyfilesystem.org/page/index-of-filesystems/>`__,
   a list of PyFilesystem 2 implementations

.. |PyPI version| image:: https://badge.fury.io/py/fs.youtube.svg
   :target: https://pypi.python.org/pypi/fs.youtube
.. |Build Status| image:: https://travis-ci.org/media-proxy/fs.youtube.svg?branch=master
   :target: https://travis-ci.org/media-proxy/fs.youtube
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/c8331c97a4054df88cc79878c615cdb2
   :target: https://www.codacy.com/app/media-proxy/fs.youtube?utm_source=github.com&utm_medium=referral&utm_content=media-proxy/fs.youtube&utm_campaign=Badge_Grade
.. |codecov| image:: https://codecov.io/gh/media-proxy/fs.youtube/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/media-proxy/fs.youtube
