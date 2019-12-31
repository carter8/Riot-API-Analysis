import requests
import URLs

class RiotAPI(object):

	def __init__(self, api_key, region=URLs.REGIONS['north_america']):
		self.api_key = api_key
		self.region = region
	
	def _request(self, api_url, params={}):
		args = {'api_key': self.api_key}
		for key, value in params.items():
			if key not in args:
				args[key] = value
		response = requests.get(
			URLs.BASE_URL.format(
				proxy=self.region,
				url=api_url
				),
			params=args,verify=True
			)
		return response.json()
	
	def get_mastery_by_summoner(self, summoner_id):
		api_url = (URLs.ChampionMasteryV4urls['base'] +
			URLs.ChampionMasteryV4urls['by_summoner'].format(
				encryptedSummonerId=summoner_id
				))
		return self._request(api_url)
		
	def get_mastery_by_summoner_by_champion(self, summoner_id, champion_id):
		api_url = (URLs.ChampionMasteryV4urls['base'] +
			URLs.ChampionMasteryV4urls['by_summoner_by_champion'].format(
				encryptedSummonerId=summoner_id,
				championId=champion_id
				))
		return self._request(api_url)
		
	def get_score_by_summoner(self, summoner_id):
		api_url = (URLs.ChampionMasteryV4urls['base'] +
			URLs.ChampionMasteryV4urls['score_by_summoner'].format(
				encryptedSummonerId=summoner_id
				))
		return self._request(api_url)
		
	def get_champion_rotations(self):
		api_url = URLs.ChampionV3urls['rotation']
		return self._request(api_url)
		
	def get_challenger_by_queue(self, queue):
	# get the challenger league for a given queue
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['challenger_by_queue'].format(
				queue=queue
				))
		return self._request(api_url)
		
	def get_league_by_summoner(self, summoner_id):
	# get league entries in all queues for a given summoner ID
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['by_summoner'].format(
				encryptedSummonerId=summoner_id
				))
		return self._request(api_url)
		
	def get_entries(self, queue, tier, division, page=None):
	# get all the league entries in a given queue, tier, and division
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['entries_by_queue_tier_division'].format(
				queue=queue,
				tier=tier,
				division=division
				))
		args = {}
		if page is not None:
			args['page'] = page
		return self._request(api_url, args)
	
	def get_grandmaster_by_queue(self, queue):
	# get the grandmaster league for a given queue
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['grandmaster_by_queue'].format(
				queue=queue
				))
		return self._request(api_url)
		
	def get_league_by_id(self, league_id):
	# get the league with a given ID
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['by_league'].format(
				leagueId=league_id
				))
		return self._request(api_url)
		
	def get_master_by_queue(self, queue):
	# get the master league for a given queue
		api_url = (URLs.LeagueV4urls['base'] +
			URLs.LeagueV4urls['master_by_queue'].format(
				queue=queue
				))
		return self._request(api_url)
		
	def get_match_by_id(self, match_id):
	# get the match for a given ID
		api_url = (URLs.MatchV4urls['base'] +
			URLs.MatchV4urls['by_match'].format(
				matchId=match_id
				))
		return self._request(api_url)
		
	def get_matchlist_by_account(self, account_id, champion_id=None, queue=None, end_time=None, begin_time=None, end_index=None, begin_index=None):
	# get matchlist for games played on given account ID and filtered using given parameters, if any
		api_url = (URLs.MatchV4urls['base'] +
			URLs.MatchV4urls['matchlist_by_account'].format(
				encryptedAccountId=account_id
				))
		args = {}
		if champion_id is not None:
			args['champion'] = champion_id
		if queue is not None:
			args['queue'] = queue
		if end_time is not None:
			args['endTime'] = end_time
		if begin_time is not None:
			args['beginTime'] = begin_time
		if end_index is not None:
			args['endIndex'] = end_index
		if begin_index is not None:
			args['beginIndex'] = begin_index
		return self._request(api_url, args)
		
	def get_timeline_by_id(self, match_id):
	# get the match timeline for a given ID
		api_url = (URLs.MatchV4urls['base'] +
			URLs.MatchV4urls['timeline_by_match'].format(
				matchId=match_id
				))
		return self._request(api_url)
		
	def get_active_games_by_summoner(self, summoner_id):
	# get current game information for the given summoner
		api_url = (URLs.SpectatorV4urls['base'] +
			URLs.SpectatorV4urls['by_summoner'].format(
				encryptedSummonerId=summoner_id
				))
		return self._request(api_url)
	
	def get_featured_games(self):
	# get list of featured games
		api_url = (URLs.SpectatorV4urls['base'] +
			URLs.SpectatorV4urls['featured_games'])
		return self._request(api_url)
		
	def get_summoner_by_account(self, account_id):
	# get a summoner by account ID
		api_url = (URLs.SummonerV4urls['base'] +
			URLs.SummonerV4urls['by_account'].format(
				encryptedAccountId=account_id
				))
		return self._request(api_url)
		
	def get_summoner_by_name(self, summoner_name):
	# get a summoner by summoner name
		api_url = (URLs.SummonerV4urls['base'] +
			URLs.SummonerV4urls['by_name'].format(
				summonerName=summoner_name
				))
		return self._request(api_url)
		
	def get_summoner_by_puuid(self, puuid):
	# get a summoner by PUUID
		api_url = (URLs.SummonerV4urls['base'] +
			URLs.SummonerV4urls['by_puuid'].format(
				encryptedPUUID=puuid
				))
		return self._request(api_url)	
		
	def get_summoner_by_id(self, summoner_id):
	# get a summoner by summoner ID
		api_url = (URLs.SummonerV4urls['base'] +
			URLs.SummonerV4urls['by_id'].format(
				encryptedSummonerId=summoner_id
				))
		return self._request(api_url)