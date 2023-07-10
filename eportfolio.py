from functools import cached_property

import re

from bs4 import BeautifulSoup


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
