import API

api_key = 'RGAPI-4ad9bfde-d344-4f8f-b075-f9a9ee1ecdac' # expires in 24hrs, generated at: developer.riotgames.com
summoner_name = 'the carter iii'
max_games = 30 # cannot be larger than ~45

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

# gets the info for each summoner in the active game
# usuable once loading screen starts
lobby = connection.get_active_games_by_summoner(summoner['id'])

def get_game_stats(game_id, account_id):
    # want to return win/loss, kills, deaths, assists
    stats = [0] * 4
    participant_id = 0
    game_stats = connection.get_match_by_id(game_id)
    for player in game_stats['participantIdentities']:
        if player['player']['accountId'] == account_id:
            participant_id = player['participantId']
            break
    for player in game_stats['participants']:
        if player['participantId'] == participant_id:
            if player['stats']['win'] == True:
                stats[0] = 1
            stats[1] += player['stats']['kills']
            stats[2] += player['stats']['deaths']
            stats[3] += player['stats']['assists']
            break
    return stats

# info for summoner in index 0 of active game
summoner_1 = [''] * 4
summoner_1[0] = lobby['participants'][0]['summonerName']
summoner_1[1] = lobby['participants'][0]['summonerId']
summoner_1[2] = (connection.get_summoner_by_name(summoner_1[0]))['accountId']
summoner_1[3] = lobby['participants'][0]['championId']

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
        summoner_1_stats[4] += 1
        summoner_1_stats[0] = game[0]
        summoner_1_stats[1] = game[1]
        summoner_1_stats[2] = game[2]
        summoner_1_stats[3] = game[3]
    
summoner_1_stats.append(summoner_1_stats[4] - summoner_1_stats[0]) # add number of losses
summoner_1_stats[1] = summoner_1_stats[1] / summoner_1_stats[4] # avg kills
summoner_1_stats[2] = summoner_1_stats[2] / summoner_1_stats[4] # avg deaths
summoner_1_stats[3] = summoner_1_stats[3] / summoner_1_stats[4] # avg assists
print('%s on Selected Champion' % (summoner_1[0]))
print('Winrate: %.0f%% (%dW / %dL)' % (summoner_1_stats[0]/summoner_1_stats[4]*100,summoner_1_stats[0], summoner_1_stats[5]))
print('Average KDA: %.2f' % (summoner_1_stats[1]/summoner_1_stats[2]))
print()

# info for summoner in index 5 of active game
summoner_2 = [''] * 4
summoner_2[0] = lobby['participants'][5]['summonerName']
summoner_2[1] = lobby['participants'][5]['summonerId']
summoner_2[2] = (connection.get_summoner_by_name(summoner_1[0]))['accountId']
summoner_2[3] = lobby['participants'][5]['championId']

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
        summoner_1_stats[4] += 1
        summoner_1_stats[0] = game[0]
        summoner_1_stats[1] = game[1]
        summoner_1_stats[2] = game[2]
        summoner_1_stats[3] = game[3]
    
summoner_2_stats.append(summoner_2_stats[4] - summoner_2_stats[0]) # add number of losses
summoner_2_stats[1] = summoner_2_stats[1] / summoner_2_stats[4] # avg kills
summoner_2_stats[2] = summoner_2_stats[2] / summoner_2_stats[4] # avg deaths
summoner_2_stats[3] = summoner_2_stats[3] / summoner_2_stats[4] # avg assists
print('%s on Selected Champion' % (summoner_2[0]))
print('Winrate: %.0f%% (%dW / %dL)' % (summoner_2_stats[0]/summoner_2_stats[4]*100,summoner_2_stats[0], summoner_2_stats[5]))
print('Average KDA: %.2f' % (summoner_2_stats[1]/summoner_2_stats[2]))