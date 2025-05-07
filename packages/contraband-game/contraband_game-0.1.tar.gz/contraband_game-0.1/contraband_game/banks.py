
from .gamesettings import GameSettings
from .signups import SignUps
from .teams import Teams
import random

class Banks:
    
    
    def __init__(self, countries_players: SignUps , team_list: Teams, game_settings: GameSettings):
        
        self.countries_players = countries_players
        self.team_list = team_list
        self.game_settings = game_settings
        
        self.northern_country_personal_bankaccounts = None
        self.southern_country_personal_bankaccounts = None
        
        self.northern_atm_bankaccounts = None
        self.southern_atm_bankaccounts = None
        

#_______________________________________________NORTHEN SECTION THIRD COUNTRY_____________________________________________________________________________        
    
    
    
    def northern_bankaccount_third_country(self):
        
        """Returns the total amount of money obtained from the entire northen country team during the game"""
        
        if self.northern_country_personal_bankaccounts is not None:
            return self.northern_country_personal_bankaccounts
        
        else:
            # getting the northern player's list
            self.northern_bank_players = self.team_list.northern_country_players()
            
            # Placing each player's names by referencing their list position with index.
            self.northern_country_personal_bankaccounts = {self.northern_bank_players[0]:200_000_000,
                                        self.northern_bank_players[1]:200_000_000,
                                        self.northern_bank_players[2]:200_000_000,
                                        self.northern_bank_players[3]:200_000_000,
                                        self.northern_bank_players[4]:200_000_000
                                        }
            
            # Gathering all the values in the dictionary.
            self.bankaccounts_values_northern = self.northern_country_personal_bankaccounts.values()
            
            # Total amount of the Northern country.
            self.total_amount_northern_thirdcountry = sum(self.bankaccounts_values_northern) 
            
            return self.total_amount_northern_thirdcountry
            
     
    def security_amount_condition_northern(self): 
        
        """ Checking northern inspector declaration amount to prevent statements that requires a security of more than what is in his or her outside bank account."""
        
        for name_key in self.northern_country_personal_bankaccounts.keys():
             
            if self.game_settings.inspector == name_key:
                
                personal_bankaccount = self.northern_country_personal_bankaccounts[name_key]
            
            
                if self.game_settings.security_amount > personal_bankaccount:
                        
                    
                    while True:
                            
                        print("the amount cannot be backed by your security amount. Please try again")
                        
                            
                        if self.game_settings.inspector != self.team_list.player1 and self.game_settings.inspector != self.team_list.player2 and self.game_settings.inspector != self.team_list.player3 and self.game_settings.inspector != self.team_list.player4:
                            statement_amount_attemmpts = float(random.randrange(1,100_000_000))
                            
                            if statement_amount_attemmpts / 2 < personal_bankaccount:
                                self.game_settings.statement_amount = statement_amount_attemmpts
                                break
                            else:
                                self.game_settings.statement_amount = personal_bankaccount / 2
                        else:
                            statement_amount_attemmpts = float(input("here you go mate: "))
                            if statement_amount_attemmpts / 2 < personal_bankaccount:
                                self.game_settings.statement_amount = statement_amount_attemmpts
                                break
        
        
    def money_update_as_northern_smuggler(self): 
        
        """Uptdates bank account of each northern country players based on outcome of the game when role is of a smuggler.""" 
             
        for name_key in self.northern_country_personal_bankaccounts.keys():
            
            
            # Scenario where inspector calls DOUBT but smuggler's money inside the trunk exceed the amount declared from inspector.
            if self.game_settings.smuggler == name_key and self.game_settings.smuggler_win is True and self.game_settings.sec_amount_win is True: 
                
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                ammount_won = self.game_settings.smuggling_amount
                security_ammount_won = self.game_settings.security_amount
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val + ammount_won + security_ammount_won
            
            # Scenario where the smuggler has no money in the trunk and inspector calls doubt.
            elif  self.game_settings.smuggler == name_key and self.game_settings.sec_amount_win is True:
                    
                #This is the value of the dictionary. The integer.
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                #This is the security amount deriving from the game.
                ammount_won = self.game_settings.security_amount
                
                # Assigning a new value by adding the previous value with the security amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val + ammount_won
             
            #Scenario where inspector calls DOUBT and it matches or exceeds amount of money inside the smuggler's trunk. 
            elif self.game_settings.smuggler == name_key and self.game_settings.inspector_win is True: 
            
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                # This is the smuggling amount deriving from the game.
                ammount_lost = self.game_settings.smuggling_amount
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val - ammount_lost
                
            
            # Scenario where inspector calls PASS but smuggler carries money inside the trunk.   
            elif self.game_settings.smuggler == name_key and self.game_settings.smuggler_win is True:
                
                current_val = self.northern_country_personal_bankaccounts[name_key]
        
                ammount_won = self.game_settings.smuggling_amount
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val + ammount_won 
            else:
                pass  
     
          
    def money_update_as_northern_inspector(self): 
        
        
        """Uptdates bank account of each northern country players based on outcome of the game when role is of a inspector.""" 
        
                # Matching the parameter with the keys of the players bank account dictionary for then using the variable of the loop as representation of the name string.
        for name_key in self.northern_country_personal_bankaccounts.keys():
            
            
            if self.game_settings.inspector == name_key and self.game_settings.smuggler_win is True and self.game_settings.sec_amount_win is True: 
                
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                ammount_lost = self.game_settings.smuggling_amount
                security_ammount_lost = self.game_settings.security_amount
                
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val - ammount_lost - security_ammount_lost  
            
            elif  self.game_settings.inspector == name_key and self.game_settings.sec_amount_win is True:
                    
                #This is the value of the dictionary. The integer.
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                #This is the security amount deriving from the game.
                ammount_lost = self.game_settings.security_amount
                
                # Assigning a new value by adding the previous value with the security amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val - ammount_lost
                
                
            elif self.game_settings.inspector == name_key and self.game_settings.inspector_win is True: 
            
                current_val = self.northern_country_personal_bankaccounts[name_key]
                
                # This is the smuggling amount deriving from the game.
                ammount_won = self.game_settings.smuggling_amount
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val + ammount_won
                
            
            # Condition occurring in a declared PASS scenario.   
            elif self.game_settings.inspector == name_key and self.game_settings.smuggler_win is True:
                
                current_val = self.northern_country_personal_bankaccounts[name_key]
        
                ammount_lost = self.game_settings.smuggling_amount
                
                # Assigning a new value by adding the previous value with the smuggling amount.
                self.northern_country_personal_bankaccounts[name_key] = current_val - ammount_lost 
                
            else:
                pass  
        
        
#______________________________________________SOUTHERN SECTION THIRD COUNTRY__________________________________________________________________________      
 
 
 
 
    def southern_bankaccount_third_country(self):
        
        """Returns the total amount of money obtained from the entire southern country team during the game"""
        
        if self.southern_country_personal_bankaccounts is not None:
            return self.southern_country_personal_bankaccounts
        
        else:
           
            self.southern_bank_players = self.team_list.southern_country_players()
        
            self.southern_country_personal_bankaccounts = {self.southern_bank_players[0]:200_000_000,
                                        self.southern_bank_players[1]:200_000_000,
                                        self.southern_bank_players[2]:200_000_000,
                                        self.southern_bank_players[3]:200_000_000,
                                        self.southern_bank_players[4]:200_000_000
                                        }
            
            self.bankaccounts_values_southern = self.southern_country_personal_bankaccounts.values()
    
            self.total_amount_southern_thirdcountry = sum(self.bankaccounts_values_southern) 
               
            return self.total_amount_southern_thirdcountry


    def security_amount_condition_southern(self): 
        
        """ Checking inspector declaration amount to prevent statements that requires a security of more than what is in his or her outside bank account."""
  
        
        for name_key in self.southern_country_personal_bankaccounts.keys():
            
            if self.game_settings.inspector == name_key:
                
                personal_bankaccount = self.southern_country_personal_bankaccounts[name_key]
                
                if self.game_settings.security_amount > personal_bankaccount: 
                    
                    
                    while True:
                        
                        
                        print("the amount cannot be backed by your security amount. Please try again")
                            
                        if self.game_settings.inspector != self.team_list.player1 and self.game_settings.inspector != self.team_list.player2 and self.game_settings.inspector != self.team_list.player3 and self.game_settings.inspector != self.team_list.player4:
                            statement_amount_attemmpts = float(random.randrange(1,100_000_000))
                            
                            if statement_amount_attemmpts / 2 < personal_bankaccount:
                                self.game_settings.statement_amount = statement_amount_attemmpts
                                break
                            else:
                                self.game_settings.statement_amount = personal_bankaccount / 2
                        else:
                            statement_amount_attemmpts = float(input("here you go mate: "))
                            if statement_amount_attemmpts / 2 < personal_bankaccount:
                                self.game_settings.statement_amount = statement_amount_attemmpts
                                break
                                        

    def money_update_as_southern_smuggler(self): 
        
        """Uptdates bank account of each southern country players based on outcome of the game when role is of a smuggler.""" 
                
        for name_key in self.southern_country_personal_bankaccounts.keys():
            
            if self.game_settings.smuggler == name_key and self.game_settings.smuggler_win is True and self.game_settings.sec_amount_win is True: 
                
                current_val = self.southern_country_personal_bankaccounts[name_key]
                
                amount_won = self.game_settings.smuggling_amount
                
                security_ammount_won = self.game_settings.security_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val + amount_won + security_ammount_won
                
                
            elif  self.game_settings.smuggler == name_key and self.game_settings.sec_amount_win is True:
                    
                current_val = self.southern_country_personal_bankaccounts[name_key]
           
                amount_won = self.game_settings.security_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val + amount_won
                
                 
            elif self.game_settings.smuggler == name_key and self.game_settings.inspector_win is True: 
            
                current_val = self.southern_country_personal_bankaccounts[name_key]
            
                amount_lost = self.game_settings.smuggling_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val - amount_lost
                
                
             
            elif self.game_settings.smuggler == name_key and self.game_settings.smuggler_win is True:
                
                current_val = self.southern_country_personal_bankaccounts[name_key]
        
                amount_won = self.game_settings.smuggling_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val + amount_won 
            else:
                pass  
    
    
    def money_update_as_southern_inspector(self): 
    
        
        """Uptdates bank account of each southern country players based on outcome of the game when role is of a inspector.""" 
        
    
        for name_key in self.southern_country_personal_bankaccounts.keys():
            
            if self.game_settings.inspector == name_key and self.game_settings.smuggler_win is True and self.game_settings.sec_amount_win is True: 
                
                current_val = self.southern_country_personal_bankaccounts[name_key]
                
                ammount_lost = self.game_settings.smuggling_amount
                
                security_ammount_lost = self.game_settings.security_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val - ammount_lost - security_ammount_lost  
                
                
            elif  self.game_settings.inspector == name_key and self.game_settings.sec_amount_win is True:
                    
                current_val = self.southern_country_personal_bankaccounts[name_key]
            
                ammount_lost = self.game_settings.security_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val - ammount_lost
                
                
            elif self.game_settings.inspector == name_key and self.game_settings.inspector_win is True: 
            
                current_val = self.southern_country_personal_bankaccounts[name_key]
              
                ammount_won = self.game_settings.smuggling_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val + ammount_won
                
                
         
            elif self.game_settings.inspector == name_key and self.game_settings.smuggler_win is True:
                
                current_val = self.southern_country_personal_bankaccounts[name_key]
        
                ammount_lost = self.game_settings.smuggling_amount
                
                self.southern_country_personal_bankaccounts[name_key] = current_val - ammount_lost 
                
            else:
                pass  

  
                            
#________________________________________________________ATMs_______________________________________________________________________________


    
    def northern_atm(self):
        
        """It contains loaned amount of each northern players and deducts amount for each smuggler turn"""
        
        if self.northern_atm_bankaccounts is not None:
            
            if self.game_settings.smuggler == self.team_list.player2 or self.game_settings.smuggler == self.team_list.player4:
                
                for name_key in self.northern_atm_bankaccounts.keys():
                    
                    if name_key == self.game_settings.smuggler:
                        current_val = int(self.northern_atm_bankaccounts[name_key])
                        self.northern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount      
            else:
                
                for name_key in self.northern_atm_bankaccounts.keys():
                
                    if name_key == self.game_settings.smuggler:
                        
                        current_val = int(self.northern_atm_bankaccounts[name_key])
                        
                        if current_val <= 0:
                            
                            self.game_settings.smuggling_amount = 0 
                            
                        elif current_val >= 100_000_000:
                            self.southern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                        else:
                            self.game_settings.smuggling_amount = random.randrange(0,current_val)
                            self.northern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                     
        
        else:
            self.northern_ba_with_money_loaned = self.team_list.northern_country_players()
                

            self.northern_atm_bankaccounts = {self.northern_ba_with_money_loaned[0]:300_000_000,
                                            self.northern_ba_with_money_loaned[1]:300_000_000,
                                            self.northern_ba_with_money_loaned[2]:300_000_000,
                                            self.northern_ba_with_money_loaned[3]:300_000_000,
                                            self.northern_ba_with_money_loaned[4]:300_000_000
                                            }
        
                
            for name_key in self.northern_atm_bankaccounts.keys():
                
                if name_key == self.game_settings.smuggler:
                    
                    current_val = self.northern_atm_bankaccounts[name_key]
                    
                    if current_val <= 0:
                        
                        self.game_settings.smuggling_amount = 0 
                    else:
                    
                        self.northern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                
                      
                        

   
    def southern_atm(self):
        
        """It contains loaned amount of each southern players and deducts amount for each smuggler turn"""
        
        
        if self.southern_atm_bankaccounts is not None:
            
            for name_key in self.southern_atm_bankaccounts.keys():
                
                if self.game_settings.smuggler == self.team_list.player1 or self.game_settings.smuggler == self.team_list.player3:
                    for name_key in self.southern_atm_bankaccounts.keys():
                        
                        if name_key == self.game_settings.smuggler:
                            current_val = int(self.southern_atm_bankaccounts[name_key])
                            self.southern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount      
                
                if name_key == self.game_settings.smuggler:
                    
                    current_val = int(self.southern_atm_bankaccounts[name_key])
                    
                    if current_val <= 0:
                        self.game_settings.smuggling_amount = 0 
                        
                    elif current_val >= 100_000_000:
                        self.southern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                    else:
                        self.game_settings.smuggling_amount = random.randrange(0,current_val)
                        self.southern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                        
            
         
        else:
            
            self.southern_ba_with_money_loaned = self.team_list.southern_country_players()
            

            self.southern_atm_bankaccounts = {self.southern_ba_with_money_loaned[0]:300_000_000,
                                        self.southern_ba_with_money_loaned[1]:300_000_000,
                                        self.southern_ba_with_money_loaned[2]:300_000_000,
                                        self.southern_ba_with_money_loaned[3]:300_000_000,
                                        self.southern_ba_with_money_loaned[4]:300_000_000
                                        }
        
                
            for name_key in self.southern_atm_bankaccounts.keys():
                
                if name_key == self.game_settings.smuggler:
                    
                    current_val = self.southern_atm_bankaccounts[name_key]
                    
                    if current_val <= 0:
                        
                        self.game_settings.smuggling_amount = 0 
                    else:
                        self.southern_atm_bankaccounts[name_key] = current_val - self.game_settings.smuggling_amount
                        
                else:
                    pass
                



    
