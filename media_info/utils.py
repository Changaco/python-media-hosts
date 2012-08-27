try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

from miss.six import PY3


def text(o, *attrs):
    attrs += ('text',)
    return getattrs(o, *attrs)


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
