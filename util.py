from fake_useragent import UserAgent
from nhlpy.nhl_client import NHLClient

NHLCLIENT = NHLClient()

def random_agent():
    """ Create a random user agent for BeautifulSoup """
    return {"User-Agent": UserAgent().random}

def contains_any(string, elements):
    """ Check if a string contains any of elements"""
    return any(element in string for element in elements)

def create_name_list():
    """ Create the list of Canucks players and staff (manual) to search for """
    roster = NHLCLIENT.teams.roster(team_abbr='VAN', season="20242025")
    full_roster = roster["forwards"] + roster["defensemen"] + roster["goalies"]
    canucks_names = []
    for player in full_roster:
        canucks_names.append(player['lastName']['default'].lower())
    canucks_names += ['tocchet', 'allvin', 'rutherford', 'aquillini', 'canucks', 'vancouver']
    return canucks_names