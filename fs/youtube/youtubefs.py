#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import with_statement

import pafy
from six.moves.urllib.request import BaseHandler
from six.moves.urllib.request import Request
from six.moves.urllib.request import build_opener
from six.moves.urllib.request import install_opener
from six.moves.urllib.request import urlopen
from six.moves.urllib.response import addinfourl

from .. import errors
from ..base import FS
from ..enums import ResourceType
from ..info import Info
from ..iotools import RawWrapper


class HTTPRangeHandler(BaseHandler):

    @classmethod
    def http_error_206(self, req, fp, code, msg, hdrs):
        # Range header supported
        r = addinfourl(fp, hdrs, req.get_full_url())
        r.code = code
        r.msg = msg
        return r

    @classmethod
    def http_error_416(self, req, fp, code, msg, hdrs):
        # Range header not supported
        raise URLError('Requested Range Not Satisfiable')


class SeekableHTTPFile:
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.pos = 0
        self.fileobj = None

        response = urlopen(url)
        response.close()

    def read(self, size=-1):
        if self.fileobj:
            self.fileobj.close()
        opener = build_opener(HTTPRangeHandler)
        install_opener(opener)

        if size < 0:
            rangeheader = {'Range': 'bytes=%s-' % (self.pos)}
        else:
            rangeheader = {'Range': 'bytes=%s-%s' % (self.pos, self.pos + size - 1)}

        req = Request(self.url, headers=rangeheader)
        res = urlopen(req)

        self.pos += size
        data = res.read()

        return data

    def tell(self):
        return self.pos

    def flush(self):
        pass

    def seek(self, offset, whence=0):
        """Seek within the byte range.
        Positioning is identical to that described under tell().
        """

        if whence == 0:  # absolute seek
            self.pos = offset
        elif whence == 1:  # relative seek
            self.pos += offset
        elif whence == 2:  # absolute from end of file
            raise errors.Unsupported('seek from end of file not supported.')
        else:
            raise errors.Unsupported('Whence must be 0, 1 or 2')

    def close(self):
        if self.fileobj:
            self.fileobj.close()

    @classmethod
    def writable(self):
        return False


class YoutubeFS(FS):
    """A filesystem for reading Youtube Playlists and Videos.

    Arguments:
        url (str): The YouTube URL for a Playlist or a Video

    """

    _meta = {
        'case_insensitive': False,
        'invalid_path_chars': '\0"\[]+|<>=;?*":',
        'network': True,
        'read_only': True,
        'thread_safe': True,
        'unicode_paths': True,
        'virtual': False,
    }

    def __init__(self, url, playlist=True, seekable=True):
        super(YoutubeFS, self).__init__()
        self.playlist = playlist
        self.seekable = seekable
        self.url = url
        self._cache = {}
        if playlist:
            self._title = pafy.get_playlist(self.url)['title']
        else:
            self._title = pafy.new(self.url).title

    def __str__(self):
        return 'YoutubeFS: %s' % self._title

    @classmethod
    def _get_name(self, pafyobj):
        name = '%s.%s' % (pafyobj.title, pafyobj.getbest().extension)

        for char in self._meta['invalid_path_chars']:
            name = name.replace(char, '')

        return name

    def listdir(self, path):
        _path = self.validatepath(path)

        if _path in [u'.', u'/', u'./']:
            if self.playlist:
                parser = pafy.get_playlist(self.url)
                outlist = []
                for entry in parser['items']:
                    name = self._get_name(entry['pafy'])
                    self._cache[self.validatepath(u'/%s' % name)] = entry['playlist_meta']['encrypted_id']
                    outlist.append(u'%s' % name)
                return outlist
            else:
                parser = pafy.new(self.url)
                name = self._get_name(parser)
                self._cache[self.validatepath(u'/%s' % name)] = self.url
                return [name]
        else:
            if _path in self._cache:
                raise errors.DirectoryExpected(path)
            else:
                raise errors.ResourceNotFound(path)

    def getinfo(self, path, namespaces=None):
        _path = self.validatepath(path)
        namespaces = namespaces or ('basic')

        if _path in [u'', u'.', u'/', u'./']:

            info = Info({
                "basic":
                {
                    "name": '',
                    "is_dir": True
                },
                "details":
                {
                    "type": int(ResourceType.directory)
                }
                })
            return info
        else:
            if _path in self._cache:
                info_dict = {}
                name = _path[1:]

                info_dict['basic'] = {
                    "name": name,
                    "is_dir": False
                }
                pafyobj = None
                stream = None
                if 'details' in namespaces:
                    pafyobj = pafy.new(self._cache[_path])
                    stream = pafyobj.getbest()
                    info_dict['details'] = {
                        "type": int(ResourceType.file),
                        "size": stream.get_filesize(),
                    }

                if 'mediaproxy.media' in namespaces:
                    if not pafyobj:
                        pafyobj = pafy.new(self._cache[_path])
                        stream = pafyobj.getbest()
                    info_dict['mediaproxy.media'] = {
                        "type": 'video',
                        "title": pafyobj.title,
                        "rating": pafyobj.rating,
                        "viewcount": pafyobj.viewcount,
                        "author": pafyobj.author,
                        "length": pafyobj.length,
                        "duration": pafyobj.duration,
                        "likes": pafyobj.likes,
                        "dislikes": pafyobj.dislikes,
                        "description": pafyobj.description,
                        "thumb": pafyobj.thumb,
                        "bigthumb": pafyobj.bigthumbhd,
                        "category": pafyobj.category,
                        "videoid": pafyobj.videoid,
                        "keywords": pafyobj.keywords,
                        # Streamdata
                        "mediatype": stream.mediatype,
                        "extension": stream.extension,
                        "quality": stream.quality,
                        "url": stream.url,
                    }

                return Info(info_dict)
            else:
                raise errors.ResourceNotFound(path)

    def openbin(self, path, mode=u'r', *args, **kwargs):

        _path = self.validatepath(path)

        if mode == 'rt':
            raise ValueError('rt mode not supported in openbin')

        if mode == 'h':
            raise ValueError('h mode not supported in openbin')

        if not 'r' in mode:
            raise errors.Unsupported()
        try:
            pafyobj = pafy.new(self._cache[_path])
            url = pafyobj.getbest().url
        except:
            raise errors.ResourceNotFound(path)

        class HTTPFile(RawWrapper):

            @classmethod
            def writable(self):
                return False

            @classmethod
            def seekable(self):
                return False

            @classmethod
            def flush(self):
                return

            @classmethod
            def seek(self, *args):
                raise errors.Unsupported()

        if self.seekable:
            response = SeekableHTTPFile(url)
            return RawWrapper(response, mode=mode, *args, **kwargs)
        else:
            return HTTPFile(urlopen(url), mode=mode, *args, **kwargs)

    @classmethod
    def makedir(self, *args, **kwargs):
        raise errors.Unsupported()

    @classmethod
    def remove(self, *args, **kwargs):
        raise errors.Unsupported()

    @classmethod
    def removedir(self, *args, **kwargs):
        raise errors.Unsupported()

    @classmethod
    def setinfo(self, *args, **kwargs):
        raise errors.Unsupported()
