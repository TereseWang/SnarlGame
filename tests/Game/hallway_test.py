import unittest
from src.state.room import Room
from src.state.hallway import Hallway

class TestHallway(unittest.TestCase):
    def test_checkReachable(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        self.assertEqual(hallway.returnReachable((6, 3)), [(6, 3), (8, 5)])
        self.assertEqual(hallway.returnReachable((10, 10)), None)

    def test_checkTraversable(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        self.assertTrue(hallway.checkTraversable((6, 3)))
        self.assertFalse(hallway.checkTraversable((10, 10)))

    def test_checkHallwayOverlapRoom(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
        (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        self.assertFalse(hallway.checkHallwayOverlapRoom(room1))
        room2 = Room((8, 3), 4, 4, [(8, 3)],[(8, 3)],None)
        self.assertTrue(hallway.checkHallwayOverlapRoom(room2))

    def test_checkHallwaysContainHallway(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(13, 6)], (10, 6), (13, 11))
        self.assertTrue(hallway1.checkHallwaysContainHallway([hallway1,hallway]))
        self.assertTrue(hallway1.checkHallwaysContainHallway([hallway,hallway1]))
        self.assertTrue(hallway2.checkHallwaysContainHallway([hallway,hallway1]))
        self.assertFalse(hallway1.checkHallwaysContainHallway([hallway,hallway]))

    def test_checkHallwayOverlapHallway(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        self.assertTrue(hallway.checkHallwayOverlapHallway(hallway))
        self.assertFalse(hallway1.checkHallwayOverlapHallway(hallway))

    def test_maxXminYmaxYminY(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        self.assertEqual(hallway.maxXminXmaxYminY(), [8, 6, 5, 3])

    def test_InvalidHallway(self):
        with self.assertRaises(Exception) as context:
            hallway = Hallway([(10, 10)], (1, 1), (2, 1))
        self.assertTrue('Waypoints cannot connect to the start end point'
                                in str(context.exception))
    def test_generateHallway(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        self.assertEqual(hallway.generteHallway(), [(6, 3), (7, 3), (8, 3),
                            (8, 4), (8, 5)])
        self.assertEqual(hallway1.generteHallway(), [(10, 6),(11, 6),(12, 6),
                            (13, 6),(13, 7),(13, 8),(13, 9),(13, 10),(13, 11)])

if __name__ == '__main__':
    unittest.main()
