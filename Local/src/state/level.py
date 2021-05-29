from src.state.room import Room
from src.state.hallway import Hallway
import copy
import random
"""
A SnarlLevel is a class that is composed of a list of Rooms Class
and a list of hallways
"""
class SnarlLevel:
    def __init__(self, rooms, hallways):
        self.__checkValidArgs(rooms, hallways)
        self.__rooms = rooms
        self.__hallways = hallways

    """
    Check if the given argument for implementing a snarl level is legal
    by checking if hallways overlap hallways, rooms overlap rooms or
    rooms overlap hallways
    """
    @staticmethod
    def __checkValidArgs(rooms, hallways):
        if(SnarlLevel.__checkAllHallwaysOverlapping(hallways)):
            raise Exception("Hallways must not overlap hallways")
        if(SnarlLevel.__checkAllRoomsOverlapping(rooms)):
            raise Exception("Rooms must not overlap rooms")
        if(SnarlLevel.__checkRoomsOverlapHallways(hallways, rooms)):
            raise Exception("Rooms must not overlap hallways")

    """
    check if the given point is traversable in this level by looking if
    it is inside of hallway or rooms and it is on none wall tiles
    point: a position in tupple(x, y) format
    """
    def checkTraversable(self, point):
        for room in self.__rooms:
            if room.returnReachable(point) != None and room.returnReachable(point) != "walls":
                return True
                break
        for hallway in self.__hallways:
            if hallway.checkTraversable(point):
                return True
                break
        return False

    """
    place an object on the map. Return True is placement is successful.
    Otherwise, return False
    obj: String
    posn: turple
    """
    def placeObject(self,obj, posn):
        bound = self.maxXminXmaxYminY()
        if posn[0] < bound[1] or posn[0] > bound[0]:
            return False
        if posn[1] > bound[2] or posn[1] < bound[3]:
            return False
        room = self.returnRoomWithGivenPosn(posn)
        if room is None:
            return False
        result = room.placeObject(obj,posn)
        return result

    """
    return a position in a random room in this map
    """
    def returnRandomPosn(self):
        freetiles = self.returnDownRightRoomFreeTiles()
        return random.sample(freetiles, 1)[0]

    """
    return the type of the segment in this level that this point is located
    types including "room" if the point reside in a room, "hallway" if the point
    reside in a hallway, and "void" if it is outside of the level
    point: a position in tupple(x, y) format
    """
    def returnType(self, point):
        result = "void"
        for room in self.__rooms:
            if not(room.returnReachable(point) == None):
                result = "room"
                return result
                break
        for hallway in self.__hallways:
            if hallway.checkTraversable(point):
                result = "hallway"
                break
        return result


    """
    return the rooms that is reachable to the given point according to given
    type
    point: a position in tupple(x, y) format
    type: a string indicating type of the segment, "room" or "hallway" or "void"
    if the type is a room, return the rooms that is connect to the room that
    point is in, if the type if a hallway, return the rooms that this hallway
    connect to, else return empty.
    """
    def returnReachable(self, point, type):
        if type == "room":
            return self.__roomReturnReachable(point)
        elif type == "hallway":
            return self.__hallwayReturnReachable(point)
        else:
            return []

    """
    return all non wall tiles in the most upper left room
    first check if the room is the most upper left by looking at its room posn
    has minimum x y value and then return taht rooms non wall tiles
    """
    def returnUpperLeftRoomFreeTiles(self):
        rooms = self.__rooms
        x = rooms[0].returnRoomPosn()[0]
        y = rooms[0].returnRoomPosn()[1]
        result = rooms[0].returnNoneWallTiles()
        for room in self.__rooms:
            roomPosn = room.returnRoomPosn()
            if roomPosn[1] < y and roomPosn[0] < x:
                result = room.returnNoneWallTiles()
            elif roomPosn[1] < y:
                result = room.returnNoneWallTiles()
        return result

    """
    return all non wall tiles in the most down right room
    first check if the room is the most down right by looking at its room posn
    has maximum x y value and then return taht rooms non wall tiles
    """
    def returnDownRightRoomFreeTiles(self):
        rooms = self.__rooms
        result = []
        upperleft = self.returnUpperLeftRoomFreeTiles()
        for room in self.__rooms:
            result += room.returnFreeTiles()
        result = list(set(result) - set(upperleft))
        return result

    """
    draw the current level
    """
    def draw(self):
        map = self.renderLevel()
        return self.drawMap(map)


    """
    check there exsit any overlapping of hallway in this map by iterate each
    hallway and look if any hallway overlap its rest of the hallway list
    hallways: List of Hallway Class
    """
    @staticmethod
    def __checkAllHallwaysOverlapping(hallways):
        for hallwayIndex in range(len(hallways)):
            hallway = hallways[hallwayIndex]
            # check if current hallway overlaps any hallway from
            # the rest of the list
            if SnarlLevel.__checkHallwaysContainHallway(
                                hallways[hallwayIndex + 1:], hallway):
                return True
        return False

    """
    check there exsit any overlapping of rooms in this map by iterate each room
    and look if any room overlap its rest of the room list
    rooms: List of Room Class
    """
    @staticmethod
    def __checkAllRoomsOverlapping(rooms):
        for roomIndex in range(len(rooms)):
            room = rooms[roomIndex]
            if SnarlLevel.__checkRoomsContainRoom(rooms[roomIndex + 1:], room):
                return True
        return False

    """
    check if there is any overlapping between hallway list and room list by
    iterate each hallway and check if the any room in room list overlap the
    hallway
    hallways: List of Hallway class
    rooms: List of Room class
    """
    @staticmethod
    def __checkRoomsOverlapHallways(hallways, rooms):
        for hallway in hallways:
            if SnarlLevel.__checkRoomsContainHallway(hallway, rooms):
                return True
                break
        return False

    """
    render the given level into string format, by rendering each row and column
    map: A 2D Array that contains information about this level, including where
    room is located, where is all the objects, doors, non wall tiles and such
    """
    def drawMap(self, map):
        result = ""
        for row in map:
            rowString = ""
            for cell in row:
                if cell == "1":
                    rowString += "  "
                elif cell == "2":
                    rowString += " 2"
                elif cell == "x":
                    rowString += " x"
                elif cell == "k":
                    rowString += " k"
                elif cell == "e":
                    rowString += " e"
                elif cell == "+":
                    rowString += " +"
                elif type(cell) == tuple:
                    rowString+= "  "
                else:
                    rowString+= " {0}".format(cell)
            result+=rowString+"\n"
        return result

    """
    return a 2D array that contains information about this level, including where
    room is located, where is all the objects, doors, non wall tiles and such
    First generate an default 2D array that create a list of N list of M cells
    which N will be the horizontal width, M will be the vertical width
    """
    def renderLevel(self):
        resultMap = self.__createEmptyMap(self)
        minX = resultMap[0][0][0]
        minY = resultMap[0][0][1]
        for room in self.__rooms:
            resultMap = room.renderRoom(resultMap, minX, minY)
        for hallway in self.__hallways:
            resultMap = hallway.renderHallway(resultMap, minX, minY)
        return resultMap

    """
    return all the rooms that is reachable to the given point, assume the
    given point is inside a room of this level
    point: a position inside of a room of this level in tuple(x, y) format
    """
    def __roomReturnReachable(self, point):
        result = []
        if self.returnRoomWithGivenPosn(point) != None:
            room = self.returnRoomWithGivenPosn(point)
            hallwayPosn = self.returnHallwayPosnWithGivenRoom(room)
            for posn in hallwayPosn:
                room2 = self.returnRoomWithGivenPosn(posn)
                room2Posn = room2.returnReachable(posn)
                result+=[room2Posn]
        return result

    """
    return all the rooms that is reachable to the given point, assume the
    given point is inside a hallway of this level
    point: a position inside of a hallway of this level in tuple(x, y) format
    """
    def __hallwayReturnReachable(self, point):
        result = []
        if self.__returnHallwayPosnWithGivenPosn(point) != None:
            hallwayPosn = self.__returnHallwayPosnWithGivenPosn(point)
            hallwayStart = hallwayPosn[0]
            hallwayEnd = hallwayPosn[1]
            room1 = self.returnRoomWithGivenPosn(hallwayStart)
            room2 = self.returnRoomWithGivenPosn(hallwayEnd)
            room1Posn = room1.returnReachable(hallwayStart)
            room2Posn = room2.returnReachable(hallwayEnd)
            result+=[room1Posn]
            result+=[room2Posn]
        return result

    """
    checks if otherhallway overlaps any hallway in the hallway list
    hallways: List of Hallway
    otherhallway: Hallway
    """
    @staticmethod
    def __checkHallwaysContainHallway(hallways, otherhallway):
        if(hallways == None):
            return False
        else:
            for hallway in hallways:
                if otherhallway.checkHallwayOverlapHallway(hallway):
                    return True
        return False

    """
    check if the given otherRoom overlaps any room from given room list
    rooms: List of Room
    otherRoom: Room
    """
    @staticmethod
    def __checkRoomsContainRoom(rooms, otherRoom):
        if(rooms == None):
            return False
        else:
            for room in rooms:
                if otherRoom.checkRoomsOverlap(room):
                    return True
        return False

    """
    check if the given hallway overlaps any room from the list
    hallway: Hallway
    rooms: List of Room
    """
    @staticmethod
    def __checkRoomsContainHallway(hallway, rooms):
         for room in rooms:
             if hallway.checkHallwayOverlapRoom(room):
                 return True
                 break
         return False

    """
    generate an default 2D array that create a list of N list of M cells
    which N will be the horizontal width, M will be the vertical width
    cells will be the positions in tuple(int, int) format
    for example, 2D array for 2 2 with starting point (1, 1) will be
    [[(1, 1), (2, 1)][(1, 2), (2, 2)]]
    """
    @staticmethod
    def __createEmptyMap(self):
        maxXminXmaxYminY = SnarlLevel.maxXminXmaxYminY(self)
        maxX = maxXminXmaxYminY[0]
        minX = maxXminXmaxYminY[1]
        maxY = maxXminXmaxYminY[2]
        minY = maxXminXmaxYminY[3]
        result = []
        for y in range(minY, maxY + 1):
            row = []
            for x in range(minX, maxX + 1):
                row+=[(x, y)]
            result += [row]
        return result

    """
    return the hallway start point and endpoint if the given position is
    reachable in one of the hallway in this map
    posn: a position in tuple(x, y) format
    """
    def __returnHallwayPosnWithGivenPosn(self, posn):
        for hallway in self.__hallways:
            if hallway.returnReachable(posn) != None:
                return hallway.returnReachable(posn)
                break
        return None

    """
    return the room if the given position if reachable in that room in this level
    posn: a position in tuple(x, y) format
    """
    def returnRoomWithGivenPosn(self, point):
        for room in self.__rooms:
            if room.returnReachable(point) != None:
                return room
                break
        return None


    """
    return the information of this level in standard JSON
    """
    def returnJSON(self):
        result = { "type": "level", "rooms": [], "hallways": [],
        "objects": []}

        temp = []
        for room in self.__rooms:

            dic = room.returnJSON()
            if "object" in dic.keys():
                for type in dic["object"].keys():
                    result["objects"].append({type: dic["object"][type]})
                del dic["object"]
            temp.append(dic)

        result["rooms"] = temp

        temp = []
        for hallway in self.__hallways:
            dic = hallway.returnJSON()
            temp.append(dic)

        result["hallways"] = temp

        return result



    """
    return the hallway end point, if the given room contains the start point
    of one of the hallway in this level
    room: One Room Class
    """
    def __returnHallwayPosnWithGivenRoom(self, room):
        result = []
        for hallway in self.__hallways:
            path = hallway.generteHallway()
            start = path[0]
            end = path[len(path) - 1]
            if room.returnReachable(start) != None:
                result += [end]
            elif room.returnReachable(end) != None:
                result += [start]
        return result


    """
    return the max X and min X value of thie level, meaning the right most x
    coordinate and left most y coordinate, and also max Y and min Y, meaning
    the top most y coordinate and down most y coordinate
    return a list of integers [maxX, minX, maxY, minY]
    """
    def maxXminXmaxYminY(self):
        rooms = copy.deepcopy(self.__rooms)
        maxXminXmaxYminY = rooms[0].maxXminXmaxYminY()
        maxX = maxXminXmaxYminY[0]
        minX = maxXminXmaxYminY[1]
        maxY = maxXminXmaxYminY[2]
        minY = maxXminXmaxYminY[3]
        for room in rooms:
            roomMaxMinXY = room.maxXminXmaxYminY()
            maxX = max(roomMaxMinXY[0], maxX)
            minX = min(roomMaxMinXY[1], minX)
            maxY = max(roomMaxMinXY[2], maxY)
            minY = min(roomMaxMinXY[3], minY)
        hallways = copy.deepcopy(self.__hallways)
        for hallway in hallways:
            hallwayMaxMinXY = hallway.maxXminXmaxYminY()
            maxX = max(hallwayMaxMinXY[0], maxX)
            minX = min(hallwayMaxMinXY[1], minX)
            maxY = max(hallwayMaxMinXY[2], maxY)
            minY = min(hallwayMaxMinXY[3], minY)
        return [maxX, minX, maxY, minY]


if __name__ == '__main__':
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
    print(level.draw())
