from contraband_game.signups import SignUps
from contraband_game.teams import Teams
from contraband_game.gamesettings import GameSettings
from contraband_game.banks import Banks
from contraband_game.game import Game
import pkg_resources


def test_game_turns():
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks = Banks(test_signups,test_teams,test_gamesettings)
    test_game = Game()
    
    test_signups.data_path_players = pkg_resources.resource_filename('contraband_game', 'data/players.json')
    
    test_game.games(test_signups)
    assert test_game.game <= 25