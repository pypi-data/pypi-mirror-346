import json
import random
from .signups import *



class Teams:
  
  
  
  def __init__(self,sign_in: SignUps):
      
      self.sign_in = sign_in
      self.player1 = None
      self.player2 = None
      self.player3 = None
      self.player4 = None
      
      
   
   
    
  def player_generator(self):
    
      """Dinamically assign players values"""

      with open("data/players.json", "r") as file:
          # Read Json file.
          self.player_json_list = json.load(file) 
          
      # A list of values from the players.json's dictionaries.
      self.player_list_values = [player_nickname for dictionaries in self.player_json_list for player_nickname in dictionaries.values()] # Appending json values on a list
      
      # Remove "player0" if it exists.
      if self.player_list_values[0] == "player0": 
          self.player_list_values.pop(0) 
      
      # Creating an index paired with a value for the first 4 items in the list.
      for index_list_value, value in enumerate(self.player_list_values[:4]): 
          
           # Assigning values to initialised instance attribute matched with index of list item.
          setattr(self, f"player{index_list_value + 1}", value)
      
      return "Player/s in the game :)"



  
  def southern_country_players(self) -> list:
    
    """It returns a list containing the southern country's players"""
       
    
    team1_list = [ "Lupin", "Clyde","Charles Ponzi"]
    
    # It is mandatory to have at least a player in the game, player1. the additional players will be replaced by other invented players if they do not partake in the game.
    if self.player1 is None:
      team1_list.append("Jordan Belfort")
    else:
        team1_list.append(self.player1)
        
    # With the if statement containing else statement I have inverted the block structure pay attention.
    if self.player3 is None:
        team1_list.append("Bonnie")
    else:
        team1_list.append(self.player3)
    
  
    return team1_list



  
  def northern_country_players(self) -> list:
     
    """It returns a list containing the northern country's players"""
       
     
    team2_list = ["Maradona","Berlusconi", "Diddy"]

    if self.player2 is None:
        team2_list.append("S.Bankman-Fried")
    else:
        team2_list.append(self.player2)
        
        
    if self.player4 is None:
        team2_list.append("Ted Bundy")
    else:
        team2_list.append(self.player4)
        

    return team2_list
  
  
