"""
This script gives the win rate and kill/death ratio a player in each different
game mode they have played recently in League of Legends, as well as a total
win rate and kill/death ratio.

To look up the stats for a different player, simply change the summoner name
"""

import API

api_key = 'RGAPI-adab60fc-be49-40e9-b32c-39f814ef8f6e' # expires in 24hrs, generated at: developer.riotgames.com
summoner_name = 'xo slime'
max_games = 90 # cannot be larger than 98 due to rate limit on requests to the Riot API

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

# get the most recent matches for the summoner
match_list = connection.get_matchlist_by_account(summoner['accountId'])


def get_game_stats(game_id, account_id):
    """
    Get the stats of a given player for a single game

    :param int game_id:     The match ID (also called game ID)
    :param int account_id:  The account ID

    :returns:  list of player statistics
                   list indices and values
                    0:  1 if win, 0 if loss
                    1:  number of kills
                    2:  number of deaths
                    3:  number of assists
                    4:  1 (number of games played. will always be 1)
    """
    # want to return win/loss, kills, deaths, assists
    stats = [0] * 5
    participant_id = 0
    game_stats = connection.get_match_by_id(game_id)
    for player in game_stats['participantIdentities']:
        if player['player']['accountId'] == account_id:
            participant_id = player['participantId']
            break
    for player in game_stats['participants']:
        if player['participantId'] == participant_id:
            if player['stats']['win']:
                stats[0] = 1
            stats[1] += player['stats']['kills']
            stats[2] += player['stats']['deaths']
            stats[3] += player['stats']['assists']
            stats[4] = 1
            break
    return stats


def add_game_stats(total_stats, stats_to_add):
    """
    Adds a list of game stats to another list of game stats

    :param list total_stats:   The list of total stats that will get the other list added to it
    :param list stats_to_add:  The list of game stats that are being added
    """
    total_stats[0] += stats_to_add[0]
    total_stats[1] += stats_to_add[1]
    total_stats[2] += stats_to_add[2]
    total_stats[3] += stats_to_add[3]
    total_stats[4] += stats_to_add[4]


def print_stats(stats, queue):
    """
    Prints the win rate and kill/death ratio for a list of player stats

    :param list stats:    The list of player stats to that are being summarized and printed
    :param string queue:  The name of the queue where the stats are from
    """
    stats_to_print = stats
    stats_to_print.append(stats[4] - stats[0])
    stats_to_print[1] = stats_to_print[1] / stats_to_print[4]  # avg kills
    stats_to_print[2] = stats_to_print[2] / stats_to_print[4]  # avg deaths
    stats_to_print[3] = stats_to_print[3] / stats_to_print[4]  # avg assists
    print('%s | Winrate: %.0f%% (%dW / %dL)' % (queue, stats_to_print[0]/stats_to_print[4]*100, stats_to_print[0], stats_to_print[5]))
    print('Average KDA: %.2f' % (stats_to_print[1]/stats_to_print[2]))
    print()


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
            blind_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(blind_stats, blind_game)
        elif match['queue'] == 920:
            # poro king
            pk_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(pk_stats, pk_game)
        elif match['queue'] == 450:
            # ARAM
            aram_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(aram_stats, aram_game)
        elif match['queue'] == 400:
            # unranked draft pick
            draft_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(draft_stats, draft_game)
        elif match['queue'] == 420:
            # ranked solo/duo pick
            ranked_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(ranked_stats, ranked_game)
        elif match['queue'] == 440:
            # ranked flex pick
            ranked_flex_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(ranked_flex_stats, ranked_flex_game)
        elif match['queue'] == 900:
            # URF
            urf_game = get_game_stats(match['gameId'], summoner['accountId'])
            add_game_stats(urf_stats, urf_game)
        else:
            print('Queue not coded. Queue #: %d' % match['queue'])
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

print_stats(total_stats, 'Total')