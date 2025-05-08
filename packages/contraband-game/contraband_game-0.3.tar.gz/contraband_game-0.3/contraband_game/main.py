from .signups import SignUps
from .teams import Teams
from .gamesettings import GameSettings
from .game import Game


def main():
   
   signup_or_signin = SignUps()

   quick_start = input("Sign up = S / log in = L: ")
   
   # if chosen to sign up it is recquired to run the program again and opt for L (sign in options) now that the gamer credentials are created
   if quick_start == "S": 
      signup_or_signin.main_signup_process()
   
   elif quick_start == "L":
      signup_or_signin.main_signin_process()
      teams = Teams(signup_or_signin)
      gameset = GameSettings(teams)
      game = Game()
      game.games(signup_or_signin)
      print(game.game_aftermath())
  
      
if __name__ == "__main__":
    main()
