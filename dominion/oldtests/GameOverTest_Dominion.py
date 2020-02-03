from unittest import TestCase
import testUtility
import random
import Dominion
from collections import defaultdict


class TestGameOver(TestCase):
    # from assignment specifications
    def setUp(self):
        # Data setup
        self.players = testUtility.get_player_names()
        self.nV = testUtility.get_victory_cards(self.players)
        self.nC = testUtility.get_curse_cards(self.players)

        # Get player names
        self.player_names = testUtility.get_player_names()

        # number of curses and victory cards
        self.nV = testUtility.get_victory_cards(self.player_names)
        self.nC = testUtility.get_curse_cards(self.player_names)

        # Define box
        self.box = testUtility.get_box(self.nV)
        self.supply_order = testUtility.get_supply_order()

        # Pick 10 cards from box to be in the supply.
        self.boxList = [k for k in self.box]
        random.shuffle(self.boxList)
        self.random10 = self.boxList[:10]
        self.supply = defaultdict(list, [(k, self.box[k]) for k in self.random10])

        # The supply always has these cards
        testUtility.get_supply(self.supply, self.player_names, self.nV, self.nC)  # this is correct version

        # initialize the trash
        self.trash = []

        # Construct the Player objects
        self.player = Dominion.Player('Annie')

    def test_gameover(self):
        self.setUp()

        # check newly initialized game
        gameState = Dominion.gameover(self.supply)
        self.assertEqual(False, gameState)

        # set number of province cards in supply to 0, game should end
        self.supply["Province"] = [Dominion.Province()] * 0
        gameState = Dominion.gameover(self.supply)
        self.assertEqual(True, gameState)

        # test that game does not end as long as 5 types of cards exist in supply
        self.supply["Copper"] = [Dominion.Copper()] * 1
        self.supply["Silver"] = [Dominion.Silver()] * 1
        self.supply["Gold"] = [Dominion.Gold()] * 1
        self.supply["Estate"] = [Dominion.Estate()] * 1
        self.supply["Duchy"] = [Dominion.Duchy()] * 0
        self.supply["Province"] = [Dominion.Province()] * 1
        self.supply["Curse"] = [Dominion.Curse()] * 0
        gameState = Dominion.gameover(self.supply)
        self.assertEqual(False, gameState)

        # empty supply except for 1 province card and check that game should end
        self.supply["Copper"] = [Dominion.Copper()] * 0
        self.supply["Silver"] = [Dominion.Silver()] * 0
        self.supply["Gold"] = [Dominion.Gold()] * 0
        self.supply["Estate"] = [Dominion.Estate()] * 0
        self.supply["Duchy"] = [Dominion.Duchy()] * 0
        self.supply["Province"] = [Dominion.Province()] * 1
        self.supply["Curse"] = [Dominion.Curse()] * 0
        gameState = Dominion.gameover(self.supply)
        self.assertEqual(True, gameState)