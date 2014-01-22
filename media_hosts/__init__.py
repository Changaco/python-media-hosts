# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


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


class MediaHosts:

    def __init__(self, backends=None, _=mirror, settings={}):
        self._ = _
        self.backends = []
        for backend in (backends or list_backends()):
            try:
                module = import_module('media_hosts.backends.'+backend)
                cls = getattr(module, backend+'_backend')
                instance = cls(_, settings)
                self.backends.append(instance)
            except Exception:
                print('Failed to import "%s" backend:' % backend)
                import traceback
                traceback.print_exc()
        self.domains = {domain: backend for backend in self.backends
                                        for domain in backend.DOMAINS}

    def get_backend(self, url_str):
        url = urlparse(url_str) # this doesn't validate the URL and doesn't throw exceptions
        try:
            return (url, self.domains[pstrip(url.hostname, 'www.')])
        except KeyError:
            raise MediaHostException(self._('Unrecognized domain name: %s') % url.hostname)

    def get_info_by_id(self, backend, media_id, raw=False):
        info = backend.get_info(media_id, raw)
        info.id = media_id
        info.service = backend.NAME
        return info

    def get_info_by_url(self, url_str, raw=False):
        url, backend = self.get_backend(url_str)
        return self.get_info_by_id(backend, backend.get_id(url), raw)

    def normalize(self, url_str):
        url, backend = self.get_backend(url_str)
        i = backend.get_id(url)
        return (backend, backend.normalize(i), i)


class MediaHost(object):

    def __init__(self, _, settings):
        self._ = _
        self.settings = settings
        self.init()

    def init(self):
        pass


class MediaHostException(Exception): pass
