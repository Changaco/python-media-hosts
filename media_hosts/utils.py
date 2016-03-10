try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl


def urldecode(s):
    return {k: len(v) == 1 and v[0] or v
            for k, v in parse_qsl(s)}
