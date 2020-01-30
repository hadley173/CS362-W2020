# -*- coding: utf-8 -*-
"""
Created on Sat 1/18/2020

@author: Clayton Hadley
"""

import random
import testUtility
from collections import defaultdict


# Get player names
player_names = testUtility.get_player_names()

# number of curses and victory cards
if len(player_names) > 2:
    nV = 12
else:
    nV = 8
nC = -10 + 10 * len(player_names)

# Define box
box = testUtility.get_box(nV)
supply_order = testUtility.get_supply_order() # correct version



# Pick 10 cards from box to be in the supply.
boxList = [k for k in box]
random.shuffle(boxList)
# random10 = boxList[:10]   # correct version
random10 = boxList[:12]    # test version
supply = defaultdict(list,[(k,box[k]) for k in random10])

# The supply always has these cards
testUtility.get_supply(supply, player_names, nV, nC)

# initialize the trash
trash = []

# Construct the Player objects
players = testUtility.initialize_players(player_names)

# Play the game
testUtility.play_game(supply, supply_order, players, trash)

# Final score
testUtility.final_score(players)
