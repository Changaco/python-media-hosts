from __future__ import print_function, unicode_literals

import argparse
import json
try:
    import jsonpickle
except ImportError:
    jsonpickle = None

from . import MediaInfo, MediaInfoException
from .utils import urldecode


class FakeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)


p = argparse.ArgumentParser()
p.add_argument('uri')
p.add_argument('settings', nargs='*', default=[], help='e.g. SOUNDCLOUD_CLIENT_ID=x')
p.add_argument('-b', '--backends', nargs='*', default=None)
p.add_argument('-r', '--raw', default=False, action='store_true')
args = p.parse_args()


settings = dict(s.split('=') for s in args.settings)
media_info = MediaInfo(backends=args.backends, settings=settings)
try:
    info = media_info.get(args.uri, args.raw)
except MediaInfoException as e:
    print(e.args[0])
    exit(1)

if jsonpickle:
    print(json.dumps(json.loads(jsonpickle.encode(info.__dict__)), indent=4))
else:
    print(json.dumps(info.__dict__, indent=4, cls=FakeEncoder))
