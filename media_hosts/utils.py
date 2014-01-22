# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

from miss.six import PY3


if PY3:
    def urldecode(s):
        if isinstance(s, bytes):
            s = s.decode()
        return {k: len(v) == 1 and v[0] or v
                for k, v in parse_qsl(s)}
else:
    def udecode(o, encoding='utf8'):
        if isinstance(o, list):
            return [udecode(s, encoding) for s in o]
        else:
            return o.decode(encoding)
    def urldecode(s):
        return {k: udecode(len(v) == 1 and v[0] or v)
                for k, v in parse_qsl(s)}
