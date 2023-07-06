import os
from pprint import pprint
from functools import cached_property, partial
import re

from types import MappingProxyType
import typing as t

from cache_tools import cache_disk
from _utils import harden

import logging
log = logging.getLogger(__name__)


import urllib.request

import json
from bs4 import BeautifulSoup  # pip install beautifulsoup4
CONTENT_TYPE_PARSERS = {
    'json': ("application/json", json.load),
    'html': ("text/html", partial(BeautifulSoup, features="html.parser")), #'html5lib'
}
@cache_disk()
def get_url(url:str, type:str='json', headers={}, CONTENT_TYPE_PARSERS:t.Dict=CONTENT_TYPE_PARSERS):
    log.info(url)
    mime_type, response_parse_func = CONTENT_TYPE_PARSERS[type]
    request = urllib.request.Request(url, headers={"Content-type": mime_type, **headers})
    with urllib.request.urlopen(request) as response:
        return response_parse_func(response)


class MicrosoftGraph():
    ENDPOINT = "https://graph.microsoft.com/v1.0/"
    def __init__(self, token:str):
        assert len(token) > 2000 and len(token) < 2500, "Setup `token` environ from https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.token = token
    def _normalise_path(self, path):
        return self.ENDPOINT+path if not path.startswith(self.ENDPOINT) else path
    def get_json(self, path:str):
        return get_url(self._normalise_path(path), type='json', headers={"Authorization": f"Bearer {self.token}"})
    def get_html(self, path:str) -> BeautifulSoup:
        return get_url(self._normalise_path(path), type='html', headers={"Authorization": f"Bearer {self.token}"})


class MicrosoftGraphObjectBase():
    def __init__(self, g:MicrosoftGraph, path:str):
        self.g = g
        self.path = path
    def __str__(self):
        return self.path
    def __repr__(self):
        return f"<{self.__class__.__name__}>:{self}"
    @staticmethod
    def _normalise_name(d: MappingProxyType[str: object], name_keys=('name', 'displayName', 'title')) -> str:
        for key in name_keys:
            value = d.get(key)
            if value:
                return value
    @cached_property
    def data(self) -> MappingProxyType[str, object]:
        return harden(self.g.get_json(self.path))
    @property
    def name(self):
        return self._normalise_name(self.data)
    def _subpath(self, path:str, cls) -> MappingProxyType[str, object]:
        return harden({
            self._normalise_name(s): cls(self.g, s['self'])
            for s in self.g.get_json(self.path + path)['value']
        })

class NoteBookPage(MicrosoftGraphObjectBase):
    @property
    def content(self) -> BeautifulSoup:
        return self.g.get_html(self.path + '/content')

class NoteBookSection(MicrosoftGraphObjectBase):
    @property
    def pages(self) -> MappingProxyType[str, NoteBookPage]:
        return self._subpath('/pages', NoteBookPage)

class NoteBookSectionGroup(MicrosoftGraphObjectBase):
    @property
    def sections(self) -> MappingProxyType[str, NoteBookSection]:
        return self._subpath('/sections', NoteBookSection)

class NoteBook(MicrosoftGraphObjectBase):
    @property
    def sections(self) -> MappingProxyType[str, NoteBookSection]:
        return self._subpath('/sections', NoteBookSection)
    @property
    def sectionGroups(self) -> MappingProxyType[str, NoteBookSectionGroup]:
        return self._subpath('/sectionGroups', NoteBookSectionGroup)

class User():
    def __init__(self, g:MicrosoftGraph, user:str):
        self.g = g
        self.user = user
    @property
    def onenote_notebooks(self) -> MappingProxyType[str, NoteBook]:
        return {
            n['displayName']: NoteBook(self.g, n['self'])
            for n in self.g.get_json(f"users/{self.user}/onenote/notebooks")['value']
        }
    

class Journal():
    def __init__(self, soup:BeautifulSoup):
        self.soup = soup
    @cached_property
    def targets(self):
        def _get_target(target):
            e = self.soup.find(string=re.compile(target+'.+target', flags=re.IGNORECASE)).find_next('td')
            return {
                'target': e.text.strip(),
                'action_mentor': e.find_next(string=re.compile('action.+mentor', flags=re.IGNORECASE)).find_next('td').text.strip(),
                'action_student': e.find_next(string=re.compile('action.+student', flags=re.IGNORECASE)).find_next('td').text.strip(),
            }
        return {
            target: _get_target(target)
            for target in ('curriculum','subject','pedagogy')
        }



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    g = MicrosoftGraph(os.environ['token'])

    journal = User(g, 'sm1161@canterbury.ac.uk').onenote_notebooks['CCCU SD e-portfolio 22 - Computing'].sectionGroups['Anthony Smith'].sections['Mentor Meeting Journal'].pages['WB 27th March'].content  #['Attendance Record'].pages['Term 1'].content
    jj = Journal(journal)
    breakpoint()
    
    

    pprint(
        #g.get('me/drive/root/children')
        #g.get('me/onenote/notebooks')
        #g.get('me/onenote/notebooks?includesharednotebooks=true')
        #g.get('me/drive/sharedWithMe')
        #g.get('drives/b!xHXgvoU8vEyzub0jAj4giVQZ349IKF1DmbUorCVrz_wXiqJtUlVZSbvdnNnEXbpC/items/01YFPQNPCGP5LE5YJGQZG2E5UF2IO2OEV5')
        #g.get('sites/bee075c4-3c85-4cbc-b3b9-bd23023e2089/onenote/notebooks') no worky

        # https://graph.microsoft.com/v1.0/users/sm1161@canterbury.ac.uk/onenote/notebooks
        #g.get('users/sm1161@canterbury.ac.uk/onenote/notebooks')
        # This has the groupid urls


        # g.get('users/sm1161@canterbury.ac.uk/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sections') No work - 401 -empty because it has sectionGroups

        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/')

        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sectionGroups/')  #YEAH!!!
        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/sectionGroups/1-da46e048-00ad-4795-a5cf-24e304e78d41/sections')
        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/sections/1-997d595a-e9f0-47a5-b398-651becc13c6e/pages')
    )

#users/sm1161@canterbury.ac.uk/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sections


#https://graph.microsoft.com/v1.0/me/onenote/notebooks?includesharednotebooks=true