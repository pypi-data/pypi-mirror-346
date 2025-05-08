from .teams import Teams
from .signups import SignUps
from getpass import getpass
import random
import time



class GameSettings:
    
    
    def __init__(self,teams:Teams):
        
        self.teams = teams
        self.smuggling_amount = None
        self.inspector = None
        self.smuggler = None
        self.security_amount = None
        self.game = None
        self.inspector_win = False
        self.smuggler_win = False
        self.sec_amount_win = False
        self.doubt_investigation  = False
       
        
       
    
    def doubt_declaration(self):
        
        """All the scenarios occurring from a doubt declaration"""
        
        while True:
             
            try:
                # If it's the default player turn a random statement amount will be generated.
                if self.inspector != self.teams.player1 and self.inspector != self.teams.player2 and self.inspector != self.teams.player3 and self. inspector!= self.teams.player4:
                    self.statement_amount = float(random.randrange(1,100_000_000))
                    
                    self.security_amount = self.statement_amount / 2
                    
                    break
                else:
                    self.statement_amount = float(input("AMOUNT: "))
                    
                    # the security amount is equal to half of the statement amount. this gets temporary withdrawn from the inspector outside bank account, and given to the smuggler certain circumstances.
                    self.security_amount = self.statement_amount / 2
                    
                    # the statement amount shoudn't exceed 100milion since that is the limit of the money allowed inside the trunk.
                    if self.statement_amount >= 100_000_000:
                        break
                    else:
                        print("Invalid amount")
            except:
                print("Invalid input. Please enter a numeric value.")
                
                
        
    def doubt_declaration_aftermath(self): 
        
        """All the possible outcome from the doubt statement"""   
        
        # Some suspance on the decision.
        time.sleep(15)
        print(f"the inspector {self.inspector} declared amount is equal to {self.statement_amount:,}£ inside the trunk")    
    
        # If smuggler has no money inside the trunk and the statement amount from the inspector exceeds the empty trunk the smuggler wins and gets the security amount        
        if self.smuggling_amount == 0 and self.statement_amount > 0:
            
            # This will be used to update the money in the bank account.
            self.sec_amount_win = True
            print(f"The smuggler {self.smuggler} obtained {self.security_amount:,} £ of inspector's security amount.")
            
        # If statement amount higher or equal the smuggler amount the inspector wins  
        elif self.statement_amount >= self.smuggling_amount:
            
            # This approach is used to update the money in the bank account.
            self.inspector_win = True
            print(f"Smuggling attempt flopped!!! The inspector {self.inspector} obtained {self.smuggling_amount:,} £ into his/her outside country's bank account.")
                    
        # If the statement amount is lower than the money inside the trunk from the smuggler, The latter wins and carries both the money in the trunk and security amount of the inspector
        elif self.statement_amount < self.smuggling_amount:
            
            self.smuggler_win = True
            self.sec_amount_win = True
            print(f"{self.smuggler} succesfully smuggled {self.smuggling_amount:,} £ into his/her outside country's bank account plus {self.security_amount:,} from the inspector!!!")
        else:
            pass
    
      
    
    def pass_declaration(self):
        
        """All the scenarios occurring from a pass declaration"""

        print(f"Inspector {self.inspector} declared PASS, the smuggler carried {self.smuggling_amount:,} £")
        
        # this is the only stalemate scenario
        if self.smuggling_amount == 0:
            print(f"No money has been smuggled to the outside bank account.")
            
         # if pass is called and the smuggler has money inside the trunk the smuggler wins    
        else:
            self.smuggler_win = True
            print(f"The smuggler {self.smuggler} has been able to carry {self.smuggling_amount:,} £ into his/her outside country's bank account.")
   
           
            
    def the_inspector(self):
        
        """Inspector's action"""
        
        default_player_choice = ["PASS","DOUBT"]
            
        # The if statement gives all the delfault players in the game a option between pass and doubt.
        if self.inspector != self.teams.player1 and self.inspector != self.teams.player2 and self.inspector != self.teams.player3 and self.inspector != self.teams.player4 :
            self.inspector_action = random.choice(default_player_choice)
    
            
            # slowing down the pace of the output
            time.sleep(15)
            print("Call PASS if you believe the smuggler is carrying no money. Call DOUBT if you believe money are carried by the smuggler")
            
            # Adding a bit of suspance before the decision.
            time.sleep(5)
            print(self.inspector_action) 
        else:
            # Otherwise the the user/player inserts the key words.
            self.inspector_action = input(f"{self.inspector} Call PASS if you believe the smuggler is carrying no money. Call DOUBT if you believe money are carried by the smuggler: ")
            # SORT OUT THIS IF STATEMENT LOGIC
    
        while True:
            
            if self.inspector_action == "PASS":
                time.sleep(5)
                self.pass_declaration()
                break
                
            elif self.inspector_action == "DOUBT":
                self.doubt_investigation = True
                
                time.sleep(5)
                self.doubt_declaration()
                break
            
            else:
                self.inspector_action = input("Invalid input. Please try again:  ")
                print(self.inspector_action)

   
   
    def the_smuggler(self):
        
        """The smuggler's action"""
        
        while True: 
            try:
                # The if statement declares that every non user/player place their amount with the random function.
                if self.smuggler != self.teams.player1 and self.smuggler != self.teams.player2 and self.smuggler != self.teams.player3 and self.smuggler != self.teams.player4:
                    self.smuggling_amount = float(random.randrange(1,100_000_000))
                    
                    # delayed output to make it more fluid
                    time.sleep(10)
                    
                    # The print statement masks the smuggling amount of the default player
                    print("*************")
                    
                    print(f" {self.smuggler}'s turn is over")
                    break
                else:
                # the getpass method is needed to hide the amount placed in the trunk by the smuggler.
                    self.smuggling_amount = float(getpass(f"{self.smuggler} place your amount in the trunk. The max is 100,000,000 £: "))
                    
                    # the amount in the trunk has to be 100 million £ maximum
                    if self.smuggling_amount <= 100_000_000:
                        print(f" {self.smuggler} turn is over")
                        break  
                    else:
                        print("Invalid amount. Please try again.")
            except:
                print("Invalid input. Please enter a numeric value.")
            
                
