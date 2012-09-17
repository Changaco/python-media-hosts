from __future__ import division, print_function, unicode_literals

import json
import shlex

from ..imports import *


class soundcloud_backend(MediaInfoBackend):

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

    def get_info(self, track_id):
        if not hasattr(self, 'info_url'):
            raise MediaInfoException(self._('Error: you need to provide a client ID to use the %s backend') % self.NAME)
        r = iNS(type='audio')
        info = iNS(json.loads(urlopen(self.info_url+track_id).read()))
        if info.kind != 'track':
            raise MediaInfoException(self._('%s is a %s, not a track' % (track_id,info.kind)))
        r.alternates = call(lambda url: [{'type':'video','url':url}], info.video_url or identity)
        r.authors = call(singleton, info.user['username'])
        r.artwork_url = info.artwork_url
        r.beats_per_minute = info.bpm or identity
        r.comment_count = info.comment_count
        r.description = info.description
        r.duration = info.duration / 1000
        r.favorite_count = info.favoritings_count
        r.genre = info.genre or identity
        r.license = info.license
        r.published = call(parse_date, info.created_at)
        r.purchase_url = info.purchase_url or identity
        r.tags = shlex.split(info.tag_list)
        r.thumbnails = call(lambda url: [{'url': url}], info.waveform_url)
        r.title = info.title
        r.subtype = info.track_type or identity
        r.view_count = info.playback_count
        r.downloads = list(filter(None, [info.download_url, info.stream_url]))
        return r

    def normalize(self, url):
        p = url.path
        return ('http://soundcloud.com'+p, p)
