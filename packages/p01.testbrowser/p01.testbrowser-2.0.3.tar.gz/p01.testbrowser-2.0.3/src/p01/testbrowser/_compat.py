from __future__ import unicode_literals
from __future__ import absolute_import

import sys
from future import standard_library
standard_library.install_aliases()

PYTHON3 = sys.version_info[0] == 3
PYTHON2 = sys.version_info[0] == 2

HAVE_MECHANIZE = False

import http.cookies as httpcookies
import http.client as httpclient
import base64
import sgmllib

if PYTHON2:
    import urllib
    import urllib2 as urllib_request
    import urlparse
    from urllib import quote as url_quote, urlencode
    from cgi import escape as html_escape
    from UserDict import DictMixin
    import StringIO
    import httplib
    import htmlentitydefs
    try:
        from collections import MutableMapping
    except ImportError:
        class MutableMapping(object, DictMixin):
            pass

    base64_encodebytes = base64.encodestring

else:
    import urllib.request as urllib_request
    import urllib.parse as urlparse
    from urllib.parse import quote as url_quote, urlencode
    from html import escape as html_escape
    from collections.abc import MutableMapping
    from io import StringIO
    import http.client as httplib
    import html.entities as htmlentitydefs
    base64_encodebytes = base64.encodebytes
