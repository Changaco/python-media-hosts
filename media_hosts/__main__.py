# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from __future__ import print_function, unicode_literals

import argparse
import json
try:
    import jsonpickle
except ImportError:
    jsonpickle = None

from . import MediaHosts, MediaHostException


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
media_hosts = MediaHosts(backends=args.backends, settings=settings)
try:
    info = media_hosts.get_info_by_url(args.uri, args.raw)
except MediaHostException as e:
    print(e.args[0])
    exit(1)

if jsonpickle:
    print(json.dumps(json.loads(jsonpickle.encode(info.__dict__)), indent=4, sort_keys=True))
else:
    print(json.dumps(info.__dict__, indent=4, cls=FakeEncoder, sort_keys=True))
