# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from __future__ import division, print_function, unicode_literals

from ..imports import *

try:
    import gdata.youtube.service
    yt_service = gdata.youtube.service.YouTubeService()
except ImportError:
    yt_service = None


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
            info = urldecode(urlopen(info_url).read())
            if not info:
                errors.append(self._('Recieved empty response from %s') % info_url)
        except Exception as e:
            info = {}
            errors.append(ustr(e))
            raise
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
            d = info.url_encoded_fmt_stream_map.split(',')
            d = {a['itag']: a for a in map(urldecode, d)}
            for fmt in info.fmt_list.split(','):
                itag, resolution, extra_data = fmt.split('/', 2)
                # TODO figure out what extra_data is
                d[itag].update(resolution=resolution, extra_data=extra_data)
            r.downloads = d.values()

        # Try to get info from GData
        try:
            entry = yt_service.GetYouTubeVideoEntry(video_id=video_id)
        except Exception as e:
            entry = None
            if yt_service is None:
                print('Warning: gdata module not found, some information could not be retrieved')
            else:
                errors.append(e.message.get('reason', ustr(e)))
        if raw:
            return iNS(get_video_info=info, gdata=entry)
        elif entry:
            make_author = safe(lambda a:
                {'name': author.name.text,
                 'urlname': author.uri.text.split('/')[-1]}
            )
            r.authors = list(filter(None, map(make_author, getattr(entry, 'author', [])))) or r.authors
            r.description = text(entry, 'content')
            r.duration = call(int, getattrsi(entry, 'media', 'duration', 'seconds'), r.duration)
            r.favorite_count = call(int, getattrsi(entry, 'statistics', 'favorite_count'))
            r.published = call(parse_date, text(entry, 'published'), r.published)
            rating = getattr(entry, 'rating', None)
            if rating:
                r.rating = dict(average=float(rating.average), num_raters=int(rating.num_raters))
            r.recorded = call(parse_date, text(entry, 'recorded'))
            thumbnails = [dict(url=t.url, height=int(t.height), width=int(t.width),
                            time=t.extension_attributes['time'])
                        for t in getattrsi(entry, 'media', 'thumbnail')]
            r.thumbnails = thumbnails or r.thumbnails
            r.title = text(entry, 'title') or r.title
            r.updated = call(parse_date, text(entry, 'updated'))
            r.view_count = call(int, getattrsi(entry, 'statistics', 'view_count'), r.view_count)
            d = [dict(url=c.url, type=c.type,
                    itag=c.extension_attributes['{http://gdata.youtube.com/schemas/2007}format'])
                for c in getattrsi(entry, 'media', 'content')
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
