from unittest import TestCase
import testUtility
import random
import Dominion
from collections import defaultdict

class TestCard(TestCase):

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

    def test_init(self):
        #initialize test data
        self.setUp()
        cost = 1
        buypower = 5

        #instantiate card object
        card = Dominion.Coin_card(self.player.name, cost, buypower)

        #verify taht thte class variables have the expected values
        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual("coin", card.category)
        self.assertEqual(0, card.vpoints)

    def test_react(self):
        pass
