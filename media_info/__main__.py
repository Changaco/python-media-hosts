from __future__ import print_function, unicode_literals
import argparse
import json
try:
    import jsonpickle
except ImportError:
    jsonpickle = None

from . import MediaInfo, MediaInfoException

p = argparse.ArgumentParser()
p.add_argument('url')
p.add_argument('-b', '--backends', nargs='*', default=None)
args = p.parse_args()

class FakeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

media_info = MediaInfo(backends=args.backends)
try:
    info = media_info.get(args.url)
    if jsonpickle:
        print(json.dumps(json.loads(jsonpickle.encode(info.__dict__)), indent=4))
    else:
        print(json.dumps(info.__dict__, indent=4, cls=FakeEncoder))
except MediaInfoException as e:
    print(e.args[0])
