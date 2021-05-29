import unittest
from src.state.gamestate import GameState
from src.state.gamestate import Player
from src.state.gamestate import Adversary
from src.manager.ruleChecker import RuleChecker
from src.state.level import SnarlLevel
from src.state.room import Room
from src.state.hallway import Hallway
import random
import copy
from src.manager.gameManager import GameManager
from src.adversary.adversaryComponent import AdversaryComponent

class TestChecker(unittest.TestCase):
    def init_adversary(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (4, 2), (5, 2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], {"exit": (5, 2), "key":(4, 3)});
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7), (9, 7)],
                        [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], None)
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], None)
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],[hallway,
                                hallway1, hallway2, hallway3, hallway4, hallway5])
        namelist = ["dio", "ferd"]
        adversaryList = ([(4, 2)], [(15, 17)])
        playerList = [(4, 1), (5, 1)]
        manager = GameManager(namelist, level, 4, adversaryList, playerList)
        state = manager.returnGameState()
        adC1 = AdversaryComponent("z0", state,(4,2),"zombie")
        adC2 = AdversaryComponent("g0", state,(15,17),"ghost")
        return (adC1, adC2, manager)

    def testDecideMove(self):
        data = self.init_adversary()
        ad1 = data[0]
        ad2 = data[1]
        self.assertEqual(ad1.decide_move(), [(4, 1), (4, 3), (5, 2), (5, 2)])
        self.assertEqual(ad2.decide_move(), [(14, 17), (15, 16), (15, 18), (16, 17)])

    def testFindClosest(self):
        data = self.init_adversary()
        ad1 = data[0]
        ad2 = data[1]
        self.assertEqual(ad1.find_closest(), (4, 1))
        self.assertEqual(ad2.find_closest(), (5, 1))

    def testRequestMove(self):
        data = self.init_adversary()
        ad1 = data[0]
        ad2 = data[1]
        manager = data[2]
        self.assertEqual(ad1.posn, (4,2))
        ad1.request_move(manager)
        self.assertEqual(ad1.posn, (4, 1))
        self.assertEqual(ad2.posn, (15,17))
        ad2.request_move(manager)
        self.assertEqual(ad2.posn, (14, 17))

    def testRequestInteraction(self):
        data = self.init_adversary()
        ad1 = data[0]
        ad2 = data[1]
        manager = data[2]
        ad1.request_move(manager)
        self.assertEqual(ad1.request_interaction(manager), "dio")
        ad2.request_move(manager)
        self.assertEqual(ad2.request_interaction(manager), "ok")

if __name__ == '__main__':
    unittest.main()
