# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from __future__ import division, print_function, unicode_literals

import shlex

from ..imports import *


class soundcloud_backend(MediaHost):

    DOMAINS = ('soundcloud.com',)
    NAME = 'Soundcloud'

    def init(self):
        client_id = self.settings.get('SOUNDCLOUD_CLIENT_ID', '')
        if not client_id:
            return
        self.info_url = 'http://api.soundcloud.com/resolve.json' \
                      + '?client_id='+client_id \
                      + '&url=http://soundcloud.com/'

    def get_id(self, url):
        return url.path[1:]

    def get_info(self, track_id, raw):
        if not hasattr(self, 'info_url'):
            raise MediaHostException(self._('Error: you need to provide a client ID to use the %s backend') % self.NAME)
        r = iNS(type='audio')
        info = iNS(requests.get(self.info_url+track_id).json())
        if raw:
            return info
        if info.kind != 'track':
            raise MediaHostException(self._('%s is a %s, not a track' % (track_id,info.kind)))
        r.alternates = call(lambda url: [{'type':'video','url':url}], info.video_url or identity)
        make_author = safe(lambda u: {'name':u['username'], 'urlname':u['permalink']})
        r.authors = call(lambda a: [a], make_author(info.user or {}))
        r.beats_per_minute = info.bpm or identity
        r.comment_count = info.comment_count
        r.coverart_url = info.artwork_url
        r.description = info.description
        r.duration = info.duration / 1000
        r.favorite_count = info.favoritings_count
        r.genres = call(lambda a: [a], info.genre or identity)
        r.license = info.license
        r.published = call(parse_date, info.created_at)
        r.purchase_url = info.purchase_url or identity
        r.tags = shlex.split(info.tag_list)
        r.title = info.title
        r.subtype = info.track_type or identity
        r.view_count = info.playback_count
        r.waveform_url = info.waveform_url
        r.downloads = list(filter(None, [info.download_url, info.stream_url]))
        return r

    def normalize(self, track_id):
        return 'http://soundcloud.com/'+track_id
