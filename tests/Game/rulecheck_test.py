import unittest
from src.state.room import Room
from src.state.level import SnarlLevel
from src.state.hallway import Hallway
from src.state.gamestate import Player
from src.state.gamestate import Adversary
from src.state.gamestate import GameState
from src.manager.ruleChecker import RuleChecker
from src.manager.gameManager import GameManager

class TestChecker(unittest.TestCase):
    def init_manager(self):
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
        return manager

    def testReturnInteraction(self):
        manager = self.init_manager()
        state = manager.returnGameState()
        rule = RuleChecker(state)

        self.assertEqual(rule.returnInteraction((4, 2)), "ejected")
        self.assertEqual(rule.returnInteraction((3, 2)), "valid")
        self.assertEqual(rule.returnInteraction((4, 3)), "unlock")
        self.assertEqual(rule.returnInteraction((5, 2)), "locked")

    def testReturnAdInteraction(self):
        manager = self.init_manager()
        state = manager.returnGameState()
        rule = RuleChecker(state)
        self.assertEqual(rule.returnAdInteraction((4, 1)).playerName(), "dio")
        self.assertEqual(rule.returnAdInteraction((3, 2)), "moved")

    def testCheckValidPlayerMovement(self):
        manager = self.init_manager()
        state = manager.returnGameState()
        rule = RuleChecker(state)
        self.assertFalse(rule.checkValidPlayerMovement((1, 1), "aa"))
        self.assertFalse(rule.checkValidPlayerMovement((1, 1), "dio"))
        self.assertFalse(rule.checkValidPlayerMovement((4, 4), "dio"))
        self.assertFalse(rule.checkValidPlayerMovement((5, 1), "dio"))
        self.assertTrue(rule.checkValidPlayerMovement((4, 2), "dio"))

    def testCheckValidAdversaryMovement(self):
        manager = self.init_manager()
        state = manager.returnGameState()
        rule = RuleChecker(state)
        try:
            self.assertFalse(rule.checkValidAdversaryMovement((1, 1), "aaa"))
        except Exception as e:
            self.assertEqual(str(e), "Cannot find with the given adversary")
        self.assertFalse(rule.checkValidAdversaryMovement((1, 1), "g0"))
        self.assertFalse(rule.checkValidAdversaryMovement((15, 19), "g0"))
        self.assertFalse(rule.checkValidAdversaryMovement((4, 4), "z0"))
        self.assertTrue(rule.checkValidAdversaryMovement((15, 18), "g0"))
        self.assertTrue(rule.checkValidAdversaryMovement((4, 3), "z0"))


if __name__ == '__main__':
    unittest.main()
