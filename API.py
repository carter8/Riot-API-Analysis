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
            params=args, verify=True
        )
        return response.json()

    def get_mastery_by_summoner(self, summoner_id):
        """
        Get all champion mastery entries for a summoner ID

        :param string summoner_id:  The summoner ID

        :returns: List[ChampionMasteryDTO]: This object contains single Champion Mastery
                                            information for player and champion combination
        """
        api_url = (URLs.ChampionMasteryV4urls['base'] +
                   URLs.ChampionMasteryV4urls['by_summoner'].format(
                       encryptedSummonerId=summoner_id
                   ))
        return self._request(api_url)

    def get_mastery_by_summoner_by_champion(self, summoner_id, champion_id):
        """
        Get champion mastery entry for a summoner ID on a specific champion

        :param string summoner_id:  The summoner ID
        :param int champion_id:     Champion ID to receive mastery for

        :returns: ChampionMasteryDTO: This object contains single Champion Mastery
                                      information for player and champion combination
        """
        api_url = (URLs.ChampionMasteryV4urls['base'] +
                   URLs.ChampionMasteryV4urls['by_summoner_by_champion'].format(
                       encryptedSummonerId=summoner_id,
                       championId=champion_id
                   ))
        return self._request(api_url)

    def get_score_by_summoner(self, summoner_id):
        """
        Gets sum of player's mastery score for each champion

        :param string summoner_id:  The summoner ID

        :returns: int
        """
        api_url = (URLs.ChampionMasteryV4urls['base'] +
                   URLs.ChampionMasteryV4urls['score_by_summoner'].format(
                       encryptedSummonerId=summoner_id
                   ))
        return self._request(api_url)

    def get_champion_rotations(self):
        """
        Returns champion rotations, including free-to-play and low-level free-to-play rotations.

        :returns: ChampionInfo
        """
        api_url = URLs.ChampionV3urls['rotation']
        return self._request(api_url)

    def get_challenger_by_queue(self, queue):
        """
        Get the challenger league for a given queue

        :param string queue:  The queue to query, i.e. RANKED_SOLO_5x5

        :returns: LeagueListDTO
        """
        api_url = (URLs.LeagueV4urls['base'] +
                   URLs.LeagueV4urls['challenger_by_queue'].format(
                       queue=queue
                   ))
        return self._request(api_url)

    def get_league_by_summoner(self, summoner_id):
        """
        Get league entries in all queues for a given summoner ID

        :param string summoner_id:  The summoner ID

        :returns: Set[LeagueEntryDTO]
        """
        api_url = (URLs.LeagueV4urls['base'] +
                   URLs.LeagueV4urls['by_summoner'].format(
                       encryptedSummonerId=summoner_id
                   ))
        return self._request(api_url)

    def get_entries(self, queue, tier, division, page=1):
        """
        Get all the league entries in a given queue, tier, and division

        :param string queue:    The queue to query, i.e. RANKED_SOLO_5x5
        :param string tier:     The tier to query, i.e. GOLD
        :param string division: The division to query, i.e. IV
        :param int page:        The page for the query to paginate to. Starts at 1.

        :returns: Set[LeagueEntryDTO]
        """
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
        """
        Get the grandmaster league for a given queue

        :param string queue:  The queue to query, i.e. RANKED_SOLO_5x5

        :returns: LeagueListDTO
        """
        api_url = (URLs.LeagueV4urls['base'] +
                   URLs.LeagueV4urls['grandmaster_by_queue'].format(
                       queue=queue
                   ))
        return self._request(api_url)

    def get_league_by_id(self, league_id):
        """
        Get league with given ID, including inactive entries

        :param string league_id:  The league ID to query

        :returns: LeagueListDTO
        """
        api_url = (URLs.LeagueV4urls['base'] +
                   URLs.LeagueV4urls['by_league'].format(
                       leagueId=league_id
                   ))
        return self._request(api_url)

    def get_master_by_queue(self, queue):
        """
        Get the master league for a given queue

        :param string queue:  The queue to query, i.e. RANKED_SOLO_5x5

        :returns: LeagueListDTO
        """
        api_url = (URLs.LeagueV4urls['base'] +
                   URLs.LeagueV4urls['master_by_queue'].format(
                       queue=queue
                   ))
        return self._request(api_url)

    def get_match_by_id(self, match_id):
        """
        Get the match for a given ID

        :param int match_id:  The match ID

        :returns: MatchDto
        """
        api_url = (URLs.MatchV4urls['base'] +
                   URLs.MatchV4urls['by_match'].format(
                       matchId=match_id
                   ))
        return self._request(api_url)

    def get_matchlist_by_account(self, account_id, champion_id=None, queue=None, end_time=None, begin_time=None,
                                 end_index=None, begin_index=None):
        """
        Get matchlist for games played on given account ID and filtered using given parameters, if any

        :param string account_id:     The account ID
        :param Set[int] champion_id:  Set of champion ID's for which to filter on
        :param Set[int] queue:        Set of queues for which to filter on
        :param long end_time:         The end time to use for filtering matchlist specified
                                      as epoch milliseconds
        :param long begin_time:       The begin time to use for filtering matchlist specified
                                      as epoch milliseconds
        :param int end_index:         The end index to use for filtering matchlist
        :param int begin_index:       The begin index to use for filtering matchlist

        :returns: MatchlistDto
        """
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
        """
        Get the match timeline for a given match ID

        :param int match_id:  The match ID

        :returns: MatchTimelineDto
        """
        api_url = (URLs.MatchV4urls['base'] +
                   URLs.MatchV4urls['timeline_by_match'].format(
                       matchId=match_id
                   ))
        return self._request(api_url)

    def get_active_games_by_summoner(self, summoner_id):
        """
        Get current game information for the given summoner

        :param string summoner_id:  The summoner ID

        :returns: CurrentGameInfo
        """
        api_url = (URLs.SpectatorV4urls['base'] +
                   URLs.SpectatorV4urls['by_summoner'].format(
                       encryptedSummonerId=summoner_id
                   ))
        return self._request(api_url)

    def get_featured_games(self):
        """
        Get list of featured games

        :returns: FeaturedGames
        """
        api_url = (URLs.SpectatorV4urls['base'] +
                   URLs.SpectatorV4urls['featured_games'])
        return self._request(api_url)

    def get_summoner_by_account(self, account_id):
        """
        Get a summoner by account ID

        :param string account_id:  The account ID

        :returns: SummonerDTO
        """
        api_url = (URLs.SummonerV4urls['base'] +
                   URLs.SummonerV4urls['by_account'].format(
                       encryptedAccountId=account_id
                   ))
        return self._request(api_url)

    def get_summoner_by_name(self, summoner_name):
        """
        Get a summoner by summoner name

        :param string summoner_name:  The summoner name

        :returns: SummonerDTO
        """
        api_url = (URLs.SummonerV4urls['base'] +
                   URLs.SummonerV4urls['by_name'].format(
                       summonerName=summoner_name
                   ))
        return self._request(api_url)

    def get_summoner_by_puuid(self, puuid):
        """
        Get a summoner by PUUID

        :param string puuid:  PUUID

        :returns: SummonerDTO
        """
        api_url = (URLs.SummonerV4urls['base'] +
                   URLs.SummonerV4urls['by_puuid'].format(
                       encryptedPUUID=puuid
                   ))
        return self._request(api_url)

    def get_summoner_by_id(self, summoner_id):
        """
        Get a summoner by summoner ID

        :param string summoner_id:  The summoner ID

        :returns: SummonerDTO
        """
        api_url = (URLs.SummonerV4urls['base'] +
                   URLs.SummonerV4urls['by_id'].format(
                       encryptedSummonerId=summoner_id
                   ))
        return self._request(api_url)
