from types import MappingProxyType
import typing as t
from functools import cached_property

import json

from _utils import urllib_request, urllib_request_no_cache, harden


import logging
log = logging.getLogger(__name__)



class MicrosoftGraph():
    ENDPOINT = "https://graph.microsoft.com/v1.0/"
    def __init__(self, token:str):
        assert len(token) > 2000 and len(token) < 2500, "Setup `token` environ from https://developer.microsoft.com/en-us/graph/graph-explorer"
        self.token = token
    def _normalise_path(self, path):
        return self.ENDPOINT+path if not path.startswith(self.ENDPOINT) else path
    def get_json(self, path:str):
        return json.loads(self.get(path, headers={"Content-type": "application/json"}))
    def get(self, path:str, headers:t.Dict[str, str]={}):
        return urllib_request(self._normalise_path(path), headers={"Authorization": f"Bearer {self.token}", **headers})  #"Content-type": "text/html", 
    def post_json(self, path:str, data={}, headers:t.Dict[str,str]={}):
        return json.loads(urllib_request_no_cache(self._normalise_path(path), data=json.dumps(data).encode('utf-8'), headers={"Authorization": f"Bearer {self.token}", "Content-type": "application/json", **headers}, method='POST'))


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
    @property
    def data(self) -> MappingProxyType[str, object]:
        return harden(self.g.get_json(self.path))
    @property
    def content(self):
        return self.g.get(self.path + '/content')
    @property
    def name(self):
        return self._normalise_name(self.data)
    def _subpath(self, path:str, cls) -> MappingProxyType[str, object]:
        return harden({
            self._normalise_name(s): cls(self.g, s['self'])
            for s in self.g.get_json(self.path + path)['value']
        })

class NoteBookPage(MicrosoftGraphObjectBase):
    #def duplicate(self, destination_section_groups: t.Iterable[NotebookSectionGroup]):
        pass

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

class MicrosoftUser():
    def __init__(self, g:MicrosoftGraph, user:str):
        self.g = g
        self.user = user
    @property
    def onenote_notebooks(self) -> MappingProxyType[str, NoteBook]:
        return {
            n['displayName']: NoteBook(self.g, n['self'])
            for n in self.g.get_json(f"users/{self.user}/onenote/notebooks")['value']
        }
