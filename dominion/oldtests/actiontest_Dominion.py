from unittest import TestCase
import testUtility
import random
import Dominion
#import mock
#import module


from collections import defaultdict


class TestAction(TestCase):
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

        # Construct the Player object
        self.player = Dominion.Player('Annie')

    def test_init(self):
        self.setUp()
        # setup for generic card
        cost = 4
        category = "action"
        buypower = 2
        vpoints = 2
        # create
        card = Dominion.Card(self.player.name, category, cost, buypower, vpoints)

        # Setup for generic Action Card
        actions = 7
        cards = 3
        buys = 6
        coins = 4
        action_card = Dominion.Action_card(card, cost, actions, cards, buys, coins)

        # check values of card and action card objects
        self.assertEqual(cost, card.cost)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(vpoints, card.vpoints)
        self.assertEqual(cost, action_card.cost)
        self.assertEqual(actions, action_card.actions)
        self.assertEqual(cards, action_card.cards)
        self.assertEqual(buys, action_card.buys)
        self.assertEqual(coins, action_card.coins)
        self.assertEqual(0, action_card.buypower)
        self.assertEqual(0, action_card.vpoints)



    def test_use(self):
        self.setUp()
        smithy = Dominion.Smithy()
        feast = Dominion.Feast()

        # add cards to player's hand
        self.player.hand.append(smithy)
        self.player.hand.append(feast)

        # use the smithy card
        Dominion.Action_card.use(smithy, self.player, self.trash)

        # check that smithy card is in the played pile and not in the hand
        self.assertEqual([smithy], self.player.played)
        self.assertNotEqual([smithy], self.player.hand)

        self.player.played = []
        # play the feast card
        Dominion.Action_card.use(feast, self.player, self.trash)
        # check that feast card is in the played pile and not in the hand
        self.assertEqual([feast], self.player.played)
        self.assertNotEqual([feast], self.player.hand)

    def test_augment(self):
        self.player = Dominion.Player('Annie')
        self.player.hand = []
        # Check the fields affected by augment function are zero when initialized as such
        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 0
        self.player.cards = 0
        self.assertEqual(0, self.player.actions)
        self.assertEqual(0, self.player.buys)
        self.assertEqual(0, self.player.purse)
        self.assertEqual(0, self.player.cards)

        # Set values for the fields affected by augment and check they are correct
        self.player.actions = 2
        self.player.buys = 2
        self.player.purse = 2
        self.player.cards = 2

        self.assertEqual(2, self.player.actions)
        self.assertEqual(2, self.player.buys)
        self.assertEqual(2, self.player.purse)
        self.assertEqual(2, self.player.cards)


        village = Dominion.Village()
        throne = Dominion.Throne_Room

        # calling augment on village card should add 2 actions to the player
        village.augment(self.player)

        # two actions added to player from the village cards
        self.assertEqual(4, self.player.actions)
        self.assertEqual(2, self.player.buys)
        self.assertEqual(2, self.player.purse)
        self.assertEqual(2, self.player.cards)
        # Player only draws once, despite player.cards value being set to 3
        self.assertEqual(1, len(self.player.hand))

