import API

# gives win rate and KDA for each queue

api_key = 'RGAPI-8c9357f7-5447-451b-9da0-3b33922a97ad' # expires in 24hrs, generated at: developer.riotgames.com
summoner_name = 'the carter iii'
max_games = 90 # cannot be larger than 98

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

matchlist = connection.get_matchlist_by_account(summoner['accountId'])

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
	

# iterate through matchlist
# limiting to 50 matches. api key has a rate limit of 100 requests every 2 mins
urf_stats = [0] * 5
aram_stats = [0] * 5
blind_stats = [0] * 5
draft_stats = [0] * 5
ranked_stats = [0] * 5
ranked_flex_stats = [0] * 5
total_games = 0
for match in matchlist['matches']:
	total_games += 1
	if total_games > max_games:
		break
	if match['queue'] == 430:
		# unranked blind pick
		blind = get_game_stats(match['gameId'], summoner['accountId'])
		blind_stats[4] += 1
		blind_stats[0] += blind[0]
		blind_stats[1] += blind[1]
		blind_stats[2] += blind[2]
		blind_stats[3] += blind[3]
	elif match['queue'] == 450:
		# ARAM
		aram = get_game_stats(match['gameId'], summoner['accountId'])
		aram_stats[4] += 1
		aram_stats[0] += aram[0]
		aram_stats[1] += aram[1]
		aram_stats[2] += aram[2]
		aram_stats[3] += aram[3]
	elif match['queue'] == 400:
		# unranked draft pick
		draft = get_game_stats(match['gameId'], summoner['accountId'])
		draft_stats[4] += 1
		draft_stats[0] += draft[0]
		draft_stats[1] += draft[1]
		draft_stats[2] += draft[2]
		draft_stats[3] += draft[3]
	elif match['queue'] == 420:
		# ranked solo/duo pick
		ranked = get_game_stats(match['gameId'], summoner['accountId'])
		ranked_stats[4] += 1
		ranked_stats[0] += ranked[0]
		ranked_stats[1] += ranked[1]
		ranked_stats[2] += ranked[2]
		ranked_stats[3] += ranked[3]
	elif match['queue'] == 440:
		# ranked flex pick
		ranked_flex = get_game_stats(match['gameId'], summoner['accountId'])
		ranked_flex_stats[4] += 1
		ranked_flex_stats[0] += ranked_flex[0]
		ranked_flex_stats[1] += ranked_flex[1]
		ranked_flex_stats[2] += ranked_flex[2]
		ranked_flex_stats[3] += ranked_flex[3]
	elif match['queue'] == 900:
		# URF
		urf = get_game_stats(match['gameId'], summoner['accountId'])
		urf_stats[4] += 1
		urf_stats[0] += urf[0]
		urf_stats[1] += urf[1]
		urf_stats[2] += urf[2]
		urf_stats[3] += urf[3]
	else:
		print('Queue not coded. Queue #: %d' % match['queue'])
		
		
# calculate total stats and print queue summaries
total_stats = [0] * 5

print('Stats for %s:\n' % (summoner['name']))

if urf_stats[4] != 0:
	total_stats[0] += urf_stats[0]
	total_stats[1] += urf_stats[1]
	total_stats[2] += urf_stats[2]
	total_stats[3] += urf_stats[3]
	total_stats[4] += urf_stats[4]
	urf_stats.append(urf_stats[4] - urf_stats[0]) # add number of losses
	urf_stats[1] = urf_stats[1] / urf_stats[4] # avg kills
	urf_stats[2] = urf_stats[2] / urf_stats[4] # avg deaths
	urf_stats[3] = urf_stats[3] / urf_stats[4] # avg assists
	print('URF | Winrate: %.0f%% (%dW / %dL)' % (urf_stats[0]/urf_stats[4]*100,urf_stats[0], urf_stats[5]))
	print('Average KDA: %.2f' % (urf_stats[1]/urf_stats[2]))
	print()
	
if aram_stats[4] != 0:
	total_stats[0] += aram_stats[0]
	total_stats[1] += aram_stats[1]
	total_stats[2] += aram_stats[2]
	total_stats[3] += aram_stats[3]
	total_stats[4] += aram_stats[4]
	aram_stats.append(aram_stats[4] - aram_stats[0]) # add number of losses
	aram_stats[1] = aram_stats[1] / aram_stats[4] # avg kills
	aram_stats[2] = aram_stats[2] / aram_stats[4] # avg deaths
	aram_stats[3] = aram_stats[3] / aram_stats[4] # avg assists
	print('ARAM | Winrate: %.0f%% (%dW / %dL)' % (aram_stats[0]/aram_stats[4]*100,aram_stats[0], aram_stats[5]))
	print('Average KDA: %.2f' % (aram_stats[1]/aram_stats[2]))
	print()
	
if blind_stats[4] != 0:
	total_stats[0] += blind_stats[0]
	total_stats[1] += blind_stats[1]
	total_stats[2] += blind_stats[2]
	total_stats[3] += blind_stats[3]
	total_stats[4] += blind_stats[4]
	blind_stats.append(blind_stats[4] - blind_stats[0]) # add number of losses
	blind_stats[1] = blind_stats[1] / blind_stats[4] # avg kills
	blind_stats[2] = blind_stats[2] / blind_stats[4] # avg deaths
	blind_stats[3] = blind_stats[3] / blind_stats[4] # avg assists
	print('Blind Pick | Winrate: %.0f%% (%dW / %dL)' % (blind_stats[0]/blind_stats[4]*100,blind_stats[0], blind_stats[5]))
	print('Average KDA: %.2f' % (blind_stats[1]/blind_stats[2]))
	print()
	
if draft_stats[4] != 0:
	total_stats[0] += draft_stats[0]
	total_stats[1] += draft_stats[1]
	total_stats[2] += draft_stats[2]
	total_stats[3] += draft_stats[3]
	total_stats[4] += draft_stats[4]
	draft_stats.append(draft_stats[4] - draft_stats[0]) # add number of losses
	draft_stats[1] = draft_stats[1] / draft_stats[4] # avg kills
	draft_stats[2] = draft_stats[2] / draft_stats[4] # avg deaths
	draft_stats[3] = draft_stats[3] / draft_stats[4] # avg assists
	print('Draft Pick | Winrate: %.0f%% (%dW / %dL)' % (draft_stats[0]/draft_stats[4]*100,draft_stats[0], draft_stats[5]))
	print('Average KDA: %.2f' % (draft_stats[1]/draft_stats[2]))
	print()
	
if ranked_flex_stats[4] != 0:
	total_stats[0] += ranked_flex_stats[0]
	total_stats[1] += ranked_flex_stats[1]
	total_stats[2] += ranked_flex_stats[2]
	total_stats[3] += ranked_flex_stats[3]
	total_stats[4] += ranked_flex_stats[4]
	ranked_flex_stats.append(ranked_flex_stats[4] - ranked_flex_stats[0]) # add number of losses
	ranked_flex_stats[1] = ranked_flex_stats[1] / ranked_flex_stats[4] # avg kills
	ranked_flex_stats[2] = ranked_flex_stats[2] / ranked_flex_stats[4] # avg deaths
	ranked_flex_stats[3] = ranked_flex_stats[3] / ranked_flex_stats[4] # avg assists
	print('Ranked Flex | Winrate: %.0f%% (%dW / %dL)' % (ranked_flex_stats[0]/ranked_flex_stats[4]*100,ranked_flex_stats[0], ranked_flex_stats[5]))
	print('Average KDA: %.2f' % (ranked_flex_stats[1]/ranked_flex_stats[2]))
	print()
	
if ranked_stats[4] != 0:
	total_stats[0] += ranked_stats[0]
	total_stats[1] += ranked_stats[1]
	total_stats[2] += ranked_stats[2]
	total_stats[3] += ranked_stats[3]
	total_stats[4] += ranked_stats[4]
	ranked_stats.append(ranked_stats[4] - ranked_stats[0]) # add number of losses
	ranked_stats[1] = ranked_stats[1] / ranked_stats[4] # avg kills
	ranked_stats[2] = ranked_stats[2] / ranked_stats[4] # avg deaths
	ranked_stats[3] = ranked_stats[3] / ranked_stats[4] # avg assists
	print('Ranked Solo/Duo | Winrate: %.0f%% (%dW / %dL)' % (ranked_stats[0]/ranked_stats[4]*100,ranked_stats[0], ranked_stats[5]))
	print('Average KDA: %.2f' % (ranked_stats[1]/ranked_stats[2]))
	print()

total_stats.append(total_stats[4] - total_stats[0]) # add number of losses
total_stats[1] = total_stats[1] / total_stats[4] # avg kills
total_stats[2] = total_stats[2] / total_stats[4] # avg deaths
total_stats[3] = total_stats[3] / total_stats[4] # avg assists
print('Total Winrate: %.0f%% (%dW / %dL)' % (total_stats[0]/total_stats[4]*100,total_stats[0], total_stats[5]))
print('Average KDA: %.2f' % (total_stats[1]/total_stats[2]))