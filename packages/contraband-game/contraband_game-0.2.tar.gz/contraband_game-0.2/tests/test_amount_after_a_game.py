from contraband_game.signups import SignUps
from contraband_game.teams import Teams
from contraband_game.gamesettings import GameSettings
from contraband_game.banks import Banks



def test_amount_after_a_game():
    
    """Testing update of values from both the smuggler and inspector perspectives as a game ends."""
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks = Banks(test_signups,test_teams,test_gamesettings)
    
    test_gamesettings.smuggler = "Lupin"
    test_gamesettings.inspector = "Maradona"
    test_gamesettings.smuggling_amount = 100_000_000
    test_gamesettings.smuggler_win = True
    
    inital_val = 200_000_000
    
    test_banks.southern_bankaccount_third_country()
    test_banks.northern_bankaccount_third_country()
    
    test_banks.money_update_as_southern_smuggler()
    test_banks.money_update_as_northern_inspector()
    
    
    assert test_banks.southern_country_personal_bankaccounts[test_gamesettings.smuggler] > inital_val
    assert test_banks.northern_country_personal_bankaccounts[test_gamesettings.inspector] < inital_val
    
    test_gamesettings.smuggler = "Berlusconi"
    test_gamesettings.inspector = "Jordan Belfort"
    
    test_banks.money_update_as_northern_smuggler()
    test_banks.money_update_as_southern_inspector()
    
    assert test_banks.northern_country_personal_bankaccounts[test_gamesettings.smuggler] > inital_val
    assert test_banks.southern_country_personal_bankaccounts[test_gamesettings.inspector] < inital_val
    