# -*- coding: utf-8 -*-
"""
Craps
Lauren Garofalo
"""

import random

class Dice():
    def __init__(self):
        ''' sets invalid dice values to indicate a roll needs to occur'''
        self.die1_value = 0
        self.die2_value = 0
    
    def roll(self):
        ''' generates random value 1-6 to signify rolling the dice'''
        self.die1_value = random.randint(1, 6)
        self.die2_value = random.randint(1, 6)
        print(f"DICE ROLL RESULTS:{self.die1_value}  {self.die2_value}")
        return self.die1_value, self.die2_value
        
class Table(Dice):
    def __init__(self):
        super().__init__()
        self.dice = Dice() #initializes set of dice for the table
        self.point = False # start in "come out" phase
    
    #TODO: how do we change the state?
    #TODO: how do we assign/manage players?    
     
class Player(Table):  
    def __init__(self, table):
        super().__init__()
        self.table = table #assigns table for player to be at
        self.name = input("Enter player name:\n") #collect player name
        print("Please enter a bankroll amount.")
        self.bankroll = self.get_valid_dollar_amt() #get a valid $ amt
        
    def get_valid_dollar_amt(self):
        
        ''' collects from user and returns a positive, integer dollar amount '''
        
        while True: #until we return a valid dollar amount
            dollar_amt = input("Enter dollar amount:\n")
            #set criteria we need to meet
            is_int = False
            is_pos = False
            try:    
                user_input = float(dollar_amt)
                dollar_amt = int(dollar_amt)
                if user_input == dollar_amt: #user did not enter a decimal/fraction
                    is_int = True
                else:
                    print("Please enter a dollar value.\n")
                
                if dollar_amt > 0: #needs to be a positive number
                    is_pos = True 
                else:
                    print("Please enter a value greater than 0.\n")
                 
            except ValueError: #if the user did not enter a numerical value
                print("Please enter a numerical value.\n")
                
            if (is_int and is_pos): #when both criteria are met for a given input
                return dollar_amt 
            
    def get_valid_yes_no_choice(self): 
        
        ''' collects from user and returns a valid 'yes' or 'no' choice'''
        
        while True: #until we return valid choice
            user_choice = input("Enter choice:")
            
            #use .lower() so selection isn't case sensitive
            #accept "yes"/"y" and "no"/"n" as valid options
            if user_choice.lower() == "yes" or user_choice.lower() == 'y':
                return "yes"
            elif user_choice.lower() == "no" or user_choice.lower() == 'n': 
                return "no"
            else: #we did not get a valid response from the user
                print("Invalid response. Please type 'yes' or 'no'.")
        
    
          
class Bets(Player):
   def __init__(self, player):
       #super().__init__() #leads to Player being initialized twice? - omitting for now
       self.player = player #keeps track of the player that made the bets
       #initialize all bets to 0
       self.pass_line_amt = 0
       self.do_not_pass_amt = 0
       self.odds_bet_amt = 0
       
   def insufficient_funds(self):
       print(f"{self.player.name} has insufficient funds.")
       #TODO: list amounts
       #TODO: prompt player to make another bet
       
   def pass_line(self):
       
       ''' sets up a valid pass-line bet from the user '''
       
       #collect desired bet amount in dollars
       print("Please enter passline bet.\n")
       pl_bet = self.player.get_valid_dollar_amt()
       
       
       if pl_bet > self.player.bankroll: #if bet is too large
           self.insufficient_funds()
           
       else: #set the bet amount for the given player/bet
           self.pass_line_amt = pl_bet 
    
   def betting_turn(self):
       
       ''' prompts user to make a bet '''
       
       print("Would you like to make a bet?")
       choice = self.player.get_valid_yes_no_choice()
       if choice == "yes":
           self.pass_line()
       #TODO: make this available for all bet types    
           

#%% Defines method that runs the game using the classes
def play_game():
    '''plays the game using the previously defined class methods/attributes '''
    
    #initialize everything we need
    table = Table()
    player = Player(table)
    bet = Bets(player)
    
    #TODO: implement the stages #while not table.point: #while in come out phase
    #TODO: have some check for active bets
    
    bet.betting_turn() # get a bet
    if bet.pass_line_amt > 0: #we have a bet
    
        table.dice.roll() #roll the dice
        
        if (table.die1_value + table.die2_value) in [2, 3, 12]: #crapped out
            print("You Lose!")
            player.bankroll -= bet.pass_line_amt
            print(f"New bankroll: {player.bankroll}")
            
        else: #not actually the rules, just here for testing purposes right now
            print("You win!")
            player.bankroll += bet.pass_line_amt
            print(f"New bankroll: {player.bankroll}")
            
#%% run the game            
play_game()  
    
#%%        
'''Simple testing scripts held below for troubleshooting'''  
      
# Test Roll Dice
'''
dice = Dice()
dice.roll()
print(dice.die1_value, dice.die2_value)       
'''

# Test Table dice roll
'''
table = Table()
print(table.die.roll())
print(table.die.die1_value)
'''
# Test Player Initialization + Simple betting
'''
table = Table()
player = Player(table) 

bet = Bets(player)
bet.betting_turn()
'''

        

