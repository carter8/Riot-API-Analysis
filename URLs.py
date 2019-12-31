BASE_URL = 'https://{proxy}.api.riotgames.com/{url}'

REGIONS = {
    'north_america' : 'na1',
    'europe_nordic_and_east' : 'eun1',
    'europe_west' : 'euw1',
    'korea' : 'kr'
}

ChampionMasteryV4urls = {
    'base' : 'lol/champion-mastery/v4',
    'by_summoner' : '/champion-masteries/by-summoner/{encryptedSummonerId}',
    'by_summoner_by_champion' : '/champion-masteries/by-summoner/{encryptedSummonerId}/by-champion/{championId}',
    'score_by_summoner' : '/scores/by-summoner/{encryptedSummonerId}'
}

ChampionV3urls = {
	'rotation' : 'lol/platform/v3/champion-rotations'
}

LeagueV4urls = {
	'base' : 'lol/league/v4',
	'challenger_by_queue' : '/challengerleagues/by-queue/{queue}',
	'by_summoner' : '/entries/by-summoner/{encryptedSummonerId}',
	'entries_by_queue_tier_division' : '/entries/{queue}/{tier}/{division}',
	'grandmaster_by_queue' : '/grandmasterleagues/by-queue/{queue}',
	'by_league' : '/leagues/{leagueId}',
	'master_by_queue' : 'masterleagues/by-queue/{queue}'
}

MatchV4urls = {
	'base' : 'lol/match/v4',
	'by_match' : '/matches/{matchId}',
	'matchlist_by_account' : '/matchlists/by-account/{encryptedAccountId}',
	'timeline_by_match' : '/timelines/by-match/{matchId}'
}

SpectatorV4urls = {
	'base' : 'lol/spectator/v4',
	'by_summoner' : '/active-games/by-summoner/{encryptedSummonerId}',
	'featured_games' : '/featured-games'
}

SummonerV4urls = {
	'base' : 'lol/summoner/v4/summoners',
	'by_account' : '/by-account/{encryptedAccountId}',
	'by_name' : '/by-name/{summonerName}',
	'by_puuid' : '/by-puuid/{encryptedPUUID}',
	'by_id' : '/{encryptedSummonerId}'
}