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

    #journal_content = MicrosoftUser(g, 'sm1161@canterbury.ac.uk') \
    #    .onenote_notebooks['CCCU SD e-portfolio 22 - Computing'] \
    #    .sectionGroups['Anthony Smith'] \
    #    .sections['Mentor Meeting Journal'] \
    #    .pages['WB 27th March'] \
    #    .content
    #['Attendance Record'].pages['Term 1'].content

    #jj = Journal(journal_content)
    #jj.target_reflections

    notebooks = MicrosoftUser(g, 'sm1161@canterbury.ac.uk') .onenote_notebooks

    eportfolios = ePortfolioManager(ChainMap(
        notebooks['CCCU SD e-portfolio 22 - Computing'].sectionGroups,
        notebooks['CCCU PG e-portfolio 22 - Computing'].sectionGroups,
    ))
    
    #eportfolios.targets
    eportfolios.mentors

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