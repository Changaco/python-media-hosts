from datetime import datetime
import re
try:
    from urllib.parse import *
except ImportError:
    from urlparse import *

try:
    from dateutil.parser import parse as parse_date
except ImportError:
    parse_date = lambda _: identity
import requests

from miss.identity import *
from miss.namespace import iNS
from miss.six import ustr

from . import MediaHost, MediaHostException, mirror
from .utils import *
