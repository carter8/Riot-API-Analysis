def get_game_stats(game_id, account_id, api_connection):
    """
    Get the stats of a given player for a single game

    :param long game_id:        The match ID (also called game ID)
    :param string account_id:   The account ID
    :param API api_connection:  The API object used to scrape data from Riot API

    :returns:  list of player statistics
                    0:  1 if win, 0 if loss
                    1:  number of kills
                    2:  number of deaths
                    3:  number of assists
                    4:  1 (number of games played. will always be 1)
    """
    # want to return win/loss, kills, deaths, assists
    stats = [0] * 5
    participant_id = 0
    game_stats = api_connection.get_match_by_id(game_id)
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


def get_ranked_league(summoner_id, api_connection):
    """
    Gets the solo ranked league that a player is in

    :param string summoner_id:  The summoner ID
    :param API api_connection:  The API object used to get data from Riot online API

    :returns:  string league
                   the solo ranked league the player is in
                   None if the player is not in one
    """
    leagues = api_connection.get_league_by_summoner(summoner_id)
    league = None

    if len(leagues) == 0:
        return league
    else:
        for queue in leagues:
            if queue['queueType'] == 'RANKED_SOLO_5x5':
                league = queue['tier'] + ' ' + queue['rank']
    return league


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
    print('Average KDA: %.2f\n' % (stats_to_print[1]/stats_to_print[2]))
