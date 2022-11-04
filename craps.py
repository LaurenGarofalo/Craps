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
        
        ''' generates and displays random value 1-6 to signify rolling the dice'''
        
        self.die1_value = random.randint(1, 6)
        self.die2_value = random.randint(1, 6)
        
        print(f"DICE ROLL RESULTS:{self.die1_value}  {self.die2_value}")
        
        #TODO: check if return statement is needed here
        #return self.die1_value, self.die2_value
        
class Table(Dice):
    
    def __init__(self):
        
        ''' sets up table with a pair of dice and the come out phase '''
        
        super().__init__()
        self.dice = Dice() #initializes set of dice for the table
        self.point = False # start in "come out" phase
  
     
class Player(Table):  
    
    def __init__(self, table):
        ''' sets up player at a table and gets name/valid bankroll from user''' 
        super().__init__()
        self.table = table #assigns table for player to be at
        self.name = input("Enter player name:\n") #collect player name
        print("Please enter a bankroll amount.")
        self.bankroll = self.get_valid_dollar_amt() #get a valid $ amt
        self.original_bankroll = self.bankroll #to compare overall earnings after the game is over
        
    def get_valid_dollar_amt(self):
        
        ''' collects from user and returns a positive, integer dollar amount '''
        
        while True: #until we return a valid dollar amount
            dollar_amt = input("Enter dollar amount:\n")
            
            #set criteria we need to meet
            is_int = False
            is_pos = False
            
            try:    
                #check that a whole number was entered
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
            
            #use .lower() so selection is case insensitive
            #accept "yes"/"y" and "no"/"n" as valid options
            if user_choice.lower() == "yes" or user_choice.lower() == 'y':
                return "yes"
            elif user_choice.lower() == "no" or user_choice.lower() == 'n': 
                return "no"
            else: #we did not get a valid response from the user
                print("Invalid response. Please type 'yes' or 'no'.")
        
    
          
class Bets(Player):
   def __init__(self, player):
       
       self.player = player #keeps track of the player that made the bets
       
       #initialize all bets to 0
       self.pass_line_amt = 0
       self.do_not_pass_amt = 0
       self.odds_bet_amt = 0
       
   def insufficient_funds(self):
       
       ''' Explains that the bet made is too large and asks user for another
           bet after displaying the current bankroll'''
       
       print(f"{self.player.name} has insufficient funds.")
       print("To make a bet, you must enter an amount lower than your remaining bankroll.")
       print(f"Current bankroll: {self.player.bankroll}")
       
       bet = self.player.get_valid_dollar_amt() #will be checked against bankroll again later
       return bet
       
   
   def get_max_odds_bet(self):
       
       ''' returns the maximum bet that can be made based on the pass line wager
       rules: 3x pass line for 4, 10; 4x pass line for 5, 9; 5x pass line for 6,8'''
       
       if self.pass_line_amt > 0: #if we have pass line bet
           if self.player.point in [4, 10]:
               return 3 * self.pass_line_amt
           
           if self.player.point in [5, 9]:
               return 4 * self.pass_line_amt
           
           if self.player.point in [6, 8]:
               return 5 * self.pass_line_amt
       
       return 0 #an odds bet cannot be made
        
        
   def pass_line(self, pl_bet):
       
       ''' sets up a valid pass-line bet from the user '''
       
       #collect desired bet amount in dollars
       #print("Please enter pass line bet.")
       #pl_bet = self.player.get_valid_dollar_amt()
       
       
       #if pl_bet > self.player.bankroll: #if bet is too large
       #    self.insufficient_funds()
           
       #else: #set the bet amount for the given player/bet
       self.pass_line_amt += pl_bet 
       self.player.bankroll -= pl_bet
           
   def do_not_pass(self, dnpl_bet):
       
       ''' sets up a valid do not pass-line bet from the user '''
       
       #collect desired bet amount in dollar
       #print("Please enter a do not pass line bet.")
       #dnpl_bet = self.player.get_valid_dollar_amt()
       
       #if dnpl_bet > self.player.bankroll: #if bet is too large
       #    self.insufficient_funds()
           
       #else:  #set the bet amount for the given player/bet
       self.do_not_pass_amt += dnpl_bet
       self.player.bankroll -= dnpl_bet
           
   
   def ingest_bet(self):
       ''' gets a valid bet amount '''
       
       bet = self.player.get_valid_dollar_amt()  
       while bet > self.player.bankroll:
           bet = self.insufficient_funds()
       return bet    
           
    
   def betting_turn(self):
       print("IN BETTING TURN")
       ''' prompts user to make a pass/do not pass bet '''
       while self.player.bankroll > 0:
           if not self.player.point:
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
                       self.shooter()    
                   else: 
                       print("Error: Invalid bet name.")
                       self.betting_turn()
               else:
                   self.payout()
                   break
           else: #we are in point phase - roll die
             #TODO hash out point phase of game in shooter
             #ask for bets until we reach max
             #7 = lose
             #point = win
             self.shooter()
           
          
   
   def shooter(self):
       print("IN SHOOTER")
       #if we have a bet, roll the die
       if self.pass_line_amt != 0 or self.do_not_pass_amt != 0:
           self.player.roll()
           roll_sum = self.player.die1_value + self.player.die2_value
           
           if roll_sum in [4, 5, 6, 8, 9, 10]:
               print(f"ON: {roll_sum}")
               self.player.point = roll_sum
               self.odds()
               
           if not self.player.point: #in come-out phase
           
               if roll_sum in [2, 3, 12]:
                   if self.pass_line_amt > 0: #crapped out
                       self.bet_loser("pass")
                   if self.do_not_pass_amt > 0 and roll_sum != 12:  
                       self.bet_winner("no pass")
                       
               elif roll_sum  in [7, 11]: # pass wins, no pass loses
                   if self.pass_line_amt > 0:
                       self.bet_winner("pass")
                   if self.do_not_pass_amt >0:
                       self.bet_loser("no pass")
                     
                          
               
   def bet_loser(self, bet_type):
       print(f"You lost a {bet_type} bet.")
       if bet_type == "pass":
           money_lost = self.pass_line_amt
           self.pass_line_amt = 0
           #no need to subtract because bet was removed from bankroll when bet was made and odds are 1:1
       elif bet_type == "no pass":
           money_lost = self.do_not_pass_amt
           self.do_not_pass_amt = 0
       else:
           pass 
           #TODO: put odds bet lost with wager
       self.print_bet_lost(money_lost)    
           

   def bet_winner(self, bet_type):
       print(f"You won a {bet_type} bet!")
       if bet_type == "pass":
           money_won = self.pass_line_amt
           self.pass_line_amt = 0
           self.player.bankroll += (2 * money_won) #get bet back + winnings (1:1)
           
       elif bet_type == "no pass":
           money_won = self.do_not_pass_amt
           self.do_not_pass_amt = 0
           self.player.bankroll += (2 * money_won) 
           
       else:
           pass 
           #TODO: put odds bet won with wager
           
       self.print_bet_won(money_won) 
       

   def print_bet_made(self):
       ''' prints the bets made and remaining bankroll '''
       
       if self.pass_line_amt > 0:
           print(f"Pass line bet made: {self.pass_line_amt}")
           
       if self.do_not_pass_amt > 0:
           print(f"Do not pass line bet made: {self.do_not_pass_amt}")
           
       if self.odds_bet_amt > 0:
           print(f"Odds bet made: {self.odds_bet_amt}")
           
       print(f"Remaining balance: {self.bankroll}")    
                           
   def print_bet_won(self, money_won):
       print(f"You won ${money_won}!")
       print(f"Current bankroll: {self.player.bankroll}")
      
   
   def print_bet_lost(self, money_lost):
       print(f"You lost ${money_lost}.")
       print(f"Current bankroll: {self.player.bankroll}")
       
   
                
   def odds(self):
       if self.pass_line_amt > 0:
           max_bet = min([self.get_max_odds_bet(), self.player.bankroll])
           print(f"The maximum bet that can be made is {max_bet}")
           print(f"Your current bankroll is {self.player.bankroll}")
           print("Would you like to make an odds bet?")
           choice = self.player.get_valid_yes_no_choice()
           if choice == "yes":
               odds_bet = self.ingest_bet()
               self.odds_bet_amt += odds_bet
               self.player.bankroll -= odds_bet
       else:
           print("An odds bet cannot be made right now.")
           self.odds_bet_amt = 0 
           
   def payout(self):
       if self.pass_line_amt == 0 and self.do_not_pass_amt == 0 and self.odds_bet_amt == 0:
           print("Keep playing?")
           choice = self.player.get_valid_yes_no_choice()
           if choice == "yes":
               self.betting_turn()
           else:
               earnings = self.player.bankroll - self.player.original_bankroll
               if earnings > 0:
                   print(f"Congrats! You won ${earnings}!")
               elif earnings < 0: 
                   print(f"Too bad! You lost ${-earnings}.")
               else:
                   print("You broke even!")
       else: 
           print("Active bets must be reconciled before cashout.")
           self.shooter()
           

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
#bet.shooter()
      
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

        

