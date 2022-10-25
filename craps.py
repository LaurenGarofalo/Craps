# -*- coding: utf-8 -*-
"""
Craps
Lauren Garofalo
"""

import random

class Dice():
    def __init__(self):
        self.die1_value = 0
        self.die2_value = 0
    
    def roll(self):
        self.die1_value = random.randint(1, 6)
        self.die2_value = random.randint(1, 6)
        
#%% Roll Dice
dice = Dice()
dice.roll()
print(dice.die1_value, dice.die2_value)        
        

