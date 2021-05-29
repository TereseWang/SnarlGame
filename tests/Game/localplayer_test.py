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
from src.player.LocalPlayer import Player

class TestChecker(unittest.TestCase):
    def init_player(self):
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
        player1 = Player("dio", 4, (4, 1))
        player2 = Player("ferd", 4, (5, 1))
        return (player1, player2, manager)

    def testMove(self):
        data = self.init_player()
        player1 = data[0]
        player2 = data[1]
        manager = data[2]
        player1.move([4, 2])
        self.assertEqual(player1.posn, [4, 2])
        player2.move([4, 3])
        self.assertEqual(player2.posn, [4, 3])

    def testRequestMove(self):
        data = self.init_player()
        player1 = data[0]
        player2 = data[1]
        manager = data[2]
        self.assertEqual(player1.request_move(manager, (4, 2)), manager)
        self.assertEqual(player2.request_move(manager, None), "please re-enter movement")

    def testRequestInteraction(self):
        data = self.init_player()
        player1 = data[0]
        player2 = data[1]
        manager = data[2]
        self.assertEqual(player1.request_interaction(manager, (4, 2)), 'Eject')
        self.assertEqual(player2.request_interaction(manager, (4, 3)), "Key")


if __name__ == '__main__':
    unittest.main()
