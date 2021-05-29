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
        '''
        Constructor arguments:
        :param  __rooms:     list of Room, all the rooms in this level
        :param  __hallways   list of Hallway, all the hallways in this level
        '''
        # first check for validity
        self.__checkValidArgs(rooms, hallways)
        self.__rooms = rooms
        self.__hallways = hallways


    def maxXminXmaxYminY(self):
        """
        return the max X and min X value of thie level, meaning the right most x
        coordinate and left most y coordinate, and also max Y and min Y, meaning
        the top most y coordinate and down most y coordinate
        @rtype:     list of int
        @return:    [maxX, minX, maxY, minY]
        """
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

    """
    return the hallway end point, if the given room contains the start point
    of one of the hallway in this level
    @type   room:       Room
    @param  room:       the room where the hallway starts from
    @rtype:             tuple of int
    @return:            hallway end point
    """
    def returnHallwayPosnWithGivenRoom(self,room):
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


    def placeObject(self,obj, posn):
        """
        place an object on the map. Return True is placement is successful.
        Otherwise, return False
        @type    obj:      String
        @param   obj:      object
        @type   posn:      tuple of int
        @param  posn:      point hope to place the object
        @rtype:            boolean
        @return:           whether the placement is successful
        """
        bound = self.maxXminXmaxYminY()
        if posn[0] < bound[1] or posn[0] > bound[0]:
            return False
        if posn[1] > bound[2] or posn[1] < bound[3]:
            return False
        room = self.returnRoomWithGivenPosn(posn)
        if room is None:
            return False
        return room.placeObject(obj,posn)


    def returnReachable(self, point, type):
        """
        return the rooms that is reachable to the given point according to given
        string indicating type of the segment, "room" or "hallway" or "void"
        if the type is a room, return the rooms that is connect to the room that
        point is in, if the type if a hallway, return the rooms that this hallway
        connect to, else return empty.
        @type   point:      tuple of int
        @param  point:      point hope to check
        @type    type:      String
        @param   type:      type of the segment
        @rtype:             list
        @return:            hallways or rooms that can be reached to point
        point: a position in tupple(x, y) format
        """
        if type == "room":
            return self.roomReturnReachable(point)
        elif type == "hallway":
            return self.hallwayReturnReachable(point)
        else:
            return []


    def returnType(self, point):
        """
        return the type of the segment in this level that this point is located
        types including "room" if the point reside in a room, "hallway" if the point
        reside in a hallway, and "void" if it is outside of the level
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             String
        @return:            where is the point in this map
        """
        for room in self.__rooms:
            if not(room.returnReachable(point) == None):
                return "room"
        for hallway in self.__hallways:
            if hallway.checkTraversable(point):
                return "hallway"
        return "void"


    def returnRandomPosn(self):
        """
        return a position in a random room in this map
        @rtype:            tuple of int
        @return:           a random point in the room in this map
        """
        freetiles = self.returnDownRightRoomFreeTiles()
        return random.sample(freetiles, 1)[0]


    def draw(self):
        """
        draw the current level
        @rtype:     String
        @return:    all the information of this level
        """
        map = self.renderLevel()
        return self.drawMap(map)

    def drawMap(self, map):
        """
        render the given level into string format, by rendering each row and column
        @type   map:    2D array
        @param  map:    a map contains information about this level, including
                where room is located, where is all the objects, doors, non wall
                tiles and such
        @rtype:         String
        @return:        all the information from map
        """
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



    def renderLevel(self):
        """
        Gives a map that contains information about this level, including where
        room is located, where is all the objects, doors, non wall tiles and such
        First generate an default 2D array that create a list of N list of M cells
        which N will be the horizontal width, M will be the vertical width
        @rtype:     2D array
        @return:    map of this level
        """
        resultMap = self.__createEmptyMap(self)
        minX = resultMap[0][0][0]
        minY = resultMap[0][0][1]
        for room in self.__rooms:
            resultMap = room.renderRoom(resultMap, minX, minY)
        for hallway in self.__hallways:
            resultMap = hallway.renderHallway(resultMap, minX, minY)
        return resultMap


    @staticmethod
    def __checkValidArgs(rooms, hallways):
        """
        Check if the given argument for implementing a snarl level is legal
        by checking if hallways overlap hallways, rooms overlap rooms or
        rooms overlap hallways
        @type     rooms:      list of Room
        @param    rooms:      rooms used to construct this level
        @type  hallways:      list of Hallway
        @param hallways:      hallways used to construct this level
        """
        if(SnarlLevel.__checkAllHallwaysOverlapping(hallways)):
            raise Exception("Hallways must not overlap hallways")
        if(SnarlLevel.__checkAllRoomsOverlapping(rooms)):
            raise Exception("Rooms must not overlap rooms")
        if(SnarlLevel.__checkRoomsOverlapHallways(hallways, rooms)):
            raise Exception("Rooms must not overlap hallways")



    def hallwayReturnReachable(self, point):
        """
        return all the rooms that is reachable to the given point, assume the
        given point is inside a hallway of this level
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             list of Hallway
        @return:            hallways that can be reached to point
        """
        result = []
        if self.returnHallwayPosnWithGivenPosn(point) != None:
            hallwayPosn = self.returnHallwayPosnWithGivenPosn(point)
            hallwayStart = hallwayPosn[0]
            hallwayEnd = hallwayPosn[1]
            room1 = self.returnRoomWithGivenPosn(hallwayStart)
            room2 = self.returnRoomWithGivenPosn(hallwayEnd)
            room1Posn = room1.returnReachable(hallwayStart)
            room2Posn = room2.returnReachable(hallwayEnd)
            result+=[room1Posn]
            result+=[room2Posn]
        return result


    def roomReturnReachable(self, point):
        """
        return all the rooms that is reachable to the given point, assume the
        given point is inside a room of this level
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             list of Room
        @return:            rooms that can be reached to point
        """
        result = []
        if self.returnRoomWithGivenPosn(point) != None:
            room = self.returnRoomWithGivenPosn(point)
            hallwayPosn = self.returnHallwayPosnWithGivenRoom(room)
            for posn in hallwayPosn:
                room2 = self.returnRoomWithGivenPosn(posn)
                room2Posn = room2.returnReachable(posn)
                result+=[room2Posn]
        return result


    def checkTraversable(self, point):
        """
        check if the given point is traversable in this level by looking if
        it is inside of hallway or rooms and it is on none wall tiles
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             boolean
        @return:            whether given point is traversable in this level
        """
        for room in self.__rooms:
            if room.returnReachable(point) != None and room.returnReachable(point) != "walls":
                return True
                break
        for hallway in self.__hallways:
            if hallway.checkTraversable(point):
                return True
                break
        return False


    def returnDownRightRoomFreeTiles(self):
        """
        first check if the room is the most down right by looking at its room posn
        has maximum x y value and then return taht rooms non wall tiles
        @rtype:     list of tuple of int
        @return:    aall non wall tiles in the most down right room
        """
        rooms = self.__rooms
        result = []
        upperleft = self.returnUpperLeftRoomFreeTiles()
        for room in self.__rooms:
            result += room.returnFreeTiles()
        result = list(set(result) - set(upperleft))
        return result



    def returnUpperLeftRoomFreeTiles(self):
        """
        first check if the room is the most upper left by looking at its room posn
        has minimum x y value and then return taht rooms non wall tiles
        @rtype:     list of tuple of int
        @return:    all non wall tiles in the most upper left room
        """
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



    @staticmethod
    def __createEmptyMap(self):
        """
        generate an default 2D array that create a list of N list of M cells
        which N will be the horizontal width, M will be the vertical width
        cells will be the positions in tuple(int, int) format
        for example, 2D array for 2 2 with starting point (1, 1) will be
        [[(1, 1), (2, 1)][(1, 2), (2, 2)]]
        @rtype:     2D array
        @return:    map of this level
        """
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


    @staticmethod
    def __checkAllHallwaysOverlapping(hallways):
        """
        check there exsit any overlapping of hallway in this map by iterate each
        hallway and look if any hallway overlap its rest of the hallway list
        @type   hallways:   list of Hallway
        @param  hallways:   all the hallways hope to check
        @rtype:             boolean
        @return:            wether the overlapping exsists
        """
        for hallwayIndex in range(len(hallways)):
            hallway = hallways[hallwayIndex]
            # check if current hallway overlaps any hallway from
            # the rest of the list
            if SnarlLevel.__checkHallwaysContainHallway(
                                hallways[hallwayIndex + 1:], hallway):
                return True
        return False


    def returnRoomWithGivenPosn(self, point):
        """
        return the room if the given position if reachable in that room in this level
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             Room
        @return:            the room that can be reachable at given position
        """
        for room in self.__rooms:
            if room.returnReachable(point) != None:
                return room
                break
        return None


    def returnHallwayPosnWithGivenPosn(self, point):
        """
        return the hallway start point and endpoint if the given position is
        reachable in one of the hallway in this map
        @type   point:      tuple of int
        @param  point:      point hope to check
        @rtype:             list of tuple of int
        @return:            list contains start and end point of the hallway
        """
        for hallway in self.__hallways:
            if hallway.returnReachable(point) != None:
                return hallway.returnReachable(point)
                break
        return None


    @staticmethod
    def __checkRoomsOverlapHallways(hallways, rooms):
        """
        check if there is any overlapping between hallway list and room list by
        iterate each hallway and check if the any room in room list overlap the
        hallway
        @type   hallways:       List of Hallway
        @param  hallways:       hallways need to check
        @type      rooms:       List of Room
        @param     rooms:       rooms need to check
        @rtype:                 boolean
        @return:                whether the overlapping exsits
        """
        for hallway in hallways:
            if SnarlLevel.__checkRoomsContainHallway(hallway, rooms):
                return True
                break
        return False

    @staticmethod
    def __checkAllRoomsOverlapping(rooms):
        """
        check there exsit any overlapping of rooms in this map by iterate each room
        and look if any room overlap its rest of the room list
        @type   rooms:      List of Room
        @param  rooms:      rooms hope to check
        @rtype:             boolean
        @return:            whether the overlapping exsists
        """
        for roomIndex in range(len(rooms)):
            room = rooms[roomIndex]
            if SnarlLevel.__checkRoomsContainRoom(rooms[roomIndex + 1:], room):
                return True
        return False


    @staticmethod
    def __checkRoomsContainRoom(rooms, otherRoom):
        """
        check if the given otherRoom overlaps any room from given room list
        @type       rooms:      List of Room
        @param      rooms:      list of rooms hope to check
        @type   otherRoom:      Room
        @param  otherRoom:      room hope to check
        @rtype:                 boolean
        @return:                whether the list contains the same item
        """
        if(rooms == None):
            return False
        else:
            for room in rooms:
                if otherRoom.checkRoomsOverlap(room):
                    return True
        return False


    @staticmethod
    def __checkRoomsContainHallway(hallway, rooms):
        """
        check if the given hallway overlaps any room from the list
        @type    hallway:       Hallway
        @param   hallway:       hallway need to check
        @type      rooms:       List of Room
        @param     rooms:       rooms need to check
        @rtype:                 boolean
        @return:                whether the hallway overlaps any room
        """
        for room in rooms:
            if hallway.checkHallwayOverlapRoom(room):
                return True
        return False


    @staticmethod
    def __checkHallwaysContainHallway(hallways, otherhallway):
        """
        checks if otherhallway overlaps any hallway in the hallway list
        @type        hallways:   list of Hallway
        @param       hallways:   all the hallways hope to check
        @type   otherhallways:   Hallway
        @param  otherhallways:   the hallway hope to check
        @rtype:                  boolean
        @return:                 wether list contains the same hallway
        """
        if(hallways == None):
            return False
        else:
            for hallway in hallways:
                if otherhallway.checkHallwayOverlapHallway(hallway):
                    return True
        return False




    def returnJSON(self):
        """
        return the information of this level in standard JSON
        @rtype:     JSON
        @return:    information in this level
        """
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
