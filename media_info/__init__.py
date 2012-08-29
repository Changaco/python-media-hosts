from importlib import import_module
from os import listdir
from os.path import dirname
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from miss.str import pstrip


mirror = lambda a: a


def list_backends():
    return [a[:-3] for a in listdir(dirname(__file__)+'/backends')
                   if a[0] != '_' and a.endswith('.py')]


class MediaInfo:

    def __init__(self, backends=None, _=mirror):
        self._ = _
        self.backends = []
        for backend in (backends or list_backends()):
            self.backends.append(import_module('.backends.'+backend, 'media_info'))
        self.domains = {domain: backend for backend in self.backends
                                        for domain in backend.DOMAINS}

    def get(self, url):
        u = urlparse(url) # this doesn't validate the URL and doesn't throw exceptions
        backend = self.domains.get(pstrip(u.hostname, 'www.'), None)
        if backend is None:
            raise MediaInfoException(self._('Unrecognized domain name: %s') % u.hostname)
        else:
            info = backend.get_media_info(self._, u)
            info.service = backend.__name__.rsplit('.', 1)[1]
            return info


class MediaInfoException(Exception): pass
