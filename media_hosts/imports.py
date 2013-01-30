# This file is part of a program licensed under the terms of the GNU Lesser
# General Public License version 3 (or at your option any later version)
# as published by the Free Software Foundation.
#
# If you have not received a copy of the GNU Lesser General Public License
# along with this file, see <http://www.gnu.org/licenses/>.


from datetime import datetime
import re
try:
    from urllib.request import *
    from urllib.parse import *
except ImportError:
    from urllib2 import *
    from urlparse import *

try:
    from dateutil.parser import parse as parse_date
except ImportError:
    parse_date = lambda _: identity

from miss.identity import *
from miss.namespace import iNS
from miss.six import ustr

from . import MediaHost, MediaHostException, mirror
from .utils import *
