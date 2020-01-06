"""
This script gives the win rate and kill/death ratio a player in each different
game mode they have played recently in League of Legends, as well as a total
win rate and kill/death ratio.

To look up the stats for a different player, simply change the summoner name
"""

import API
from SummonerLookupFunctions import get_game_stats, get_ranked_league, add_game_stats, print_stats

# api key is generated at developer.riotgames.com
# expires 24 hours after generation
api_key = 'INSERT-API-KEY-HERE'

summoner_name = 'The Carter III'
max_games = 90  # cannot be larger than 98 due to rate limit on requests to the Riot API

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

# get the most recent matches for the summoner
match_list = connection.get_matchlist_by_account(summoner['accountId'])

# iterate through match list and get stats for each queue
urf_stats = [0] * 5
aram_stats = [0] * 5
pk_stats = [0] * 5
blind_stats = [0] * 5
draft_stats = [0] * 5
ranked_stats = [0] * 5
ranked_flex_stats = [0] * 5
total_games = 0
for match in match_list['matches']:
    total_games += 1
    if total_games < max_games:
        if match['queue'] == 430:
            # unranked blind pick
            blind_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(blind_stats, blind_game)
        elif match['queue'] == 920:
            # poro king
            pk_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(pk_stats, pk_game)
        elif match['queue'] == 450:
            # ARAM
            aram_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(aram_stats, aram_game)
        elif match['queue'] == 400:
            # unranked draft pick
            draft_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(draft_stats, draft_game)
        elif match['queue'] == 420:
            # ranked solo/duo pick
            ranked_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(ranked_stats, ranked_game)
        elif match['queue'] == 440:
            # ranked flex pick
            ranked_flex_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(ranked_flex_stats, ranked_flex_game)
        elif match['queue'] == 900:
            # URF
            urf_game = get_game_stats(match['gameId'], summoner['accountId'], connection)
            add_game_stats(urf_stats, urf_game)
        else:
            print('Queue not coded. Queue #: %d' % match['queue'], connection)
    else:
        break

# calculate total stats and print queue summaries
total_stats = [0] * 5

print('Stats for %s:\n' % (summoner['name']))

if urf_stats[4] != 0:
    add_game_stats(total_stats, urf_stats)
    print_stats(urf_stats, 'URF')

if pk_stats[4] != 0:
    add_game_stats(total_stats, pk_stats)
    print_stats(pk_stats, 'Poro King')

if aram_stats[4] != 0:
    add_game_stats(total_stats, aram_stats)
    print_stats(aram_stats, 'ARAM')

if blind_stats[4] != 0:
    add_game_stats(total_stats, blind_stats)
    print_stats(blind_stats, 'Blind Pick')

if draft_stats[4] != 0:
    add_game_stats(total_stats, draft_stats)
    print_stats(draft_stats, 'Draft Pick')

if ranked_flex_stats[4] != 0:
    add_game_stats(total_stats, ranked_flex_stats)
    print_stats(ranked_flex_stats, 'Ranked Flex')

if ranked_stats[4] != 0:
    add_game_stats(total_stats, ranked_stats)
    print_stats(ranked_stats, 'Ranked Solo/Duo')

# get and print the ranked league if summoner is a member of one
ranked_league = get_ranked_league(summoner['id'], connection)
if ranked_league is not None:
    print('Ranked Solo/Duo League: %s\n' % ranked_league)

print_stats(total_stats, 'Total')
