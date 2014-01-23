# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from __future__ import division, print_function, unicode_literals

import traceback

from ..imports import *


def text(o, *keys):
    keys += ('$t',)
    return getitemsi(o, *keys)


video_id_re = re.compile(r'/(?:watch\?.*v=)?([a-zA-Z0-9_-]{11})')

class youtube_backend(MediaHost):

    DOMAINS = ('youtube.com', 'youtu.be')
    NAME = 'Youtube'

    def get_id(self, url):
        video_id = video_id_re.search(url.path + '?' + url.query)
        if not video_id:
            raise MediaHostException(self._('Unrecognized url: %s') % url.geturl())
        return video_id.group(1)

    def get_info(self, video_id, raw):
        r = iNS(type='video')
        errors = []

        # Try to get info from /get_video_info
        info_url = 'http://youtube.com/get_video_info?video_id=%s' % video_id
        try:
            info = urldecode(requests.get(info_url).text)
            if not info:
                errors.append(self._('Received empty response from %s') % info_url)
        except Exception:
            traceback.print_exc()
            info = {}
        if raw:
            pass
        elif info.get('status', 'ok') != 'ok':
            errors.append(info.get('reason', ustr(info)).replace('\\n', '\n'))
        elif info:
            info = iNS(info)
            r.duration = int(info.length_seconds)
            r.published = call(datetime.fromtimestamp, int(info.timestamp))
            r.rating = call(lambda a: dict(average=a), float(info.avg_rating))
            r.tags = info.keywords.split(',')
            r.thumbnails = call(lambda url: [{'url': url}], info.thumbnail_url)
            r.title = info.title
            r.view_count = int(info.view_count)
            # Decode download info
            ds = info.url_encoded_fmt_stream_map.split(',')
            ds = {d['itag']: d for d in map(urldecode, ds) if 'itag' in d}
            for fmt in info.fmt_list.split(','):
                itag, resolution, extra_data = fmt.split('/', 2)
                # TODO figure out what extra_data is
                d = ds[itag]
                d.update(resolution=resolution, extra_data=extra_data)
                d['yt_format'] = d.pop('itag')
            r.downloads = list(ds.values())

        # Try to get info from gdata API v2
        url = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % video_id
        try:
            entry = requests.get(url).json()['entry']
            if not entry:
                errors.append(self._('Received empty response from %s') % url)
        except Exception:
            traceback.print_exc()
            entry = {}
        if raw:
            return iNS(get_video_info=info, gdata=entry)
        elif entry:
            i = iNS(entry)
            media = iNS(i['media$group'])
            stats = iNS(i['yt$statistics'])
            make_author = safe(lambda a:
                {'name': author.name.text,
                 'urlname': author.uri.text.split('/')[-1]}
            )
            r.authors = list(filter(None, map(make_author, i.author))) or r.authors
            r.description = text(media, 'media$description')
            r.duration = getitemsi(media, 'yt$duration', 'seconds')
            r.favorite_count = stats['favoriteCount']
            r.published = call(parse_date, text(i, 'published'), r.published)
            r.rating = i['gd$rating']
            r.rating['num_raters'] = r.rating.pop('numRaters', identity)
            r.recorded = call(parse_date, text(i, 'yt$recorded'))
            r.thumbnails += media['media$thumbnail']
            r.title = text(i, 'title') or r.title
            r.updated = call(parse_date, text(i, 'updated'))
            r.view_count = stats['viewCount'] or r.view_count
            d = [dict(url=c.url, type=c.type, yt_format=c['yt$format'])
                 for c in map(iNS, media['media$content'])
                 if c.type.startswith('video')]
            r.downloads += d

        if not r.title:
            if errors:
                error = self._('Youtube said:\n"%s"') % max(errors, key=len)
            else:
                error = self._('unknown reason')
            raise MediaHostException(self._('Getting video info failed, %s') % error)

        return r

    def normalize(self, video_id):
        """
        >>> print(normalize(mirror, urlparse('http://youtube.com/watch?a=b&v=0aA1bB2cC9z&c=d')))
        http://youtube.com/watch?v=0aA1bB2cC9z
        >>> print(normalize(mirror, urlparse('http://youtu.be/0aA1bB2cC9z')))
        http://youtube.com/watch?v=0aA1bB2cC9z
        """
        return 'http://youtube.com/watch?v='+video_id
