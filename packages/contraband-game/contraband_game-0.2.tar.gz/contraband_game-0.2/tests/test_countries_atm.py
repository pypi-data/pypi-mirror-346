from contraband_game.signups import SignUps
from contraband_game.teams import Teams
from contraband_game.gamesettings import GameSettings
from contraband_game.banks import Banks
import random




def test_countries_personal_ba():
    
    """Testing the amount of each players'initial loan is equal to 300 million"""
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks = Banks(test_signups,test_teams,test_gamesettings)
    
    test_banks.northern_atm()
    test_banks.southern_atm()
    
    test_north_atm = test_banks.northern_atm_bankaccounts
    test_south_atm = test_banks.southern_atm_bankaccounts
    
    united_atm_country_dict = test_north_atm
    united_atm_country_dict.update(test_south_atm)
    
    for key_names in united_atm_country_dict.keys():
        assert united_atm_country_dict[key_names] == 300_000_000
 
   
def test_atm_withdrawal_north():
    
    """Testing withdrawal from northern atm does not exceed the amount of 100 million"""
    
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks_atm = Banks(test_signups,test_teams,test_gamesettings)
    
    northern_players_list = test_teams.northern_country_players()
    southern_players_list = test_teams.southern_country_players()
        
    test_gamesettings.smuggler = random.choice(northern_players_list)
    smuggling_amount_limit = range(1,100_000_000)
    initial_players_loaned_amount =  300_000_000
    
    test_gamesettings.the_smuggler()
    
    if test_gamesettings.smuggler in northern_players_list:
        test_banks_atm.northern_atm()
        
        if initial_players_loaned_amount - test_banks_atm.northern_atm_bankaccounts[test_gamesettings.smuggler]  == test_gamesettings.smuggling_amount:
           assert test_gamesettings.smuggling_amount in smuggling_amount_limit
        
        else:
            print(f"{test_gamesettings.smuggling_amount:,} Smuggling amount exceeded the settled limit")
        
    
    else:
         assert test_gamesettings.smuggler in southern_players_list
         
         


def test_atm_withdrawal_south():
    
    """Testing withdrawal from northern atm does not exceed the amount of 100 million"""
    
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks_atm = Banks(test_signups,test_teams,test_gamesettings)
    
    northern_players_list = test_teams.northern_country_players()
    southern_players_list = test_teams.southern_country_players()
        
    test_gamesettings.smuggler = random.choice(northern_players_list)
    smuggling_amount_limit = range(1,100_000_000)
    initial_players_loaned_amount =  300_000_000
    
    test_gamesettings.the_smuggler()
    
    if test_gamesettings.smuggler in southern_players_list:
        test_banks_atm.southern_atm()
        
        if initial_players_loaned_amount - test_banks_atm.southern_atm_bankaccounts[test_gamesettings.smuggler]  == test_gamesettings.smuggling_amount:
           assert test_gamesettings.smuggling_amount in smuggling_amount_limit
        
        else:
            print(f"{test_gamesettings.smuggling_amount:,} Smuggling amount exceeded the settled limit")
        
    
    else:
         assert test_gamesettings.smuggler in northern_players_list
        
 



           
    

