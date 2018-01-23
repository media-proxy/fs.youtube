# coding: utf-8
"""`Youtube` opener definition.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from .base import Opener

__license__ = "MIT"
__copyright__ = "Copyright (c) 2017 media-proxy"
__author__ = "media-proxy"
__version__ = 'dev'

# Dynamically get the version of the main module
try:
    import pkg_resources
    _name = __name__.replace('.opener', '')
    __version__ = pkg_resources.get_distribution(_name).version
except Exception:  # pragma: no cover
    pkg_resources = None
finally:
    del pkg_resources


class YouTubeOpener(Opener):
    """`YouTube` opener.
    """

    protocols = ['youtube']

    @staticmethod
    def open_fs(fs_url, parse_result, writeable, create, cwd):  # noqa: D102
        from ..youtube import YoutubeFS

        _, _, _, ytuuid, params, _ = parse_result
        if 'v' in params:
            return YoutubeFS(params['v'], playlist=False)
        if 'list' in params:
            return YoutubeFS(params['list'])

        try:
            yt_fs = YoutubeFS(ytuuid)
        except ValueError:
            yt_fs = YoutubeFS(ytuuid, playlist=False)

        return yt_fs
