import urllib.parse
from urllib.parse import urlparse, urlsplit, urlunparse, urlunsplit


def test():
    a = urlparse("")
    b = urlunparse(a)
    c = urlsplit("")
    d = urlunsplit(c)

    e = urllib.parse.urlparse("")
    f = urllib.parse.urlunparse(e)
    g = urllib.parse.urlsplit("")
    h = urllib.parse.urlunsplit(g)
