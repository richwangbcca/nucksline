from nhlpy.nhl_client import NHLClient
from util import NHLCLIENT

def player_info(player):
    """ Filter out information, return the relevant ones """
    player_info = NHLCLIENT.stats.player_career_stats(player_id=player['playerId'])
    return {
        'name': player['skaterFullName'],
        'points': player['points'],
        'goals': player['goals'],
        'assists': player['assists'],
        'number': player_info['sweaterNumber'],
        'headshot': player_info['headshot']
    }

def find_leaders():
    """ Return the player info for the points, goals, and assists leaders """
    stats = NHLCLIENT.stats.skater_stats_summary_simple(franchise_id=20, start_season="20242025", end_season="20242025")
    points_leader = max(stats, key=lambda x: x['points'])
    goals_leader = max(stats, key=lambda x: x['goals'])
    assists_leader = max(stats, key=lambda x: x['assists'])

    points_info = player_info(points_leader)
    goals_info = player_info(goals_leader)
    assists_info = player_info(assists_leader)

    return {'points': points_info, 'goals': goals_info, 'assists': assists_info}