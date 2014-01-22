# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from __future__ import division, print_function, unicode_literals

from ..imports import *


track_id_re = re.compile(r'/track/[^/]*/([0-9]+)')

class beatport_backend(MediaHost):

    DOMAINS = ('beatport.com',)
    NAME = 'Beatport'

    def get_id(self, url):
        track_id = track_id_re.search(url.path)
        if not track_id:
            raise MediaHostException(self._('Unrecognized url: %s') % url.geturl())
        return track_id.group(1)

    def get_info(self, track_id, raw):
        r = iNS(type='audio')
        info_url = 'http://api.beatport.com/catalog/3/beatport/track?id='
        info = iNS(requests.get(info_url+track_id).json())
        if raw:
            return info
        t = iNS(info.results.get('track', None))
        if not t:
            raise MediaHostException(self._('Failed to retrieve information for track %s' % (track_id)))
        make_author = safe(lambda a: {'name':a['name'], 'urlname':a['slug']})
        r.authors = list(filter(None, map(make_author, t.artists)))
        waveform = t.images.pop('waveform', identity)
        r.artworks = list(t.images.values())
        r.beats_per_minute = t.bpm or identity
        r.clef = t.key.pop('standard')
        r.clef.update(t.key)
        minutes, seconds = t.length.split(':')
        r.duration = int(minutes)*60 + int(seconds)
        r.genres = list(filter(None, (g.get('name', None) for g in t.genres)))
        r.published = call(parse_date, t.publishDate or identity)
        r.thumbnails = call(lambda a: [a], waveform)
        r.title = t.title
        return r

    def normalize(self, track_id):
        return 'http://www.beatport.com/track//'+track_id
