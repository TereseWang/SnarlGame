import unittest
from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel
from src.state.gamestate import Player, Adversary, GameState

class TestState(unittest.TestCase):


    def test_returnJsonPlayers(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.returnJsonPlayers(),
        [ {"type": "player", "name": "p1", "position": [1, 4]},
        {"type": "player", "name": "p2", "position": [2, 4]}])

        state = GameState(level,
        {(4,1):player1},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})

        self.assertEqual(state.returnJsonPlayers(),
        [ {"type": "player", "name": "p1", "position": [1, 4]}])


    def test_returnJsonAdversaries(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.returnJsonAdversaries(),
        [{"type": "zombie","name": "a1","position": [1,5]},
        {"type": "zombie","name": "a2","position": [12,5]},
        {"type": "zombie","name": "a3","position": [17,14]}])

        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1})

        self.assertEqual(state.returnJsonAdversaries(),
        [{"type": "zombie","name": "a1","position": [1,5]}])


    def test_updateUnlock(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getUnlock(),False)
        state.updateUnlock(True)
        self.assertEqual(state.getUnlock(),True)
        state.updateUnlock(False)
        self.assertEqual(state.getUnlock(),False)

    def test_checkInsideMap(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertFalse(state.checkInsideMap((5,50)))
        self.assertTrue(state.checkInsideMap((5,5)))


    def test_getPlayerLen(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getPlayerLen(),2)

    def test_getPlayer(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getPlayer("p2"),player2)
        self.assertEqual(state.getPlayer("pooo"),None)

    def test_getAdversary(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getAdversary("a2"),adversary2)
        self.assertEqual(state.getAdversary("pooo"),None)

    def test_getPlayerPosns(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getPlayerPosns(),[(4, 1), (4, 2)])


    def test_removePlayer(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})

        self.assertEqual(state.returnJsonPlayers(),
        [ {"type": "player", "name": "p1", "position": [1, 4]},
        {"type": "player", "name": "p2", "position": [2, 4]}])

        state.removePlayer((4, 1))
        self.assertEqual(state.returnJsonPlayers(),
        [{"type": "player", "name": "p2", "position": [2, 4]}])

        state.removePlayer((4, 2))
        self.assertEqual(state.returnJsonPlayers(),
        [])

    def test_movePlayer(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.returnJsonPlayers(),
        [ {"type": "player", "name": "p1", "position": [1, 4]},
        {"type": "player", "name": "p2", "position": [2, 4]}])

        state.movePlayer((4,3),"p1")
        self.assertEqual(state.returnJsonPlayers(),
        [ {"type": "player", "name": "p2", "position": [2, 4]},
        {"type": "player", "name": "p1", "position": [3, 4]}])

        state.movePlayer((5,3),"p2")
        self.assertEqual(state.returnJsonPlayers(),
        [{"type": "player", "name": "p1", "position": [3, 4]},
        {"type": "player", "name": "p2", "position": [3, 5]}])

    def test_object(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.returnObject((4,1)),"1")
        self.assertEqual(state.returnObject((4,0)),"x")
        self.assertEqual(state.returnObject((4,4)),"2")
        self.assertEqual(state.returnObject((10,16)),"k")
        self.assertEqual(state.returnObject((13,12)),"e")


        self.assertTrue(state.placeObject("key", (4,1)))
        self.assertEqual(state.returnObject((4,1)),"k")

        self.assertTrue(state.placeObject("exit", (4,4)))
        self.assertEqual(state.returnObject((4,4)),"e")

        self.assertFalse(state.placeObject("key",(0,0)))
        self.assertFalse(state.placeObject("exit",(0,0)))
        self.assertFalse(state.placeObject("key",(4,0)))
        self.assertTrue(state.placeObject("exit",(4,0)))


    def test_getPlayerBasedOnPosn(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getPlayerBasedOnPosn((4,1)).playerName(),"p1")
        self.assertEqual(state.getPlayerBasedOnPosn((4,2)).playerName(),"p2")
        self.assertEqual(state.getPlayerBasedOnPosn((4,4)), None)

    def test_getAdversaryBasedOnPosn(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.getAdversaryBasedOnPosn((5,1)).adversaryName(),"a1")
        self.assertEqual(state.getAdversaryBasedOnPosn((5,12)).adversaryName(),"a2")
        self.assertEqual(state.getAdversaryBasedOnPosn((14,17)).adversaryName(),"a3")
        self.assertEqual(state.getAdversaryBasedOnPosn((4,4)),None)

    def test_checkValidPositions(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertTrue(state.checkValidPositions())

        state = GameState(level,
        {(4,1):player1, (4,0): Player("p",(4,0))},{})
        self.assertFalse(state.checkValidPositions())

        state = GameState(level,
        {(4,1):player1, (16,3): Player("p",(16,3))},{})
        self.assertFalse(state.checkValidPositions())

        state = GameState(level,
        {(4,1):player1, (4,5): Player("p",(4,5))},{})
        self.assertTrue(state.checkValidPositions())

        state = GameState(level,
        {(4,1):player1, (3,5): Player("p",(3,5))},{})
        self.assertFalse(state.checkValidPositions())

    def test_checkValidPosition(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertTrue(state.checkValidPosition((4,4)))
        self.assertTrue(state.checkValidPosition((5,12)))
        self.assertFalse(state.checkValidPosition((2,2)))
        self.assertFalse(state.checkValidPosition((1,1)))
        self.assertFalse(state.checkValidPosition((2,2)))
        self.assertFalse(state.checkValidPosition((17,1)))

    def test_checkNoneRepeatOccupy(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertTrue(state.checkNoneRepeatOccupy())

        state = GameState(level,
        {(4,1):Player("p1",(4,1)), (4,2): player1},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertFalse(state.checkNoneRepeatOccupy())


    def test_moveAdversary(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        state.moveAdversary((5,2),"a1")
        self.assertEqual(adversary1.adversaryPosns(),(5,2))
        state.moveAdversary((4,2),"a1")
        self.assertEqual(adversary1.adversaryPosns(),(4,2))


    def test_returnPlayerTiles(self):
        state = GameState(level,
        {(4,1):player1, (4,2): player2},
        {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})
        self.assertEqual(state.returnPlayerTiles("p1",(4,1))[1],[{'position': [0, 4], 'type': 'exit'},
        {'position': [1, 4], 'type': 'key'}])
        self.assertEqual(state.returnPlayerTiles("p1",(4,1))[0],
        [[0, 0, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 1, 1, 0],[0, 0, 1, 1, 0],
        [0, 0, 1, 1, 2]])
        self.assertEqual(state.returnPlayerTiles("p1",(4,1))[2],
        [{'name': 'a1', 'position': [1, 5], 'type': 'zombie'},
        {'name': 'p2', 'position': [2, 4], 'type': 'player'}])








if __name__ == '__main__':
    room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (4, 2), (5, 2),
                    (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
    room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7), (9, 7)],
                    [(8, 5), (10, 6)], None)
    room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                    (12, 12)], {"exit": (13, 12)})
    room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                    (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                    (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
    room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                    [(8, 16), (11, 16)], {"key" : (10, 16)})
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
    player1 = Player("p1",(4,1))
    player2 = Player("p2",(4,2))
    adversary1 = Adversary((5,1),"a1","zombie")
    adversary2 = Adversary((5,12),"a2","zombie")
    adversary3 = Adversary((14,17),"a3","zombie")
    state = GameState(level,
    {(4,1):player1, (4,2): player2},
    {(5,1):adversary1, (5,12):adversary2,(14,17):adversary3})

    unittest.main()
