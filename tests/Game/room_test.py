import unittest
from src.state.room import Room
from src.state.hallway import Hallway

class TestRoom(unittest.TestCase):
    def test_returnReachable(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
                        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4),
                        (6, 3)], None);
        self.assertEqual(room1.returnReachable((4, 1)), (3, 0))
        self.assertEqual(room1.returnReachable((3, 0)), "walls")
        self.assertEqual(room1.returnReachable((20, 1)), None)

    def test_maxXminXmaxYminY(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
                        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4),
                        (6, 3)], None);
        self.assertEqual(room1.maxXminXmaxYminY(), [6, 3, 4, 0])

    def test_placeObject(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
                        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4),
                        (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        self.assertTrue(room1.placeObject("key",(5,1)))
        self.assertTrue(room1.placeObject("exit",(4,2)))
        self.assertFalse(room1.placeObject("key",(7,7)))
        self.assertFalse(room1.placeObject("key",(3,0)))
        self.assertTrue(room1.placeObject("exit",(3,0)))

    def test_returnFreeTiles(self):
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        self.assertEqual(len(room2.returnFreeTiles()),6)
        room2.placeObject("key",(9,6))
        self.assertEqual(len(room2.returnFreeTiles()),5)


    def test_checkRoomsOverlap(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
                        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4),
                        (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        self.assertTrue(room1.checkRoomsOverlap(room1))
        self.assertFalse(room1.checkRoomsOverlap(room2))

    def test_checkHallwayRoomOverlap(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        hallway = hallway.generteHallway()
        hallway = hallway[1:len(hallway)]
        self.assertFalse(room1.checkHallwayRoomOverlap(hallway))
        room2 = Room((8, 3), 4, 4, [(8, 3)],[(8, 3)],None)
        self.assertTrue(room2.checkHallwayRoomOverlap(hallway))

    def test_returnTraversablePoint(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        self.assertEqual(room1.returnTraversablePoint((6, 1)), [[1, 5], [2, 6]])
        self.assertEqual(room1.returnTraversablePoint((10, 10)), None)
        self.assertEqual(room1.returnTraversablePoint((3, 0)), [])

    def test_returnNonWallTiles(self):
        room1 = Room((3, 0), 4, 5, [(6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        self.assertEqual(room1.returnNoneWallTiles(), [(6, 3), (4, 4)])

    def test_returnRoomPosn(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2),
        (5, 2),(6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        self.assertEqual(room1.returnRoomPosn(), (3, 0))

    def testInvalidRooms(self):
        with self.assertRaises(Exception) as context:
            room1 = Room((3, 0), 2, 1, [(3, 0)], [(3, 0)], None)
        self.assertTrue('Size is invalid please enter again' in str(context.exception))
        with self.assertRaises(Exception) as context:
            room2 = Room((3, 0), 4, 4, [(10, 10)], [(3, 0)], None)
        self.assertTrue('Invalid nonewalltiles' in str(context.exception))
        with self.assertRaises(Exception) as context:
            room3 = Room((3, 0), 4, 4, [(3, 0)], [(3, 0)], {"key":(10, 10)})
        self.assertTrue('Invalid Objects' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
