
import string
import random
import json


class SignUps:
  
  """initial sign up credentials"""

  def __init__ (self):
    
    self.json_value_validation = True
    self.name = None
    self.surname = None
    self.email_address = None
    self.nickname = None
    self.code = None
    
    

    
  def json_append_data(self,filename,*args):
      
      """Append gamer credentials' dictionary in the json file"""
      
      with open (filename,"r") as file:
        # Json list object
         self.data_to_append = json.load(file) 
      
      # This is uselful to append any other object beside self.user dict in a json file.   
      if self.name is None and self.surname is None: 
        for arg in args:
            self.data_to_append.append(arg) 
      else:
       # The dictionary comes from the dict credential function 
       self.data_to_append.append(self.user_dict) 
         
      with open (filename,"w") as file:
        # Writing the new data in the json file once it has been appended with the variable instance of the json list
        return json.dump(self.data_to_append,file, indent=4)
    
    
    
  def json_read_data(self,filename) ->list:
    
      """Reads list from json files"""
      
      #reads a json file
      with open (filename,"r") as file:
         # returns a list object
         return json.load(file) 
       
      
      
       
  def json_account_check_process(self):
    
    """Checks if value is in the json dictionary"""
  
    read_data_for_signin = self.json_read_data("data/user_data.json")  
    read_data_for_players = self.json_read_data("data/players.json")
       

    self.json_user_data_list = [values for dictionaries in read_data_for_signin for values in dictionaries.values()] 
 
    self.players_json_list = [value_players for dictionaries_players in read_data_for_players for value_players in dictionaries_players.values()] 
    
    # Check if nickname has been already in the player.json file in order to avoid multiple sign in with the same gamer credentials.
    if self.nickname_signin in self.players_json_list:
      print("player already generated")
      
    else:
      
      if self.nickname_signin in self.json_user_data_list and self.code_signin in self.json_user_data_list:
    
          index1 = self.json_user_data_list.index(self.nickname_signin) 
          index2 = self.json_user_data_list.index(self.code_signin)
          
          # This will avoid accessing the game with credentials deriving from two different account but still present in the json list
          if index1 + 1 == index2: 
          # Stopping the while self.json_value_validation in sign in if condition are met.
            self.json_value_validation = False
            print("Credentials present on database")
            
          else:
            print("Incorrect credentials")
      
       
    
  def sign_up(self) -> str:
    
      """User initial information."""
      
      print("Welcome to the contraband game please sign up")  
      
      self.name = input("Name:  ")
      self.surname = input("Surame:  ")
      
      while True:
        
        # Email in a while loop in case it doesn't match requirements
        self.email_address = input("email: ")
        
         # Checking requirements needed for an email 
        if "@" in self.email_address and "." in self.email_address:
          print("Succesful sign up")
          break
        
        else:
          print("Not matching email standards. Please add a @ and a . into your email.")  
          
           
    
  def dict_credentials(self) -> str: 
        
      """Data where each user generated credentials are stored"""
      
      
      self.user_dict = {"nickname": self.nickname,
                  "code": self.code,
                  "email": self.email_address,
                  }
    
      print("Data inserted on database")
     

    
  def game_generated_credentials(self) -> str:
    
        """Generating nickname and code for each user."""  
        
        game_list_data_instance = self.json_read_data("data/user_data.json")
        
        # Instead of checking name and surname that might be homonym, this checks if email is already in the json list suggesting a creation of a previous account.
        if self.email_address != None and self.email_address in game_list_data_instance:
          
            # preventing creation of multiple accounts
            print("Account already exists")
    
        else:
            # Nickname contains the first three character of a name and the rest is made by the entire surname.
            self.nickname = self.name[0:3] + self.surname  

            # this contains all the upper case letters
            letters_uppercase = string.ascii_uppercase
            
            # this tuple contains lower case, punctuations and numbers.
            my_tuppy = (string.ascii_lowercase,string.punctuation,string.digits)
            
            # mergin the upper case letters with the rest of the tuple
            code_chars = letters_uppercase.join(my_tuppy)
            
            # accessing each character in the list
            list_char = [char for char in code_chars]
            
            # shuffling the list
            random.shuffle(list_char)
            
            empty = ""
             # merging the empty string with the tuple (of the list) to have an array of random characters
            code_string = empty.join(tuple(list_char))
            
            # the code is made by the first 18 random characters.
            self.code = code_string[0:18]
            
        
            print(f"Please save and use the generated user credentials to login. NICKNAME:{self.nickname} USER CODE:{self.code}")
     
     
        
  def sign_in(self) -> str:
      
      
        """Login for user after obtained the game credentials"""
        
        
        # the instance variable comes from json_check_account_process
        while self.json_value_validation:
          
          print("Insert 'skip' on both nickname and code if convenient to skip.") 
          self.nickname_signin = input("Nickname: ")
          self.code_signin = input("code: ")
          
          
          try:
            
            # Checking if gamer credentials are in the json_user_data file, avoiding access with nickname and code from two different game credentials in the json file etc...
            self.json_account_check_process()
            
            # this is an additional layer (probably redundant)
            if self.nickname_signin in self.nickname and self.code_signin in self.code:
              
            
              print(f"{self.nickname_signin} and {self.code_signin} accepted")
              print("ACCOUNT CREATED")   
              
              break
            
          except:
            pass
            
          if self.nickname_signin == "skip" and self.code_signin == 'skip':
            break
      
          else:
            pass
                
          
         
    
  def main_signup_process(self):
        
        """Sign up function that summarises all the sign up process"""
        
        
        # sign up first gamer.
        self.sign_up() 
        
        # creating the gamer credentials needed to access the game.
        self.game_generated_credentials()  
        
        # creating the dictionary which will be passed as an argument in the json_append_data function.
        self.dict_credentials()
        # Adding dict_credentials in the json_user_data file.
        self.json_append_data("data/user_data.json")
        
        while True:
          
          # sign up second player.
          self.additional_player = input("to join a second gamer press S otherwise press N: ")  
        
          if self.additional_player == "S":
            
            self.sign_up()
            self.game_generated_credentials() 
            
            self.dict_credentials()
            self.json_append_data("data/user_data.json")
            break
            
          elif self.additional_player == "N":
              print("Only 1 player logged in")
              break
          
          else:
              self.additional_player = input("please try again: ")
        

 
  def main_signin_process(self):
    
    """Sign up function that summarises all the sign up process"""
    
    # Used to multiple log in requests. Maximum 4 players.
    count_players  = 3 
    
    self.sign_in()
    
    # Unlike the sign up this will grab the user nickname data for then store it in a json file
    self.json_append_data("data/players.json",{"Nickname": self.nickname_signin})
    
    while count_players > 0:
      
      try:
        
        second_sign_in = int(input("Insert 2 to sign up another player else Insert 0: "))
        
        if second_sign_in == 0:
          break
          
        elif second_sign_in == 2:
          
          # Needed to be added since after the first call of the functions the boolian variable turns in returnd false.
          self.json_value_validation = True
          # Print statement occurring.
          self.sign_in()
          # Unlike the sign up process in this case the function will not append a dixtionary therefore the argument is needed.
          self.json_append_data("data/players.json",{"Nickname": self.nickname_signin})
          count_players -= 1
      
      except:
          print("I Know it sounds frustrating, please restart the log in process.")
        
      
      




    
      
      




    
