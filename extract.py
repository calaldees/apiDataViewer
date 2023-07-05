import os
from pprint import pprint
from functools import cached_property

from types import MappingProxyType
import typing as t

from cache_tools import cache_disk
from _utils import harden

import logging
log = logging.getLogger(__name__)

import urllib.request
import json
@cache_disk()
def get_json(url, headers={}):
    log.info(url)
    req = urllib.request.Request(url, headers={"Content-type": "application/json", **headers})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


class MicrosoftGraph():
    ENDPOINT = "https://graph.microsoft.com/v1.0/"
    def __init__(self, token:str):
        assert len(token) > 2000 and len(token) < 2500, "Setup `token` environ from https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.token = token
    def get(self, path:str) -> dict:
        url = self.ENDPOINT+path if not path.startswith(self.ENDPOINT) else path
        return get_json(url, headers={"Authorization": f"Bearer {self.token}"})

class MicrosoftGraphObjectBase():
    def __init__(self, g:MicrosoftGraph, path:str):
        self.g = g
        self.path = path
    def __str__(self):
        return self.path
    def __repr__(self):
        return str(self)
    @cached_property
    def data(self) -> MappingProxyType[str, object]:
        return harden(self.g.get(self.path))
    @property
    def name(self):
        return self.data.get('name') or self.data.get('displayName')
    def _subpath(self, path:str, cls) -> MappingProxyType[str, object]:
        return harden({
            s['displayName']: cls(self.g, s['self'])
            for s in self.g.get(self.path + path)['value']
        })

class NoteBookSection(MicrosoftGraphObjectBase):
    pass

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
            for n in self.g.get(f"users/{self.user}/onenote/notebooks")['value']
        }
    



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #print(get_json("https://jsonplaceholder.typicode.com/todos/1"))
    g = MicrosoftGraph(os.environ['token'])
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

        User(g, 'sm1161@canterbury.ac.uk').onenote_notebooks['CCCU SD e-portfolio 22 - Computing'].sectionGroups['Anthony Smith'].sections

        # g.get('users/sm1161@canterbury.ac.uk/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sections') No work - 401 -empty because it has sectionGroups

        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/')

        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sectionGroups/')  #YEAH!!!
        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/sectionGroups/1-da46e048-00ad-4795-a5cf-24e304e78d41/sections')
        #g.get('users/c4168a74-5379-49f3-bda2-91efdd7a27d8/onenote/sections/1-997d595a-e9f0-47a5-b398-651becc13c6e/pages')
    )

#users/sm1161@canterbury.ac.uk/onenote/notebooks/1-c45f72e9-0b2b-4e65-a0d0-4c7d901749b7/sections


#https://graph.microsoft.com/v1.0/me/onenote/notebooks?includesharednotebooks=true