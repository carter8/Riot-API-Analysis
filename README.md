# Riot-API-Analysis
Riot API Analysis is a project to explore the available Riot Games API focusing on the video game "League of Legends"

Contents:
- URLs.py contains dictionaries of constants which includes all of the URLs in which data can be obtained from the Riot Games API.

- API.py contains the RiotAPI object which has functions to access all available League of Legends data from the Riot API utilizing the "requests" module. A RiotAPI object is initialized with an API key that can be generated at developer.riotgames.com and is used as a necessary parameter to request the data.

- SummonerLookup.py is a script to lookup a specific summoner/player by user name and get stats and information about them which includes win rate and KDA on each game mode they play.

- SummonerLookupFunctions.py contains functions for retrieving and combining game stats from the Riot API and other useful functions for processing data from the API.

- LoadingScreenPreview.py is a script to lookup and analyze each player in an active game. It finds the active game for a particular username and is meant to be ran in the loading screen in order to identify strengths and weaknesses for other players in the game.

- ActiveGameFunctions.py contains functions to retrieve player stats and information from the current game information that is obtained from the Riot API. ActiveGameFunctions also contains a function to iterate through these stats and print out analysis.
