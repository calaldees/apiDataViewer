from functools import cached_property
import re
from collections import ChainMap
import typing as t
from types import MappingProxyType

from bs4 import BeautifulSoup

from _utils import harden


def safe_amalgamate_attrs(obj, attrs):
    return ChainMap(*filter(None, (
        getattr(obj, attr, None)
        for attr in attrs
    )))
def get_key_contains(data, subkey):
    """
    >>> data = {'My moose':1, 'My elephant':2, 'Elephant': 3}
    >>> get_key_contains(data, 'Moose')
    1
    >>> get_key_contains(data, 'Elephant')
    2
    """
    for k, v in data.items():
        if subkey.lower() in k.lower():
            return v
def _get(oo, sections):
    for section in sections:
        _all_sections = safe_amalgamate_attrs(oo, ('pages','sections','sectionGroups'))
        oo = get_key_contains(_all_sections, section)
        if not oo: return
    return oo


class ePortfolioManager():
    def __init__(self, notebooks):
        self.notebooks = notebooks

    def _get_student_sections(self, sections: t.Iterable[str]) -> MappingProxyType[str, t.Any]:  # MicrosoftGraphObjectBase
        return harden({
            student_name: _get(notebook, sections)
            for student_name, notebook in self.notebooks.items()
            if 'documentation' not in student_name.lower() and _get(notebook, sections)
        })

    @property
    def targets(self):
        student_journals_for_date = self._get_student_sections(('journal', '27th March'))
        return harden({
            student_name: Journal(notebook.content).targets
            for student_name, notebook in student_journals_for_date.items()
        })



class Journal():
    def __init__(self, html):
        self.soup = BeautifulSoup(html, features="html.parser")
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
    @cached_property
    def target_reflections(self):
        return [
            tr.text.strip()
            for tr in self.soup.find(string=re.compile('last.+targets',flags=re.IGNORECASE)).find_next('table').find_all('tr')
        ][1:]
