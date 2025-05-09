# Contraband-Game

This is one of the games from the manga "Liar Game". The instructions of the game are in the repository (game_rules.txt). 
Have fun.

![ image alt](https://github.com/andrewisoko/contraband_game/blob/main/images/image%2001.jpg)


# Instructions

* Run the game with "python -m contraband_game.main" (both IDE terminal and Command prompt)
*  Terminate the game by pressing Ctrl + C
* Clear terminal by pressing cls (command prompt) otherwise if running on IDE terminal Ctrl + L

1) The sign up process creates username and code, mandatory for participating the game.

2) Although there is no limit for the amount of accounts that can be created, only 4 accounts can partecipate.

3) User credentials , generated username and code are stored in json files. *Highly advised to remember the generated credentials for the log in*. 

4) The game (round according to the manga conventions) has no graphic interface. it requires simple inputs.

# Tests 

1) The tests are not found in the packages, if wanting to try the tests it is advised to download the entire repository.
2) "pip install setuptools" 
3) It is recquired to activate the vritual environment to run the tests.
4) Simply insert "pytest" on the terminal.


# Potential issues


*  To avoid the unlimited waiting time during the tests, it is suggested to comment all the time.sleep in the gamesettings.py module.

*  In case an issue arises with the test functionality, it is suggested to activate the virtual environment inside the tests directory for then returning back to the previous directory (cd..) to ensure the proper usage of pytest. 


# Installation instructions


1) Downloading python is required to play the game in your command prompt here is the link for the tutorial https://wiki.python.org/moin/BeginnersGuide/Download

2) Run "pip install setuptools" in your command prompt for configuring the required modules.

3) Run "pip install contraband_game" to install the package.

4) Run  "python -m contraband_game.main" to start the game.






