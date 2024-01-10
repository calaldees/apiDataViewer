import logging
log = logging.getLogger(__name__)


from types import MappingProxyType
from typing import Mapping, Iterable
def harden(data):
    """
    >>> harden({"a": [1,2,3]})
    mappingproxy({'a': (1, 2, 3)})
    >>> harden({"a": [1,2, {3}] })
    mappingproxy({'a': (1, 2, (3,))})
    >>> harden({"a": [1,2, {"b": 2}] })
    mappingproxy({'a': (1, 2, mappingproxy({'b': 2}))})
    >>> harden([1, {"c": True, "d": 3.14, "e": {"no", "no"}}])
    (1, mappingproxy({'c': True, 'd': 3.14, 'e': ('no',)}))
    """
    if isinstance(data, Mapping):
        return MappingProxyType({k: harden(v) for k, v in data.items()})
    if isinstance(data, Iterable) and not isinstance(data, str):
        return tuple((harden(i) for i in data))
    return data



#import json
#from bs4 import BeautifulSoup  # pip install beautifulsoup4
#CONTENT_TYPE_PARSERS = {
#    'json': ("application/json", json.load),
#    'html': ("text/html", partial(BeautifulSoup, features="html.parser")), #'html5lib'
#}
#CONTENT_TYPE_PARSERS:t.Dict=CONTENT_TYPE_PARSERS
#mime_type, response_parse_func = CONTENT_TYPE_PARSERS[type]

import urllib.request
from cache_tools import cache_disk
@cache_disk()
def urllib_request(*args, **kwargs):
    log.info(args[0])
    request = urllib.request.Request(*args, **kwargs)
    with urllib.request.urlopen(request) as response:
        return response.read()

def urllib_request_no_cache(*args, **kwargs):
    #log.info(args[0])
    request = urllib.request.Request(*args, **kwargs)
    with urllib.request.urlopen(request) as response:
        return response.read()


import csv
from pathlib import Path
def read_csv(path: Path):
    with Path(path).open() as f:
        return tuple(csv.DictReader(f))
