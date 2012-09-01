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
from miss.list import singleton
from miss.namespace import iNS
from miss.six import ustr

from . import MediaInfoBackend, MediaInfoException, mirror
from .utils import *
