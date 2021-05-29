import unittest
from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel

class TestLevel(unittest.TestCase):
    def test_checkTraversable(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertTrue(level.checkTraversable((4, 1)))
        self.assertFalse(level.checkTraversable((4, 100)))
        self.assertFalse(level.checkTraversable((3, 0)))

    def test_returnType(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])

        self.assertEqual(level.returnType((4, 1)), "room")
        self.assertEqual(level.returnType((4, 100)), "void")
        self.assertEqual(level.returnType((3, 0)), "room")
        self.assertEqual(level.returnType((6, 3)), "room")
        self.assertEqual(level.returnType((7, 3)), "hallway")

    def test_returnReachable(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.returnReachable((4, 1), "room"), [(7, 5), (2, 10)])
        self.assertEqual(level.returnReachable((4, 100), "void"), [])
        self.assertEqual(level.returnReachable((3, 0), "room"), [(7, 5), (2, 10)])
        self.assertEqual(level.returnReachable((6, 3), "room"), [(7, 5), (2, 10)])
        self.assertEqual(level.returnReachable((7, 3), "hallway"), [(3, 0), (7, 5)])

    def test_returnDownRightRoomFreeTiles(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))

        level = SnarlLevel([room1, room2],
                                [hallway])
        self.assertEqual(level.returnDownRightRoomFreeTiles(), [(10, 6), (8, 7), (9, 6), (8, 6), (8, 5), (9, 7)])

        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.returnDownRightRoomFreeTiles(), [(11, 16), (14, 17), (16, 16), (10, 6), (12, 12), (3, 11), (5, 13), (15, 16), (13, 17), (4, 12), (17, 16), (8, 5), (16, 17), (5, 12), (13, 16), (4, 13), (8, 6), (8, 16), (9, 7), (13, 11), (4, 10), (5, 11), (3, 13), (4, 14), (9, 16), (8, 7), (6, 12), (9, 6), (4, 11), (15, 17), (3, 12), (14, 16), (6, 13), (17, 17)])

    def test_returnUpperLeftRoomFreeTiles(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.returnUpperLeftRoomFreeTiles(), [(4, 1), (5, 1),
                            (6, 1), (4, 2), (5, 2),(6,2),(4, 3), (5, 3),
                            (6, 3), (4, 4)])


    def test_maxXminXmaxYminY(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.maxXminXmaxYminY(),[18, 2, 18, 0])


    def test_hallwayReturnReachable(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.hallwayReturnReachable((2,3)),[])
        self.assertEqual(level.hallwayReturnReachable((10,6)),[(7, 5), (12, 11)])
        self.assertEqual(level.hallwayReturnReachable((4,4)),[(3, 0), (2, 10)])


    def test_roomReturnReachable(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.roomReturnReachable((9,9)),[])
        self.assertEqual(level.roomReturnReachable((8,3)),[])
        self.assertEqual(level.roomReturnReachable((13,15)),[(8, 15)])
        self.assertEqual(level.roomReturnReachable((9,16)),[(2, 10), (13, 15)])



    def test_returnRoomWithGivenPosn(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.returnRoomWithGivenPosn((9,9)), None)
        self.assertEqual(level.returnRoomWithGivenPosn((4,10)), room4)
        self.assertEqual(level.returnRoomWithGivenPosn((8,3)), None)


    def test_returnHallwayPosnWithGivenPosn(self):
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),(6,2),
                        (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7),
                        (9, 7)], [(8, 5), (10, 6)], None)
        room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                        (12, 12)], {"exit": (13, 12)})
        room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                        (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                        (6, 13), (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
        room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                        [(8, 16), (11, 16)], {"key" : (10, 16)})
        room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                        (17, 16), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17)],
                        [(13, 16)], None)
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
        hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
        hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
        hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
        hallway5 = Hallway([], (11, 16), (13, 16))
        level = SnarlLevel([room1, room2, room3, room4, room5, room6],
                                [hallway, hallway1, hallway2, hallway3,
                                hallway4, hallway5])
        self.assertEqual(level.returnHallwayPosnWithGivenPosn((8,3)),[(6, 3), (8, 5)])
        self.assertEqual(level.returnHallwayPosnWithGivenPosn((13,6)),[(10, 6), (13, 11)])
        self.assertEqual(level.returnHallwayPosnWithGivenPosn((4,15)),[(4, 14), (8, 16)])
        self.assertEqual(level.returnHallwayPosnWithGivenPosn((13,12)),None)


    def test_InvalidLevel(self):
        hallway = Hallway([(8, 3)], (6, 3), (8, 5))
        room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2),
            (6,2), (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
        with self.assertRaises(Exception) as context:
            level = level = SnarlLevel([room1],[hallway, hallway])
        self.assertTrue('Hallways must not overlap hallways'
                                in str(context.exception))
        with self.assertRaises(Exception) as context:
            level = level = SnarlLevel([room1, room1],[hallway])
        self.assertTrue('Rooms must not overlap rooms'
                                in str(context.exception))
        with self.assertRaises(Exception) as context:
            room2 = Room((8, 3), 4, 4, [(8, 3)],[(8, 3)],None)
            level = level = SnarlLevel([room2],[hallway])
        self.assertTrue('Rooms must not overlap hallways'
                                in str(context.exception))

if __name__ == '__main__':
    unittest.main()
