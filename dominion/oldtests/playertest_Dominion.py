from unittest import TestCase
import testUtility
import random
import Dominion
from collections import defaultdict


class TestPlayer(TestCase):
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


    def test_draw(self,dest=None):
        self.setUp()
        # From PyCharm code coverage guide
        self.assertNotEqual('NotACard', self.player.draw().name)

        # Set the deck Length to 0 and call draw again
        # The deck gets set to the discard so check that the size is equal
        discardSize = len(self.player.discard)
        self.player.deck = []
        self.player.draw()
        self.assertEqual(discardSize, len(self.player.deck))
        # player hand should be size 6, since draw function was called
        self.assertEqual(6, len(self.player.hand))
        self.assertEqual(0, len(self.player.discard))
        self.assertEqual(0, len(self.player.aside))
        self.assertEqual(0, len(self.player.hold))


    def test_action_balance(self):
        self.setUp()
        """
        cost = 4
        actions = 3
        cards = 0
        buys = 0
        coins = 0
        category = "action"
        buypower = 0
        vpoints = 0
        card = Dominion.Card(self.player.name, category, cost, buypower, vpoints)
        action_card = Dominion.Action_card(card, cost, actions, cards, buys, coins)
        """
        trash = []
        player = Dominion.Player('Annie')
        spy = Dominion.Woodcutter()
        self.assertEqual(0, player.action_balance())
        player.hand.append(spy)
        player.hand.append(spy)
        player.hand.append(spy)


        #Dominion.Action_card.use(spy, player, trash)

        #self.player.action_balance()
        #self.action_balance()
        #self.assertEqual(1, player.action_balance())


        """
        cellar = Dominion.Cellar
        cellar.Category = "action"
        self.player.hand.append(cellar)
        self.player.action_balance()
        self.assertEqual(3, self.player.actions)
        """


    def test_cardsummary(self):
        self.setUp()

        summary = self.player.cardsummary()
        self.assertEqual({'Copper': 7, 'Estate': 3, 'VICTORY POINTS': 3}, summary)


        duchy = Dominion.Duchy()
        self.player.deck.append(Dominion.Province())
        self.player.hand.append(duchy)
        self.player.discard.append(duchy)

        summary = self.player.cardsummary()
        self.assertEqual({'Copper': 7, 'Duchy': 2, 'Estate': 3, 'Province': 1, 'VICTORY POINTS': 15}, summary)

    def test_calcpoints(self):
        self.setUp()

        self.assertEqual(3, self.player.calcpoints())
        self.player.deck.append(Dominion.Province())
        self.player.hand.append(Dominion.Duchy())
        self.player.discard.append(Dominion.Duchy())

        self.assertEqual(15, self.player.calcpoints())

        self.player.hand.append(Dominion.Gardens())
        self.player.hand.append(Dominion.Gardens())
        self.assertEqual(17, self.player.calcpoints())


