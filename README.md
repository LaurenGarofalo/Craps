# Text-Based Craps Game
This repository is for the development of a text-based simplified craps game. The game is simplified in that it only allows for 1 player at a time and the only bets that can be made are pass, do not pass, and odds bets. 

### Quick Start Guide
To play the game, simply download and run the script craps.py. Upon running, you will be asked if you'd like to play craps. Type "yes" or "y" and press enter. Then, the game of craps will begin. 

### Class Functionality
The following describes the functionality of each of the individual classes used in this game. 
#### Dice
- Initialization sets attributes `die1_value` and `die2_value` to 0 to indicate that they haven't been rolled yet and a roll needs to occur after the game begins. An additional attribute included is `graphics` which is a dictionary where they key is a number 1-6 (indicating possible roll values) and the value is a pictoral representation of that roll. This was included so that the dice roll could be displayed pictorally. 

- The `roll` method uses the random package to generate a random number for each of the die to signify a roll of the dice. There is also a pause using the time package to signify the rolling of the dice. After the numbers are generated, the dice are printed to the console using the `graphics` dictionary. 

#### Table
- Inherits Dice

- Initialization inherits all the attributes/methods of Dice as well as initializing a pair of `dice` as an attribute. It also includes a state `point = False` to signify that a craps game that has just started would start in the "come out" phase and no point is set. 

#### Player
- Inherits Table

- Initialization takes in the parameter `table` to assign a player to a table. The attribute `name` is set through input from the user. Any name/number/symbol combination is acceptable as it isn't used for more than printing purposes. The player is also prompted to set their `bankroll` amount which is set using the `get_valid_dollar_amt` method (described below). The final attribute set at initialization is the `original_bankroll` which holds the starting bankroll of the player to compare to at the end of the game.

- `get_valid_dollar_amt` runs a loop that only ends when the user has entered a positive whole number value to signify that only dollars can be accepted for this game. Specific error messages will be displayed if the user enters a string, a negative number, or a decimal value instructing the user on how to correct their input. This method returns a positive integer dollar amount. 

- `get_valid_yes_no_choice` similarly runs a loop until a valid yes/no choice is input by the player. Valid "yes" choices include (case-insensitive) "yes" and "y". Similarly, valid case-insensitive "no" choices include "no" and "n". This method returns string "yes" or string "no" depending on the user's selection.

#### Bets
- Inherits Player

- Initialization takes in the parameter `player` to set the player that is making the bets. Other attributes include `pass_line_amt`, `do_not_pass_amt` and `odds_bet_amt` which are all initalized to 0. These represent the current pass line, do not pass line, and odds bet amounts. 

- `insufficient_funds` is called when the player attempts to make a bet larger than their current bankroll. An error message is displayed and a new valid bet is collected using `player.get_valid_dollar_amt`. A positive integer bet is returned.

- `get_max_odds_bet` returns the maximum odds bet than can be made depending solely on the point value during the point phase. For point values 4 and 10 the max bet is 3x the pass line bet, for 5 and 9 it's 4x and for 6 and 8 it's 5x. If no point value is set or the pass line bet is 0, this method would return 0 to signify an odds bet cannot be made.

- `pass_line` collects a valid bet from the user using the `ingest_bet` method (described below). Upon received a valid bet, the `pass_line_amt` and `player.bankroll` attributes are edited to reflect the changes caused by the bet. Finally the bet made is displayed to the user by calling the `print_bet_made` method (described below).

- `do_not_pass` similar to `pass_line` collects a valid bet and updates `do_not_pass_amt` and `player.bankroll`, then prints the bet made.

- `ingest_bet` uses `player.get_valid_dollar_amt` to get a desired bet amount from the user. Then, if/while the bet is larger than the player's bankroll (invalid), calls `insufficient_funds` to tell the user that an error has occured and prompts them to make another bet. Finally, the method returns a positive integer bet lesser than or equal to the player's bankroll.

- 
