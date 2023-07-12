from functools import cached_property, reduce
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
def get_key_contains(data, _regex):
    """
    >>> data = {'My moose':1, 'My elephant':2, 'Elephant': 3}
    >>> get_key_contains(data, 'Moose')
    1
    >>> get_key_contains(data, 'Elephant')
    2
    """
    _regex = _regex if isinstance(_regex, re.Pattern) else re.compile(_regex, flags=re.IGNORECASE)
    for k, v in data.items():
        if _regex.search(k):
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
    def mentors(self):
        return Placements(self._get_student_sections(('placement',))).mentors

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


class Placements():
    def __init__(self, placement_sections):
        self.placement_sections = placement_sections

    @property
    def mentors(self):
        """
        My god?! What a mess this is
        Matching emails to possible mentor roles - over pages/placements that are inconsistent
        PGCE and SD 'placement1' and 'placement2' have been normalised (I don't know if this is the way it should be)
        """

        def extract_emails(html) -> t.Dict[str, str]:
            soup = BeautifulSoup(html, features="html.parser")
            regex_email = re.compile(r'[\w\-.]+@[\w\-.]+\.\w{2,4}')

            _line_number_map = {
                'professional': tuple(tag.parent.sourceline for tag in soup.find_all(string=re.compile('(pm|professional)', flags=re.IGNORECASE))),
                'subject': tuple(tag.parent.sourceline for tag in soup.find_all(string=re.compile('(sm|subject)', flags=re.IGNORECASE))),
            }
            def _score_email_category(e):
                _ = sorted({
                    min(abs(pos - e.parent.sourceline) for pos in poss): category
                    for category, poss in _line_number_map.items()
                    if poss
                }.items())
                return _[0] if _ else (1000, e.text)
            scored_emails_to_category = {
                tag.text.encode("ascii", "ignore").decode().strip(): _score_email_category(tag)
                for tag in soup.find_all(string=regex_email)
            }

            def _best_match(acc, i):
                email, (score, category) = i
                if acc.get(category,(1000, email))[0] >= score:
                    acc[category] = (score, email)
                return acc
            return {
                category: email
                for category, (score, email) in reduce(_best_match, scored_emails_to_category.items(), {}).items()
            }

        students_to_mentors_placement = {
            student_name: {
                page_name: extract_emails(page.content)
                for page_name, page in notebook.pages.items()
            }
            for student_name, notebook in self.placement_sections.items()
        }

        _placement_map = {
            'P1': re.compile(r'(1|base)', flags=re.IGNORECASE),
            'P2': re.compile(r'(2|contrast)', flags=re.IGNORECASE),
        }
        def _normalise_placement_name(page_name):
            for placement, _regex in _placement_map.items():
                if _regex.search(page_name):
                    return placement
            return 'unknown'
        return harden({
            student: { 
                _normalise_placement_name(placement_name): mentors
                for placement_name, mentors in placement_mentors.items()
                if mentors
            }
            for student, placement_mentors in students_to_mentors_placement.items()
        })