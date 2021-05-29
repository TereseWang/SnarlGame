import unittest
from src.state.room import Room
from src.state.level import SnarlLevel
from src.state.hallway import Hallway
from src.state.gamestate import Player
from src.state.gamestate import Adversary
from src.state.gamestate import GameState
from src.manager.gameManager import GameManager
from src.adversary.adversaryComponent import AdversaryComponent

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

    def testRenderAround(self):
        manager = self.init_manager()
        self.assertEqual(manager.renderAround((4, 1)), [[(2, 18), (3, 18), (4, 18), (5, 18),(6, 18)],
                                                        [(2, 0), 'x', 'x', 'x', 'x'],
                                                        [(2, 1), 'x', 'dio', 'ferd', 'x'],
                                                        [(2, 2), 'x', 'z', 'e', 'x'],
                                                        [(2, 3), 'x', 'k', '1', '2']])
    def testHandleAdversary(self):
        manager = self.init_manager()
        gamestate = manager.returnGameState()
        component1 = AdversaryComponent("z0", gamestate, (4, 2), "zombie")
        component2 = AdversaryComponent("g0", gamestate, (15, 17), "ghost")
        adList = [component1, component2]
        adList1 = manager.handleAdversary()
        for i in range(0, len(adList1)):
            self.assertEqual(adList[i].name, adList1[i].name)
            self.assertEqual(adList[i].posn, adList1[i].posn)
            self.assertEqual(adList[i].type, adList1[i].type)

    def testMovePlayer(self):
        manager = self.init_manager()
        self.assertEqual(manager.move_player("dio", (4, 2)), manager)
        self.assertEqual(manager.move_player("dio", None), manager)
        self.assertEqual(manager.move_player("alice", (4, 1)), "please re-enter movement")
        self.assertEqual(manager.move_player("dio", (3, 1)), "please re-enter movement")

    def testMoveAdversary(self):
        manager = self.init_manager()
        self.assertEqual(manager.move_adversary("g0", (1, 1)), "please re-enter movement")
        try:
            self.assertEqual(manager.move_adversary("a0", (1, 1)), "please re-enter movement")
        except Exception as e:
            self.assertEqual(str(e), 'Cannot find with the given adversary')
        self.assertEqual(manager.move_adversary("g0", (15, 16)), manager)
        self.assertEqual(manager.move_adversary("g0", None), manager)

    def testRespondInteraction(self):
        manager = self.init_manager()
        self.assertEqual(manager.respond_to_interaction("dio", (4, 2)), "Eject")
        self.assertEqual(manager.respond_to_interaction("dio", (3, 2)), "OK")
        self.assertEqual(manager.respond_to_interaction("dio", (4, 3)), "Key")
        manager.move_player("dio", (4, 3))
        self.assertEqual(manager.respond_to_interaction("dio", (5, 2)), "Exit")
        manager = self.init_manager()
        self.assertEqual(manager.respond_to_interaction("dio", (5, 2)), "exit locked")

    def testAdversaryInteraction(self):
        manager = self.init_manager()
        self.assertEqual(manager.adversary_interaction((4, 1)), "dio")
        self.assertEqual(manager.adversary_interaction((4, 2)), "ok")

if __name__ == '__main__':
    unittest.main()
