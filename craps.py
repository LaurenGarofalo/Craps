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
        
class Table(Dice):
    def __init__(self):
        self.die = Dice() #initializes set of dice for the table
        self.point = False # start in "come out" phase
    
    #TODO: how do we change the state?
    #TODO: how do we assign/manage players?    
     
class Player(Table):  
    def __init__(self):
        self.name = input("Enter player name:\n")
        self.bankroll = self.get_valid_bankroll()
        
    def get_valid_bankroll(self):
        #valid_bankroll = False
        while True: #until we return a valid bankroll
            bankroll = input("Enter bankroll amount:\n")
            is_int = False
            is_pos = False
            try:    
                user_input = float(bankroll)
                dollar_amt = int(bankroll)
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
                
            if (is_int and is_pos):
                #valid_bankroll = True
                return bankroll
        
        
        
#%% Test Roll Dice
'''
dice = Dice()
dice.roll()
print(dice.die1_value, dice.die2_value)       
'''

#%% Test Player Initialization
player = Player() 
        

