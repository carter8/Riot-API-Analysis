from SummonerLookupFunctions import get_ranked_league

def get_summoner_from_active_game(active_game, summoner_index, api_connection):
    """
    Gets general summoner info for players in an active game
    
    :param dict active_game:        The active game dictionary which includes info for each player
                                    in the game
    :param int summoner_index:      Index which represents player's position in the game (1-10)
    :param RiotAPI api_connection:  The API object used to scrape data from Riot API
    
    :returns:  summoner_info
                   0: summoner name
                   1: summoner ID
                   2: account ID
                   3: champion ID
    """
    summoner_info = [''] * 4
    summoner_info[0] = active_game['participants'][summoner_index]['summonerName']
    summoner_info[1] = active_game['participants'][summoner_index]['summonerId']
    summoner_info[2] = (api_connection.get_summoner_by_name(summoner_info[0]))['accountId']
    summoner_info[3] = active_game['participants'][summoner_index]['championId']
    return summoner_info


def analyze_active_game(active_game, api_connection, queue_num, game_mode):
    """
    Iterates over every player in an active game to collect player stats relating to the specific
    game mode. Prints warnings if a player has not played their champion before or does not play
    the game mode often.
    
    It then prints out a summary for each team giving the champion level and score for each player,
    how often the player plays the game mode, and the player's ranked league if they play ranked.
    
    :param dict active_game:        The active game dictionary which includes info for each player
                                    in the game
    :param RiotAPI api_connection:  The API object used to scrape data from Riot API
    :param tuple queue_num:         Tuple of ints which represent queue numbers corresponding to the
                                    game mode
    :param string game_mode:        Name of the game mode used to identify it while printing analysis
    """
    team_1 = []
    team_2 = []
    # iterate over each player in the game
    for i in range(10):
        games = 0

        # get basic player info
        player = get_summoner_from_active_game(active_game, i, api_connection)

        # get champion stats and info for the player
        champion_mastery = api_connection.get_mastery_by_summoner_by_champion(player[1], player[3])

        # player stat list: champion level, champion score, total plays in the game mode, and ranked league
        player_stats = [player[0], 0, 0, 0, None]

        # check if player has played the champion before, if so, fill player stats
        if 'status' in champion_mastery:
            print('WARNING: %s has never their champion before.' % player[0])
        else:
            player_stats[1], player_stats[2] = champion_mastery['championLevel'], champion_mastery['championPoints']

        # get recent matches for player
        matches = api_connection.get_matchlist_by_account(player[2])

        # iterate over matches to count how often the player plays the game mode
        if 'status' in matches:
            print('WARNING: %s has not played any matches recently.' % player[0])
        else:
            for match in matches['matches']:
                if match['queue'] in queue_num:
                    games += 1
            player_stats[3] = games
            if games < 5:
                print('WARNING: %s has only played %d %s games recently.' % (player[0], games, game_mode))

        # get the ranked league for each player
        player_stats[4] = get_ranked_league(player[1], api_connection)

        # sort the players into their teams
        if 0 <= i <= 4:
            team_1.append(player_stats)
        else:
            team_2.append(player_stats)

    # sort each team by who is better with their champion
    team_1 = sorted(team_1, key=lambda x: x[2], reverse=True)
    team_2 = sorted(team_2, key=lambda x: x[2], reverse=True)

    # print the stats for each team
    print('\nTeam 1')
    for i in team_1:
        print('%s on champ: Level %d, %d score\n%s games: %d' % (i[0], i[1], i[2], game_mode, i[3]))
        if i[4] is not None:
            print('League: %s' % i[4])
    print('\nTeam 2')
    for i in team_2:
        print('%s on champ: Level %d, %d score\n%s games: %d' % (i[0], i[1], i[2], game_mode, i[3]))
        if i[4] is not None:
            print('League: %s' % i[4])
