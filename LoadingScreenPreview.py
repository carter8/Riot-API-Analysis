"""
This script analyzes every player in an active game, and gives warnings if a player
has never played their champion before or does not play the game mode often.

It then prints out a summary for each team giving the champion level and score for
each player, how often the player plays the game mode, and the player's ranked league
if they play ranked.

This is meant to be ran during the loading screen, but can also be ran during the game.
It does not work in pre game lobby as the active game is created upon entering loading
screen.

To get the active game analysis for a different player, simply change the summoner name
"""

import API
from ActiveGameFunctions import analyze_active_game

# api key is generated at developer.riotgames.com
# expires 24 hours after generation
api_key = 'INSERT-API-KEY-HERE'

# your summoner name, to analyze the other players in your game
summoner_name = 'The Carter III'

connection = API.RiotAPI(api_key)

# get summoner info for desired name
summoner = connection.get_summoner_by_name(summoner_name)

# gets the info for each summoner in the active game
# active game information is only available during the loading screen and actual game
active_game = connection.get_active_games_by_summoner(summoner['id'])

# analyze the active_game depending on the game mode
if active_game['gameMode'] == 'CLASSIC':
    analyze_active_game(active_game, connection, (400, 420, 430, 440), 'Summoner\'s Rift')
    print('CLASSIC game mode not yet coded')
elif active_game['gameMode'] == 'ARAM':
    analyze_active_game(active_game, connection, (450,), 'ARAM')
elif active_game['gameMode'] == 'KINGPORO':
    analyze_active_game(active_game, connection, (920,), 'Poro King')
else:
    print('Game mode: %s is not coded.' % active_game['gameMode'])
