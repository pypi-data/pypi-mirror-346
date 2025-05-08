from .teams import Teams
from .signups import SignUps
from .gamesettings import GameSettings
from .banks import Banks
import random



class Game():
    
    def __init__(self):
        
        self.set_list = None
        self.game = None
    
    
    def random_player_set(self,list_par):
   
        
        while True:
            choice = random.choice(list_par)
            
            if choice not in self.set_list:
                self.set_list.add(choice)
                return choice
            
            elif len(self.set_list) == 10:
                self.set_list.clear()
                continue
            else:
                continue
 
    
    def games(self,sign_in):
    
        """General game setting, bare in mind the money are smuggled with a trunk but it is not in this game"""
        
        self.set_list = set()
        
        # Teams class instance where the log in of the gamer is passed as an argument
        teams_instance = Teams(sign_in)
            
        # Generating players from gamer user credentials. 1 if one player wants to play or multiple.
        teams_instance.player_generator()
            
         # adding teams as argument so players can be accessed in the class
        game_settings_instance = GameSettings(teams_instance)
            
        banks_instance = Banks(sign_in,teams_instance,game_settings_instance)
        banks_instance.northern_bankaccount_third_country()
        banks_instance.southern_bankaccount_third_country()
        
        
        
        
       # Bear in mind the turn in a game are 4
        for self.game in range(25,0,-1):
            
            
            # Initialising the class on the instance variable which will generate a random player from the southern country. Now the instance variable will have the same value throughout the all functions of the class if present in the following call of a function.
            game_settings_instance.smuggler = self.random_player_set(teams_instance.southern_country_players())
            print(f" The smuggler of the Southern team is: {game_settings_instance.smuggler}")
            
            game_settings_instance.inspector = self.random_player_set(teams_instance.northern_country_players())
            print(f" The inspector of the Northern team is: { game_settings_instance.inspector}")
            
            
            game_settings_instance.the_smuggler()
            banks_instance.southern_atm()
            
            if banks_instance.northern_country_personal_bankaccounts[game_settings_instance.inspector] <= 0:
                game_settings_instance.pass_declaration()
            else:    
                game_settings_instance.the_inspector()
            
                if game_settings_instance.doubt_investigation is True:
                    
                    banks_instance.security_amount_condition_northern()
                    game_settings_instance.doubt_declaration_aftermath()
        
                else:
                    pass
                
            banks_instance.money_update_as_southern_smuggler()
            banks_instance.money_update_as_northern_inspector()
            
            game_settings_instance.doubt_investigation = False
            game_settings_instance.smuggler_win = False
            game_settings_instance.sec_amount_win = False
            game_settings_instance.inspector_win = False
            
            
            game_settings_instance.smuggler = self.random_player_set(teams_instance.northern_country_players())
            print(f" the smuggler of the Northern team is { game_settings_instance.smuggler}")
            
            game_settings_instance.inspector = self.random_player_set(teams_instance.southern_country_players())
            print(f" the inspector of the Southern team is: { game_settings_instance.inspector}")
            
            game_settings_instance.the_smuggler()
            banks_instance.northern_atm()
            
            
            if banks_instance.southern_country_personal_bankaccounts[game_settings_instance.inspector] <= 0:
                game_settings_instance.pass_declaration()
            else:    
                game_settings_instance.the_inspector()
                if game_settings_instance.doubt_investigation is True:

                    banks_instance.security_amount_condition_southern()
                    game_settings_instance.doubt_declaration_aftermath()
                else:
                 pass
            
            
            banks_instance.money_update_as_northern_smuggler()
            banks_instance.money_update_as_southern_inspector()
            
            game_settings_instance.doubt_investigation = False
            game_settings_instance.smuggler_win = False
            game_settings_instance.sec_amount_win = False
            game_settings_instance.inspector_win = False
            
            
            print(f"{self.game - 1} game(s) remaining.\n")
            
            # Print statement return bank transitions. Not needed in the game but if in case of uncertainty it's suggested the use of it.
            # print(f"{banks_instance.northern_country_personal_bankaccounts}") 
            # print(f"{banks_instance.southern_country_personal_bankaccounts}")
            
            if self.game == 1:
                self.final_personal_ba_northern = banks_instance.northern_country_personal_bankaccounts 
                self.final_personal_ba_southern = banks_instance.southern_country_personal_bankaccounts 
                self.final_amount_northern_atm = banks_instance.northern_atm_bankaccounts
                self.final_amount_southern_atm = banks_instance.southern_atm_bankaccounts
         
        print("Game Over!")
        
        if sum(self.final_personal_ba_northern.values()) > sum(self.final_personal_ba_southern.values()):
            print(f"with the total amount of {sum(self.final_personal_ba_northern.values()):,} the northern country wins the round!!!🥳")
        else:
         print(f"with the total amount of {sum(self.final_personal_ba_northern.values()):,} the southern country wins the round!!!🥳")
         
  
    
    def game_aftermath(self):
        
        """Aftermath of the game, deducting the initial loans, spitting remaining money inside atms to the opposing country, declaring the player with the most money and the ones in dept"""
        
        self.northern_atm_aftermath = self.final_amount_northern_atm
        self.southern_atm_aftermath = self.final_amount_southern_atm
        
        self.northern_personal_account_aftermath = self.final_personal_ba_northern
        self.southern_personal_account_aftermath = self.final_personal_ba_southern
    
        
        all_values = []

        for northern_remaining_money in self.northern_personal_account_aftermath.keys():
            
            self.northern_personal_account_aftermath[northern_remaining_money] -= 400_000_000
            
        self.tot_northern_atm_aftermath = sum(self.northern_atm_aftermath.values())
    
        print(f"after the end of the round the total amount of the northern atm is {self.tot_northern_atm_aftermath:,}")
            
        if self.tot_northern_atm_aftermath > 0:
            
            for keys_personal_accounts_south in self.southern_personal_account_aftermath.keys():
                
                val_personal_accounts = self.southern_personal_account_aftermath[keys_personal_accounts_south]
                money_splitted_from_north_atm = self.tot_northern_atm_aftermath / 5
                
                self.southern_personal_account_aftermath[keys_personal_accounts_south] = int(val_personal_accounts) + int(money_splitted_from_north_atm)
                
        else:
            print(f" SOUTHERN COUNTRY FINAL PERSONAL AMOUNT: {self.southern_personal_account_aftermath} No money was left in the northern atm")
                
                    
        for southern_remaining_money in self.southern_personal_account_aftermath.keys():
            
            self.southern_personal_account_aftermath[southern_remaining_money] -= 400_000_000
        self.tot_southern_atm_aftermath = sum(self.southern_atm_aftermath.values())
         
        print(f"after the end of the round the total amount of the southern atm is {self.tot_southern_atm_aftermath:,}")
            
        if self.tot_southern_atm_aftermath > 0:
            
            for keys_personal_accounts_north in self.northern_personal_account_aftermath.keys():
                
                val_personal_accounts = self.northern_personal_account_aftermath[keys_personal_accounts_north]
                money_splitted_from_south_atm = self.tot_southern_atm_aftermath / 5
                
                self.northern_personal_account_aftermath[keys_personal_accounts_north] = int(val_personal_accounts) + int(money_splitted_from_south_atm)
                
        else:   
            print(f"NORTHERN COUNTRY FINAL PERSONAL AMOUNT:{self.northern_personal_account_aftermath} No money was left in the southern atm")       
        
        print(f"NORTHERN COUNTRY FINAL PERSONAL AMOUNT: {self.northern_personal_account_aftermath} £ \n the additional amount is derived from the money not smuggled in southern country atm") 
        print(f" SOUTHERN COUNTRY FINAL PERSONAL AMOUNT:{self.southern_personal_account_aftermath} £ \n the additional amount is derived from the money not smuggled in northern country atm")
           
    
        united_countries_dicts = self.northern_personal_account_aftermath
        united_countries_dicts.update(self.southern_personal_account_aftermath)
        
        name_highest_earner = ""
        losers = ""
        highest_amount = 0
        debt_money = 0
    
        
        for key_dicts,value_dicts in united_countries_dicts.items(): 
            all_values.append(value_dicts)
            sorted_all_values = sorted(all_values)
            
            if max(sorted_all_values) == value_dicts: 
               name_highest_earner = key_dicts
               highest_amount = value_dicts
            if value_dicts < 0:
                losers = key_dicts
                debt_money = value_dicts
                
                print(f"After the end of the round the players in debt are {losers} with {debt_money}")
              
        print(f" the highest earner of the round is {name_highest_earner} with an amount of {highest_amount:,}£") 
         
             


