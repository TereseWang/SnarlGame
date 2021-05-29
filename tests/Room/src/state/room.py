#!/usr/bin/python3
import copy
"""
A Room class is composed of a top-left cartisian point, a sizeX indicating
horizontal width, and a sizeY indicating vertical width of the room. A tiles
is a list of non wall tiles that is inside of the room. A doorsPosns is a list
of door posns indicating all the positions of the doors in side this room.
Objects will be a dictionary containing a key representing type of object
(either a key or an exit), and a value representing the position of the object
"""
class Room:
    def __init__(self, roomPosn, sizeX, sizeY, tiles, doorsPosns, objects):
        #check if all the argument inputted is valid
        self.__checkValidArgument(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects)
        self.__roomPosn = roomPosn
        self.__roomSizeX = sizeX
        self.__roomSizeY = sizeY
        self.__nonWallTiles = tiles
        self.__doorsPosns = doorsPosns
        self.__objects = objects

    """
    place a given object to a given position in this room. Return whether the
    placement is successful
    object: String
    position: turple
    """
    def placeObject(self, obj,posn):
        if obj == "exit":
            if self.__objects == None:
                self.__objects = {"exit":posn}
            else:
                self.__objects["exit"] = posn
            return True
        if obj == "key":
            if posn in self.__nonWallTiles:
                if self.__objects == None:
                    self.__objects = {"key":posn}
                else:
                    self.__objects["key"] = posn
                return True
            return False
        return



    """
    Check if all the argument inputted for this room is valid, meaning size
    should be greater than 2, none wall tiles should be inside of the room,
    doors should be in non wall tiles and also at the boundary of the room.
    Objects need to be in non wall tiles also
    roomPosn: a list of room posns in tuple format
    sizeX: horizontal
    """
    @staticmethod
    def __checkValidArgument(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects):
        if not(sizeX >= 2 and sizeY >= 2):
            raise ValueError("Size is invalid please enter again")
        if not Room.__checkValidNonWallTiles(tiles, roomPosn, sizeX, sizeY):
            raise ValueError("Invalid nonewalltiles")
        #if not Room.__checkAllDoors(doorsPosns, tiles, roomPosn, sizeX, sizeY):
            #raise ValueError("Invalid doorposns")
        if not Room.__checkValidObjects(objects, tiles):
            raise ValueError("Invalid Objects")


    """
    check if the given point is reachable in this room, if it is not reachable
    return None, if it is inside the room but it is a wall, return "walls"
    else return top left cartisian position of this room
    point: a position represent in tuple(x, y) format
    """
    def returnReachable(self, point):
        points = [point]
        if self.__checkWithInNonWallTiles(points,self.__nonWallTiles):
            return self.returnRoomPosn()
        elif self.__checkPosnWithinRoom(point, self.__roomPosn, self.__roomSizeX, self.__roomSizeY):
            return "walls"
        else:
            return None

    """Return the top left cartisian position of this room"""
    def returnRoomPosn(self):
        return copy.deepcopy(self.__roomPosn)

    """
    return all the tiles that is in none wall tiles, excluding all the tiles
    that is occupied by the object
    """
    def returnFreeTiles(self):
        tiles = self.__nonWallTiles
        if self.__objects == None:
            return tiles
        else:
            objects = list(self.__objects.values())
            tiles = list(set(tiles) - set(objects))
            return tiles

    """Return all the non wall tiles of this room"""
    def returnNoneWallTiles(self):
        return copy.deepcopy(self.__nonWallTiles)

    """
    Render the room by inputting all the non wall tiles and doors and Objects
    inside the given map.
    map: a 2D array list of tuple coordinates
    minX: an integer indicating the most top left coordinate X of the map
    minY: an integer indicating the most top left coordinate Y of the map
    return type: 2D array list with doors replaced with "2", non wall tiles
    replaced with "1", key replaced with "k", exit replaced with "e"
    """
    def renderRoom(self, map, minX, minY):
        result = map
        plusX = 0 - minX
        plusY = 0 - minY
        """render non wall tiles first"""
        result = Room.__renderWallTiles(self, result, plusX, plusY)
        for tile in self.__nonWallTiles:
            result[tile[1] + plusY][tile[0] + plusX] = "1"
        """render doors upon non wall tiles"""
        result = Room.__renderDoors(self, result, plusX, plusY)
        """render objects upon all tiles"""
        result = Room.__renderObject(self, result, plusX, plusY)
        return result

    """
    return traversable points around the given point, if none return None
    point: tuple(int, int) indicating the position of the input point
    if input point is not found return None, else return a list of tuple points
    indicating all the traversable points around the input point, and in
    reverse order, meaning (x, y) will becomes [y, x]
    """
    def returnTraversablePoint(self, point):
        result = []
        if self.__checkPosnWithinRoom(point, self.__roomPosn,
                                        self.__roomSizeX, self.__roomSizeY):
            top = (point[0], point[1] - 1)
            left = (point[0] - 1, point[1])
            right = (point[0] + 1, point[1])
            down = (point[0], point[1] + 1)
            """generate a top left right bottom points and check if they are
            within the none wall tiles"""
            if self.__checkWithInNonWallTiles([top], self.__nonWallTiles):
                result += [[top[1], top[0]]]
            if self.__checkWithInNonWallTiles([left],self.__nonWallTiles):
                result += [[left[1], left[0]]]
            if self.__checkWithInNonWallTiles([right],self.__nonWallTiles):
                result += [[right[1], right[0]]]
            if self.__checkWithInNonWallTiles([down],self.__nonWallTiles):
                result += [[down[1], down[0]]]
        else:
            return None
        return result

    """
    check if the given hallway overlap this room
    hallways: List of Hallway tiles
    iterate through each hallway tile and check if any overlap the room
    """
    def checkHallwayRoomOverlap(self, hallway):
        for tile in hallway:
            if self.__checkPosnWithinRoom(tile, self.__roomPosn,
                    self.__roomSizeX, self.__roomSizeY):
                return True
                break
        return False

    """
    check if the given room overlap this room
    room2: the other Room class that need to check with
    """
    def checkRoomsOverlap(self, room2):
        room2SizeX = room2.__roomSizeX
        room2SizeY = room2.__roomSizeY
        room2Posn = room2.__roomPosn
        room2TopL = room2Posn
        room2TopR = (room2Posn[0] + room2SizeX - 1, room2Posn[1])
        room2DownL = (room2Posn[0], room2Posn[1] + room2SizeY - 1)
        room2DownR = (room2Posn[0] + room2SizeX - 1, room2Posn[1] + room2SizeY - 1)
        origin = self.__roomPosn
        sizeX = self.__roomSizeX
        sizeY = self.__roomSizeY
        result = self.__checkPosnWithinRoom(room2TopL, origin, sizeX, sizeY)
        result = result or self.__checkPosnWithinRoom(room2TopR, origin, sizeX, sizeY)
        result = result or self.__checkPosnWithinRoom(room2DownL, origin, sizeX, sizeY)
        result = result or self.__checkPosnWithinRoom(room2DownR, origin, sizeX, sizeY)
        return result

    """
    return the max X value in this room, which will be the x of the down right
    and max Y value in this room, which will be the y of the down right, same
    for min X and min Y.
    return a list of integers [maxX, minX, maxY, minY]
    """
    def maxXminXmaxYminY(self):
        maxX = self.__roomPosn[0]+ self.__roomSizeX - 1
        minX = self.__roomPosn[0]
        maxY = self.__roomPosn[1] + self.__roomSizeY - 1
        minY = self.__roomPosn[1]
        return [maxX, minX, maxY, minY]

    """
    return the information of this room in standard JSON
    """
    def returnJSON(self):
        result = { "type" : "room"}
        result["origin"] = self.__roomPosn
        result["bounds"] = { "rows" : self.__roomSizeY, "columns" : self.__roomSizeX}
        result["layout"] = []
        # using a 2D list to collect information of layout
        temp = []
        for y in range(self.__roomPosn[1], self.__roomPosn[1] + self.__roomSizeY):
            tempList = []
            for x in range(self.__roomPosn[0], self.__roomPosn[0] + self.__roomSizeX):
                tempList.append(0)
            temp.append(tempList)

        for posn in self.__nonWallTiles:
            realPosn = (posn[0] - self.__roomPosn[0], posn[1] - self.__roomPosn[1])
            temp[realPosn[1]][realPosn[0]] = 1

        for posn in self.__doorsPosns:
            realPosn = (posn[0] - self.__roomPosn[0], posn[1] - self.__roomPosn[1])
            temp[realPosn[1]][realPosn[0]] = 2

        result["layout"] =  temp

        if self.__objects != None:
            result["object"] = self.__objects
        return result

    """
    check if all the non wall tiles is within the range of this room and also
    the length of the none wall tiles is not zero
    tiles: List of tuple posns indicating all the non wall tiles
    roomPosn: upper left position point of this room
    sizeX: int indicating horizontal length of this room
    sizeY: int indicating vertical length of this room
    """
    @staticmethod
    def __checkValidNonWallTiles(tiles, roomPosn, sizeX, sizeY):
        if(len(tiles) == 0):
            return False
        else:
            for tile in tiles:
                if not Room.__checkPosnWithinRoom(tile, roomPosn, sizeX, sizeY):
                    return False
                    break
        return True

    """
    check if all doors is valid by taking look at each door and see if it is
    at the boundary of the room and to see if it is inside non wall tiles
    and also there should be at least one door
    doorsPosns: list of tuple posns indicating position of the doors inside
    nonewalltiles: list of tuple posns represent non wall tiles
    roomPosn: upper left position point of this room
    sizeX: int indicating horizontal length of this room
    sizeY: int indicating vertical length of this room
    """
    @staticmethod
    def __checkAllDoors(doorsPosns, nonewalltiles, roomPosn, sizeX, sizeY):
        if(len(doorsPosns) == 0):
            return False
        elif Room.__checkWithInNonWallTiles(doorsPosns, nonewalltiles):
            for doorPosn in doorsPosns:
                if not Room.__checkValidDoor(doorPosn, roomPosn, sizeX, sizeY):
                    return False
                    break
        else:
            return False
        return True


    """
    check if the given object list are valid by looking if they are all within
    non wall tiles
    objects: a dictionary with key to be the type of object and value be the
    position of the object
    nonewalltiles: list of tuple posns represent non wall tiles
    """
    @staticmethod
    def __checkValidObjects(objects, nonewalltiles):
        # if a room doesn't have any objects, use empty list instead of None
        if objects == None:
            return True
        else:
            objectList = list(objects.values())
            return Room.__checkWithInNonWallTiles(objectList, nonewalltiles)

    """
    render all the wall tiles by replacing all the wall tiles from tuple posn to "x"
    map: a 2D array list of tuple coordinates
    plusX: the number to offset the boundary if the left most position X of the
    given map is negative
    plusY: the number to offset the boundary if the upper most position Y of the
    given map is negative
    """
    @staticmethod
    def __renderWallTiles(self, map, plusX, plusY):
        result = map
        roomPosn = self.__roomPosn
        minX = roomPosn[0]
        minY = roomPosn[1]
        for y in range(minY, minY + self.__roomSizeY):
            for x in range(minX, minX + self.__roomSizeX):
                result[y + plusY][x + plusX] = "x"
        return result

    """
    render all the door tiles by replacing all the door posns from tuple posn to "2"
    map: a 2D array list of tuple coordinates
    plusX: the number to offset the boundary if the left most position X of the
    given map is negative
    plusY: the number to offset the boundary if the upper most position Y of the
    given map is negative
    """
    @staticmethod
    def __renderDoors(self, map, plusX, plusY):
        result = map
        for door in self.__doorsPosns:
            result[door[1] + plusY][door[0] + plusX] = "2"
        return result

    """
    render all the objects by replacing all the object posns from tuple posn to
    object type
    map: a 2D array list of tuple coordinates
    plusX: the number to offset the boundary if the left most position X of the
    given map is negative
    plusY: the number to offset the boundary if the upper most position Y of the
    given map is negative
    """
    @staticmethod
    def __renderObject(self, map, plusX, plusY):
        result = map
        if self.__objects == None:
            return result
        for key, value in self.__objects.items():
            if key == "key":
                result[value[1] + plusY][value[0] + plusX] = "k"
            elif key == "exit":
                result[value[1] + plusY][value[0] + plusX] = "e"
        return result

    """
    check if the given door is valid
    doorsPosn: a tuple posns indicating position of the door
    roomPosn: upper left position point of this room
    roomSizeX: int indicating horizontal length of this room
    roomSizeY: int indicating vertical length of this room
    """
    @staticmethod
    def __checkValidDoor(doorPosn, roomPosn, roomSizeX, roomSizeY):
        maxX = roomPosn[0] + roomSizeX - 1
        maxY = roomPosn[1] + roomSizeY - 1
        minX = roomPosn[0]
        minY = roomPosn[1]
        doorX = doorPosn[0]
        doorY = doorPosn[1]
        if doorX == maxX or doorX == minX:
            return doorY in range(minY, maxY + 1)
        else:
            if doorY == minY or doorY == maxY:
                return doorX in range(minX, maxX + 1)
            else:
                return False
        return False

    """
    check if the given posn is within the non wall tiles
    posns: a posn in tuple(int, int) format
    nonewalltiles: a list of tuple posns representing non wall tiles
    """
    @staticmethod
    def __checkWithInNonWallTiles(posns, nonewalltiles):
        noneWallSet = set(nonewalltiles)
        posnSet = set(posns)
        return posnSet.issubset(noneWallSet)


    """
    check if the given posn is within the room
    posn: a posn in tuple(int, int) format
    origin: upper left position point of this room
    sizeX: int indicating horizontal length of this room
    sizeY: int indicating vertical length of this room
    """
    @staticmethod
    def __checkPosnWithinRoom(posn, origin, sizeX, sizeY):
        inputPointX = posn[0]
        inputPointY = posn[1]
        originX = origin[0]
        originY = origin[1]
        withinX = inputPointX in range(originX, originX + sizeX)
        withinY = inputPointY in range(originY, originY + sizeY)
        return withinX and withinY
