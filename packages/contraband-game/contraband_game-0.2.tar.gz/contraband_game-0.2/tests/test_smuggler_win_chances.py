from contraband_game.signups import SignUps
from contraband_game.teams import Teams
from contraband_game.gamesettings import GameSettings
from contraband_game.banks import Banks
from contraband_game.game import Game
import random


    
    
    
    
def test_smuggler_win_chances_south():
    
    """Testing winning chances of a southern smuggler against a northern inspector"""
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks = Banks(test_signups,test_teams,test_gamesettings)


    test_banks.southern_bankaccount_third_country()
    inital_val = 200_000_000
    amounts_updates_list = []
    test_gamesettings.smuggling_amount = 100_000_000
    test_gamesettings.security_amount = 50_000_000
    num_of_scenarios = 4
    
    
    
    #--First scenario--#
    
    test_gamesettings.smuggler =  "Lupin" # different southern smuggler's names have been used to avoid updating amount of the same smuggler during the test of the mutiple scenarios.
    test_gamesettings.smuggler_win = True
    test_gamesettings.sec_amount_win = True
    
    test_banks.money_update_as_southern_smuggler()
    amounts_updates_list.append(test_banks.southern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.smuggler_win = False
    test_gamesettings.sec_amount_win = False 
    
    #--Second scenario--#
        
    test_gamesettings.smuggler =  "Clyde"
    test_gamesettings.sec_amount_win = True
    
    test_banks.money_update_as_southern_smuggler()
    amounts_updates_list.append(test_banks.southern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.sec_amount_win = False  
        
    #---Third scenario--#
    
    test_gamesettings.smuggler =  "C.Ponzi"       
    test_gamesettings.inspector_win = True
            
    test_banks.money_update_as_southern_smuggler()
    amounts_updates_list.append(test_banks.southern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.inspector_win = False
         
    #--Fourth scenario--#
    
    test_gamesettings.smuggler =  "Jordan Belfort"      
    test_gamesettings.smuggler_win = True
    
    test_banks.money_update_as_southern_smuggler()
    amounts_updates_list.append(test_banks.southern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.smuggler_win = False
        
    winning_chances_south_smuggler = len([ amounts for amounts in amounts_updates_list if amounts > inital_val])

    
    assert winning_chances_south_smuggler == 3
    assert num_of_scenarios == 4
            
       
            
            


    
def test_smuggler_win_chances_north():
    
    """Testing winning chances of a northern smuggler against a southern inspector"""
    
    test_signups = SignUps()
    test_teams = Teams(test_signups)
    test_gamesettings = GameSettings(test_teams)
    test_banks = Banks(test_signups,test_teams,test_gamesettings)


    test_banks.northern_bankaccount_third_country()
    inital_val = 200_000_000
    amounts_updates_list = []
    test_gamesettings.smuggling_amount = 100_000_000
    test_gamesettings.security_amount = 50_000_000
    num_of_scenarios = 4
    
    
    
    #--First scenario--#
    
    test_gamesettings.smuggler =  "Maradona"
    test_gamesettings.smuggler_win = True
    test_gamesettings.sec_amount_win = True
    
    test_banks.money_update_as_northern_smuggler()
    amounts_updates_list.append(test_banks.northern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.smuggler_win = False
    test_gamesettings.sec_amount_win = False 
    
    
    #--Second scenario--#
        
    test_gamesettings.smuggler =  "Diddy"
    test_gamesettings.sec_amount_win = True
    
    test_banks.money_update_as_northern_smuggler()
    amounts_updates_list.append(test_banks.northern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.sec_amount_win = False  
        
    #---Third scenario--#
    
    test_gamesettings.smuggler =  "Ted Bundy"       
    test_gamesettings.inspector_win = True
            
    test_banks.money_update_as_northern_smuggler()
    amounts_updates_list.append(test_banks.northern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.inspector_win = False
         
    #--Fourth scenario--#
    
    test_gamesettings.smuggler =  "Berlusconi"     
    test_gamesettings.smuggler_win = True
    
    test_banks.money_update_as_northern_smuggler()
    amounts_updates_list.append(test_banks.northern_country_personal_bankaccounts[test_gamesettings.smuggler])
    
    test_gamesettings.smuggler_win = False
        
    winning_chances_north_smuggler = len([ amounts for amounts in amounts_updates_list if amounts > inital_val])

    
    assert winning_chances_north_smuggler == 3
    assert num_of_scenarios == 4