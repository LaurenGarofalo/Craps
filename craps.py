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
                    print("Please enter a dollar value, cents cannot be used.\n")
                
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
       print("To make a bet, you must enter an amount lower than your remaining bankroll.")
       print(f"Current bankroll: {self.player.bankroll}")
       bet = self.player.get_valid_dollar_amt()
       return bet
       
   
   def get_max_odds_bet(self, roll_number_betted):
       
       if roll_number_betted in [4, 10]:
           return 3 * self.pass_line_amt
       
       if roll_number_betted in [5, 9]:
           return 4 * self.pass_line_amt
       
       if roll_number_betted in [6, 8]:
           return 5 * self.pass_line_amt
       
       return 0 
        
        
   def pass_line(self, pl_bet):
       
       ''' sets up a valid pass-line bet from the user '''
       
       #collect desired bet amount in dollars
       #print("Please enter pass line bet.")
       #pl_bet = self.player.get_valid_dollar_amt()
       
       
       #if pl_bet > self.player.bankroll: #if bet is too large
       #    self.insufficient_funds()
           
       #else: #set the bet amount for the given player/bet
       self.pass_line_amt = pl_bet 
       self.player.bankroll -= pl_bet
           
   def do_not_pass(self, dnpl_bet):
       
       ''' sets up a valid do not pass-line bet from the user '''
       
       #collect desired bet amount in dollar
       #print("Please enter a do not pass line bet.")
       #dnpl_bet = self.player.get_valid_dollar_amt()
       
       #if dnpl_bet > self.player.bankroll: #if bet is too large
       #    self.insufficient_funds()
           
       #else:  #set the bet amount for the given player/bet
       self.do_not_pass_amt = dnpl_bet
       self.player.bankroll -= dnpl_bet
           
   
   def ingest_bet(self):
       ''' gets a valid bet amount '''
       
       bet = self.player.get_valid_dollar_amt()  
       while bet > self.player.bankroll:
           bet = self.insufficient_funds()
       return bet    
           
    
   def betting_turn(self):
       
       ''' prompts user to make a pass/do not pass bet '''
       
       print("Would you like to make a bet?")
       choice = self.player.get_valid_yes_no_choice()
       if choice == "yes":
           #TODO: here, get bet type, ingest get valid bet number
           print("What type of bet would you like to make?")
           print("Options: 'pass line' , 'do not pass line'")
           bet_choice = input().lower()
           if bet_choice == "pass line" or bet_choice == "do not pass line":
               bet = self.ingest_bet()
               if bet_choice == "pass line":
                   self.pass_line(bet)
               else:
                   self.do_not_pass(bet)
           else: 
               print("Error: Invalid bet name.")
               self.betting_turn()
   
   def shooter(self):
       #if we have a bet, roll the die
       if self.pass_line_amt != 0 or self.do_not_pass_amt != 0:
           self.player.roll()
           roll_sum = self.player.die1_value + self.player.die2_value
           
           
           if not self.player.point: #in come-out phase
           
               if roll_sum in [2, 3, 12]:
                   if self.pass_line_amt > 0: #crapped out
                       self.bet_loser()
                   if self.do_not_pass_amt > 0 and roll_sum != 12:  
                       self.bet_winner()
                       
               elif roll_sum  in [7, 11]: # pass wins, no pass loses
                   if self.pass_line_amt > 0:
                       self.bet_winner()
                   if self.do_not_pass_amt >0:
                       self.bet_loser()
                   
               else:
                   self.point = roll_sum    #the number that needs to be rolled again to win 
                   #TODO: need to reset this somewhere once round is over    
               
   def bet_loser(self):
       pass 

   def bet_winner(self):
       pass

   def print_bet_made(self):
       ''' prints the bets made and remaining bankroll '''
       
       if self.pass_line_amt > 0:
           print(f"Pass line bet made: {self.pass_line_amt}")
           
       if self.do_not_pass_amt > 0:
           print(f"Do not pass line bet made: {self.do_not_pass_amt}")
           
       if self.odds_bet_amt > 0:
           print(f"Odds bet made: {self.odds_bet_amt}")
           
       print(f"Remaining balance: {self.bankroll}")    
                           
   def print_bet_won(self):
       pass
   
   def print_bet_lost(self):
       pass
   
   
   def get_valid_odds_roll_bet(self):
       while True:
         num_bet_on = input("What number would you like to place an odds bet on?\n Options: 4, 5, 6, 8, 9, 10")
         try:
             if float(num_bet_on) in [4, 5, 6, 8, 9, 10]:
                 return int(num_bet_on)
         except ValueError:
             print("Please enter a numerical value.")
         
       
   def odds(self):
       if self.pass_line_amt > 0:
           num_bet_on = self.get_valid_odds_roll_bet()
           max_bet = min([self.get_max_odds_bet(num_bet_on), self.player.bankroll])
           print(f"The maximum bet that can be made is {max_bet}")
           print(f"Your current bankroll is {self.player.bankroll}")
           odds_bet = self.ingest_bet()
           self.odds_bet_amt = odds_bet
           self.player.bankroll -= odds_bet
       else:
           print("An odds bet cannot be made right now.")
           self.odds_bet_amt = 0
      
           

#%% Defines method that runs the game using the classes

'''
def play_game():
    
    #initialize everything we need
    table = Table()
    player = Player(table)
    bet = Bets(player)
    
    #TODO: implement the stages #while not table.point: #while in come out phase
    #TODO: have some check for active bets
    
    bet.betting_turn() # get a bet
'''
'''
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
'''        
            
#%% run the game            
#play_game()  
    
#%%        
'''Simple testing scripts held below for troubleshooting'''  
#Test shooter
table = Table()
player = Player(table)
bet = Bets(player)
bet.betting_turn()
bet.shooter()
      
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

        

