from unittest import TestCase
import testUtility
import random
import Dominion
import math
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

        #verify that the class variables have the expected values
        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual("coin", card.category)
        self.assertEqual(0, card.vpoints)

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
        player = Dominion.Player('Annie')

        cost = 4
        actions = 3
        cards = 0
        buys = 0
        coins = 0
        category = "action"
        buypower = 0
        vpoints = 0
        card = Dominion.Card(player.name, category, cost, buypower, vpoints)
        action_card = Dominion.Action_card(card, cost, actions, cards, buys, coins)

        balance = player.action_balance()
        self.assertEqual(0, player.action_balance())
        self.assertEqual(10, len(player.stack()))

        player.hand.append(action_card)
        player.hand.append(action_card)
        self.assertEqual(12, len(player.stack()))


        newbalance = player.action_balance()
        newbalance = round(newbalance, 2)
        self.assertAlmostEqual(23.33, newbalance)

        player.hand.append(action_card)
        self.assertEqual(13, len(player.stack()))
        newbalance = player.action_balance()
        newbalance = round(newbalance, 2)
        # 70*6/13 = ~ 32.31
        self.assertAlmostEqual(32.31, newbalance)


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