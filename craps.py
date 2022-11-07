# -*- coding: utf-8 -*-
"""
Craps
Lauren Garofalo
"""

import random
import time

class Dice():
    def __init__(self):
        
        #set invalid dice values to indicate a roll needs to occur
        self.die1_value = 0
        self.die2_value = 0
        
        #holds print graphics so pictoral representations of dice can be printed for each roll 
        self.graphics = {1: "+-----+\n|     |\n|  o  |\n|     |\n+-----+",
                         2: "+-----+\n| o   |\n|     |\n|   o |\n+-----+",
                         3: "+-----+\n| o   |\n|  o  |\n|   o |\n+-----+",
                         4: "+-----+\n| o o |\n|     |\n| o o |\n+-----+",
                         5: "+-----+\n| o o |\n|  o  |\n| o o |\n+-----+",
                         6: "+-----+\n| o o |\n| o o |\n| o o |\n+-----+"}
    
    def roll(self):
        
        ''' generates and displays random value 1-6 to signify rolling the dice'''
        
        #gets random role values for each die
        self.die1_value = random.randint(1, 6)
        self.die2_value = random.randint(1, 6)
        
        #for gaming graphic display purposes
        print("Rolling dice...") 
        time.sleep(0.5) #pause to signify dice roll
        
        #display dice using the defined graphics dictionary
        print(f"{self.graphics[self.die1_value]}\n{self.graphics[self.die2_value]}")
        time.sleep(0.5) #pause to allow user to look at dice before roll results display
        
        
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
        self.name = input("Enter player name:\n") #collect player name... any name will do (no validation needed)
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
        
            #use .lower() so selection is case insensitive
            user_choice = input("Enter choice:").lower()
            
            
            #accept "yes"/"y" and "no"/"n" as valid options
            if user_choice in ["yes",  'y']:
                return "yes"
            
            elif user_choice in [ "no" ,'n']: 
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
       print(f"Current bankroll: ${self.player.bankroll}")
       
       bet = self.player.get_valid_dollar_amt() #will be checked against bankroll again later
       #ingest_bet() prompts user to make another bet using this menthod
       return bet
       
   
   def get_max_odds_bet(self):
       
       ''' returns the maximum bet that can be made based on the pass line wager
       rules: 3x pass line for 4, 10; 4x pass line for 5, 9; 5x pass line for 6,8'''
       
       if self.pass_line_amt > 0: #if we have pass line bet
           if self.player.point in [4, 10]:
               return (3 * self.pass_line_amt - self.odds_bet_amt) #minus the current odds bet
           
           if self.player.point in [5, 9]:
               return (4 * self.pass_line_amt - self.odds_bet_amt)
           
           if self.player.point in [6, 8]:
               return (5 * self.pass_line_amt - self.odds_bet_amt)
       
       return 0 #an odds bet cannot be made
        
        
   def pass_line(self):
       
       ''' sets up a valid pass-line bet from the user '''
       
       # >0 bankroll/point phase are checked in betting_turn
       #therefore, a bet can commence
       
       bet = self.ingest_bet() #get bet amount
       
       #update bet amount and bankroll
       self.pass_line_amt += bet
       self.player.bankroll -= bet
       
       #alert user to the bet that was made
       self.print_bet_made()
           
   def do_not_pass(self, dnpl_bet):
       
       ''' sets up a valid do not pass-line bet from the user '''
       
       # >0 bankroll/point phase are checked in betting_turn
       #therefore, a bet can commence
       
       bet = self.ingest_bet() #get bet amount
       
       #update bet amount and bankroll
       self.do_not_pass_amt += bet
       self.player.bankroll -= bet
       
       #alert user to the bet that was made
       self.print_bet_made()
           
   
   def ingest_bet(self):
       
       ''' gets a valid bet amount '''
       
       #made sure we get a positive whole dollar amount
       bet = self.player.get_valid_dollar_amt()  
       
       #don't accept bets greater than the bankroll
       while bet > self.player.bankroll:
           bet = self.insufficient_funds() #prompt user to make another bet
         
       return bet    
           
    
   def betting_turn(self):
      
       ''' prompts user to make a bet then roll the dice depending on the game state'''
       
       while self.player.bankroll > 0: #while we have money to bet
           
           if not self.player.point: # in come out phase = pass/no pass bet
               
               #ask user if they'd like to bet
               print("Would you like to make a bet?")
               choice = self.player.get_valid_yes_no_choice()
               
               if choice == "yes":
                   
                   print("What type of bet would you like to make?")
                   print("Options: 'pass line' , 'do not pass line'")
                   bet_choice = input().lower() #case insensitive
                   
                   if bet_choice == "pass line" or bet_choice == "do not pass line":
                       
                       if bet_choice == "pass line":
                           self.pass_line() #make a pass line bet
                           
                       else:
                           self.do_not_pass() #make a do not pass line bet
                           
                       self.shooter() #after bet is made it's time to roll   
                       
                   else: #calls method again so player can make a valid bet
                       print("Error: Invalid bet name.")
                       self.betting_turn()
                       break #fixes error where user was prompted for another bet after ending game
                       
               else: #if user does not want to make a bet, it's time to payout
                   self.payout()
                   break #ensures nothing happens after payout
                   
           else: #we are in point phase - roll die

             self.odds() #give option to make an odds bet
             self.shooter() #roll the die
           
          
   
   def shooter(self):
       
       ''' rolls the dice and evaluates payouts if there are active bets '''
       
       #if we have a bet, roll the die
       if self.pass_line_amt != 0 or self.do_not_pass_amt != 0:
           
           #allows the user to roll the die themselves
           print("Time to roll! Hit enter to roll the dice!")
           _ = input() #prompt user to hit a key to progress with rolling the dice
           self.player.roll()
           
           #collect the sum results from the roll
           roll_sum = self.player.die1_value + self.player.die2_value
           
           
               
           if not self.player.point: #in come-out phase
                   
           
               if roll_sum in [2, 3, 12]:
                   
                   if self.pass_line_amt > 0: #crapped out on the pass bet
                       self.bet_loser("pass")
                       
                   if self.do_not_pass_amt > 0 and roll_sum != 12:  #won no pass bet
                       self.bet_winner("no pass")
                       
                   elif self.do_not_pass_amt > 0 and roll_sum == 12: #pushes - tie resets bet
                       
                       #reset values
                       self.player.bankroll += self.do_not_pass_amt
                       self.do_not_pass_amt = 0
                       
                       #print result for player
                       print("Bet pushes.")
                       print(f"Current bankroll: ${self.player.bankroll}")
                       
               
               elif roll_sum  in [7, 11]:
                
                   #pass wins
                   if self.pass_line_amt > 0:
                       self.bet_winner("pass")
                   
                   #no pass loses    
                   if self.do_not_pass_amt >0:
                       self.bet_loser("no pass")
               
               else: #leaving come-out phase
               
                   #display the on number for the player
                   print(f"ON: {roll_sum}")
                   self.player.point = roll_sum #set point value
                   
                   #if player has pass line bet, they can make an odds bet
                   if self.pass_line_amt > 0:
                       self.odds()
                       
                   else: #if not, the do not pass bet must be reconciled
                   
                       print("An odds bet cannot be made on a do not pass bet.")
                       
                       #roll die while the do not pass bet is in play
                       while self.do_not_pass_amt > 0: 
                           self.shooter()
                       
                  
           else:  #in point phase
           
               if roll_sum == 7: 
                   
                   #pass loses
                   if self.pass_line_amt > 0:
                       self.bet_loser("pass")
                       
                       #if there's an odds bet, that loses as well
                       if self.odds_bet_amt > 0:
                           self.bet_loser("odds")
                   
                   #no pass wins        
                   elif self.do_not_pass_amt > 0:
                       self.bet_winner("no pass")
                       
                   self.player.point = False #end point phase    
                       
               elif roll_sum == self.player.point: #rolled the "on" value
                   
                   #pass wins
                   if self.pass_line_amt > 0:
                       self.bet_winner("pass")
                       
                       #if there's an odds bet, that wins as well
                       if self.odds_bet_amt > 0:
                           self.bet_winner("odds")
                   
                   #do not pass loses        
                   elif self.do_not_pass_amt > 0:
                       self.bet_loser("no pass")
                       
                   self.player.point = False #end point phase   
                       
                   
   def bet_loser(self, bet_type):
       
       ''' prints and saves the losing bet type and amount lost '''
       
       #print that a bet was lost
       print(f"You lost a {bet_type} bet.")
       
       #save the money lost for a pass bet, reset bet
       if bet_type == "pass":
           money_lost = self.pass_line_amt
           self.pass_line_amt = 0
           #no need to subtract because bet was removed from bankroll when bet was made and odds are 1:1
           
       #save money lost for a no pass bet, reset bet   
       elif bet_type == "no pass":
           money_lost = self.do_not_pass_amt
           self.do_not_pass_amt = 0
       
       #save money lost for an odds bet, reset bet   
       else:
           money_lost = self.odds_bet_amt
           self.odds_bet_amt = 0
           
       #print the amount of money lost in the bet    
       self.print_bet_lost(money_lost)    
           

   def bet_winner(self, bet_type):
       
       ''' prints and saves the winning bet type and amount won '''
       
       #print that a bet was won
       print(f"You won a {bet_type} bet!")
       
       #save money won for a pass bet, reset bet
       if bet_type == "pass":
           money_won = self.pass_line_amt
           self.pass_line_amt = 0
           self.player.bankroll += (2 * money_won) #get bet back + winnings (1:1)
       
       #save money won for a no pass bet, reset bet  
       elif bet_type == "no pass":
           money_won = self.do_not_pass_amt
           self.do_not_pass_amt = 0
           self.player.bankroll += (2 * money_won) 
       
       #save money won for an odds bet (depends on point value)    
       else:
           if self.player.point in [6, 8]:
               money_won = self.odds_bet_amt * 1.2 #6 to 5
           elif self.player.point in [5, 9]:
               money_won = self.odds_bet_amt * 1.5 #3 to 2
           elif self.player.point in [4, 10]:
               money_won = self.odds_bet_amt * 2 #2 to 1
               
           
           #correct bankroll, reset bet 
           self.player.bankroll += (self.odds_bet_amt + money_won)
           self.odds_bet_amt = 0

       #print money won    
       self.print_bet_won(money_won) 
       

   def print_bet_made(self):
       
       ''' prints the bets made and remaining bankroll '''
       
       #print pass line bet if it exists
       if self.pass_line_amt > 0:
           print(f"Pass line bet made: {self.pass_line_amt}")
       
       #print do not pass bet if it exists    
       if self.do_not_pass_amt > 0:
           print(f"Do not pass line bet made: {self.do_not_pass_amt}")
       
       #print odds bet if it exists    
       if self.odds_bet_amt > 0:
           print(f"Odds bet made: {self.odds_bet_amt}")
        
       #print the player's current bankroll    
       print(f"Remaining balance: {self.player.bankroll}")    
                           
   def print_bet_won(self, money_won):
       
       ''' prints the money won, calculated in bet_winner(), and new bankroll) '''
       
       print(f"You won ${money_won}!")
       print(f"Current bankroll: ${self.player.bankroll}")
      
   
   def print_bet_lost(self, money_lost):
       
       ''' prints the money lost, calculated in bet_loser(), and new bankroll) '''
       
       print(f"You lost ${money_lost}.")
       print(f"Current bankroll: ${self.player.bankroll}")
       
       #if bankroll = 0, the game will not continue. therefore, tell user that the game is over
       if self.player.bankroll == 0:
           print(f"Game over! You lost ${self.player.original_bankroll}")
       
                 
   def odds(self):
       
       ''' check for valid odds bet amount and allows user to make an odds bet '''
       
       if self.pass_line_amt > 0: #need a pass line bet
           
           #the max odds bet will either be determined by the pass bet/point value or the bankroll
           max_bet = min([self.get_max_odds_bet(), self.player.bankroll]) #whichever is smaller
           
           if max_bet > 0: #we have a bet that could be made
               print(f"The maximum bet that can be made is {max_bet}")
               print(f"Your current bankroll is ${self.player.bankroll}")
               print("Would you like to make an odds bet?")
               
               choice = self.player.get_valid_yes_no_choice()
               
               if choice == "yes": #user wants to make an odds bet
                   
                   #get desired bet amount
                   odds_bet = self.ingest_bet()
                   
                   #make sure the odds bet isn't more than the maximum allowed
                   while odds_bet > self.get_max_odds_bet():
                       print(f"Your bet is too high. Max bet is: {self.get_max_odds_bet()}")
                       odds_bet = self.ingest_bet()
                   
                   #save bet value and update bankroll    
                   self.odds_bet_amt += odds_bet
                   self.player.bankroll -= odds_bet
                   self.print_bet_made()
               
           else: #an odds bet cannot be made, roll the die to reconcile current bets
           
               while self.pass_line_amt > 0:
                   print("You cannot make an odds bet right now.")
                   self.shooter() #still need to roll the die even if we can't bet
       
       else: #alert user that they can't make an odds bet - lacking a pass bet
           print("You cannot make an odds bet right now.")
           self.odds_bet_amt = 0 
           
   def payout(self):
       
       ''' reconciles bets, prompts user to end game or make a new bet '''
       
       #if all bets are 0, there is nothing to reconcile
       if self.pass_line_amt == 0 and self.do_not_pass_amt == 0 and self.odds_bet_amt == 0:
           
           #ask player if they want to keep playing
           print("Keep playing?")
           choice = self.player.get_valid_yes_no_choice()
           
           #if player wants to keep playing, prompt them to make a new bet
           if choice == "yes":
               self.betting_turn()
               
           else: #if not - game over, display results
               print("You have decided to end the game. Thanks for playing!\nPayout results:")
               
               #calculate the difference in player's bankroll at beginning/end of game
               earnings = self.player.bankroll - self.player.original_bankroll
               
               if earnings > 0: #if they have more money now, they won money
                   print(f"Congrats! You won ${earnings}!")
                   
               elif earnings < 0: #if not, they lost money
                   print(f"Too bad! You lost ${-earnings}.")
                   
               else: #if the amounts are the same, they broke even
                   print("You broke even!")
                   
       else: #if there are active bets, reconcile them prior to payout
           print("Active bets must be reconciled before cashout.")
           while self.pass_line_amt != 0 or self.do_not_pass_amt != 0:   
               self.shooter() #roll the die
           

#%% Interface to start game
def validate_choice(user_choice):  
    
    ''' gets a yes/no choice from user input to determine if user would like to play craps'''
    
    while True: #until a valid response is returned
        
        #case insensitive, allows for "yes"/"y" as viable options
        if user_choice.lower() in ["yes", "y"]:
            return "yes"
        
        #case insensitive, allows for "no"/"n" as viable options
        elif user_choice.lower() in ["no", "n"]:
            return "no"
        
        #prompt user to enter a valid response
        print("Invalid response. Please type 'yes' or 'no'.")
        user_choice = input("Would you like to play Craps?")
        
#gets a valid choice from the user to start the craps game
user_choice = validate_choice(input("Would you like to play Craps?"))
    
if user_choice == "yes": #user wants to play

    #set up the table, player, and begin betting to get the game going
    table = Table()
    player = Player(table)
    bet = Bets(player)
    bet.betting_turn()

else: #user doesn't want to play, exit the program
    print("You have decided not to play. Goodbye.")    
    

        

