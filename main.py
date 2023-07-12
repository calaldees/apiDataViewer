import os
from pprint import pprint

from collections import ChainMap

import logging
log = logging.getLogger(__name__)

from microsoft_graph import MicrosoftGraph, MicrosoftUser
from eportfolio import ePortfolioManager


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    token = os.environ.get('token')
    assert token, "$token should exist in environ - see https://developer.microsoft.com/en-us/graph/graph-explorer"
    g = MicrosoftGraph(token)

    notebooks = MicrosoftUser(g, 'sm1161@canterbury.ac.uk') .onenote_notebooks

    eportfolios = ePortfolioManager(ChainMap(
        notebooks['CCCU SD e-portfolio 22 - Computing'].sectionGroups,
        notebooks['CCCU PG e-portfolio 22 - Computing'].sectionGroups,
    ))
    
    #eportfolios.targets
    mm = eportfolios.mentors
    pprint(mm)
    breakpoint()
