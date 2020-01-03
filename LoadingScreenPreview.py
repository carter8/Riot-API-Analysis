import API

api_key = 'RGAPI-adab60fc-be49-40e9-b32c-39f814ef8f6e' # expires in 24hrs, generated at: developer.riotgames.com
summoner_name = 'the carter iii'
max_games = 30 # cannot be larger than ~45

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

# gets the info for each summoner in the active game
# active game information is only available during the loading screen and actual game
lobby = connection.get_active_games_by_summoner(summoner['id'])


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


def print_stats(stats, name):
    """
    Prints the win rate and kill/death ratio for a list of player stats

    :param list stats:   The list of player stats to that are being summarized and printed
    :param string name:  The name of the player
    """
    stats_to_print = stats
    stats_to_print.append(stats[4] - stats[0])
    stats_to_print[1] = stats_to_print[1] / stats_to_print[4]  # avg kills
    stats_to_print[2] = stats_to_print[2] / stats_to_print[4]  # avg deaths
    stats_to_print[3] = stats_to_print[3] / stats_to_print[4]  # avg assists
    print('%s on Selected Champion:' % name)
    print('Winrate: %.0f%% (%dW / %dL)' % (stats_to_print[0]/stats_to_print[4]*100, stats_to_print[0], stats_to_print[5]))
    print('Average KDA: %.2f' % (stats_to_print[1]/stats_to_print[2]))
    print()


def get_summoner_from_active_game(active_game, summoner_index, api_connection):
    summoner_info = [''] * 4
    summoner_info[0] = active_game['participants'][summoner_index]['summonerName']
    summoner_info[1] = active_game['participants'][summoner_index]['summonerId']
    summoner_info[2] = (api_connection.get_summoner_by_name(summoner_info[0]))['accountId']
    summoner_info[3] = active_game['participants'][summoner_index]['championId']
    return summoner_info


# info for summoner in index 0 of active game
summoner_1 = get_summoner_from_active_game(lobby, 0, connection)
summoner_1_matchlist = connection.get_matchlist_by_account(summoner_1[2], summoner_1[3])
summoner_1_stats = [0] * 5
total_games = 0

# check if they played champion before!!!
if 'status' in summoner_1_matchlist:
    print('%s has not played the champion before.' % (summoner_1[0]))
else:
    for match in summoner_1_matchlist['matches']:
        total_games += 1
        if total_games > max_games:
            break
        game = get_game_stats(match['gameId'], summoner_1[2])
        add_game_stats(summoner_1_stats, game)
    print_stats(summoner_1_stats, summoner_1[0])

# info for summoner in index 5 of active game
summoner_2 = get_summoner_from_active_game(lobby, 6, connection)
summoner_2_matchlist = connection.get_matchlist_by_account(summoner_2[2], summoner_2[3])
summoner_2_stats = [0] * 5
total_games = 0

if 'status' in summoner_2_matchlist:
    print('%s has not played the champion before.' % (summoner_2[0]))
else:
    for match in summoner_2_matchlist['matches']:
        total_games += 1
        if total_games > max_games:
            break
        game = get_game_stats(match['gameId'], summoner_2[2])
        add_game_stats(summoner_2_stats, game)
    print_stats(summoner_2_stats, summoner_2[0])