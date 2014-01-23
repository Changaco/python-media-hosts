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


def urldecode(s):
    return {k: len(v) == 1 and v[0] or v
            for k, v in parse_qsl(s)}
