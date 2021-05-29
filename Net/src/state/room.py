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
        '''
        Constructor arguments:
        :param  __roomPosn:     tuple of int, (x,y) uppper left position of this room
        :param  __roomSizeX:    int, the horizontal length of this room
        :param  __roomSizeY:    int, the vertical length of this room
        :param  _nonWallTiles:  list of tuple of int, all non-wall tiles in this room
        :param  __doorsPosns:   list of tuple of int, all the door positions in this room
        :param  __objects:      dictionary, the placement of all the objects
        '''
        #check if all the argument inputted is valid
        self.__checkValidArgument(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects)
        self.__roomPosn = roomPosn
        self.__roomSizeX = sizeX
        self.__roomSizeY = sizeY
        self.__nonWallTiles = tiles
        self.__doorsPosns = doorsPosns
        self.__objects = objects




    def returnJSON(self):
        """
        return the information of this room in standard JSON
        @rtype:     JSON
        @return:    all the information of this room
        """
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





    def returnTraversablePoint(self, point):
        """
        return traversable points around the given point, if none return None.
        Otherwise return a list of tuple points indicating all the traversable
        points around the input point, and in reverse order, meaning (x, y) will
        becomes [y, x]
        @type   point:  tuple of int
        @param  point:  (int, int), representing a position
        @rtype:         list of tuple of int
        @return:        all the points that can be reached from given point
        """
        result = []
        if self.__checkPosnWithinRoom(point, self.__roomPosn,
                                        self.__roomSizeX, self.__roomSizeY):
            top = (point[0], point[1] - 1)
            left = (point[0] - 1, point[1])
            right = (point[0] + 1, point[1])
            down = (point[0], point[1] + 1)
            # generate a top left right bottom points and check if they are
            # within the none wall tiles
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


    def checkRoomsOverlap(self, room2):
        """
        check if the given room overlap this room.
        @type   room2:      Room
        @param  room2:      the other room we hope to check for overlapping
        @rtype:             boolean
        @return:            whether there is overlapping between this room and
                        given room
        """
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




    def placeObject(self, obj,posn):
        """
        place a given object to a given position in this room. Return whether the
        placement is successful
        @type    object:    string
        @param   object:    the object at given position
        @type    posn:      tuple of int
        @param   posn:      position in the map
        @rtype:             boolean
        @return:            whether the placement is successful
        """
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
        return False



    def renderRoom(self, map, minX, minY):
        """
        Render the room by inputting all the non wall tiles and doors and Objects
        inside the given map. Gives back 2D a array list with doors replaced with
        "2", non wall tiles replaced with "1", key replaced with "k", exit replaced
        with "e"
        @type   map:    2D list
        @param  map:    room information
        @type  minX:    int
        @param minX:    upper left horizontal coordinate value of the map
        @type  minY:    int
        @param minY:    upper left vertical coordinate value of the map
        @rtype:         2D list
        @return:        updated map with this room rendered on
        """
        result = map
        plusX = 0 - minX
        plusY = 0 - minY
        #render non wall tiles first
        result = Room.__renderWallTiles(self, result, plusX, plusY)
        for tile in self.__nonWallTiles:
            result[tile[1] + plusY][tile[0] + plusX] = "1"
        #render doors upon non wall tiles
        result = Room.__renderDoors(self, result, plusX, plusY)
        #render objects upon all tiles
        result = Room.__renderObject(self, result, plusX, plusY)
        return result



    @staticmethod
    def __renderWallTiles(self, map, plusX, plusY):
        """
        render all the wall tiles by replacing all the wall tiles from tuple posn to "x"
        @type     map:     of tuple of int
        @param    map:    the information of a map
        @type   plusX:    int
        @param  pluxX:    the number to offset the boundary if the left most
                        position X of the given map is negative
        @type   plusY:    int
        @param  pluxY:    the number to offset the boundary if the left most
                        position Y of the given map is negative
        """
        result = map
        roomPosn = self.__roomPosn
        minX = roomPosn[0]
        minY = roomPosn[1]
        for y in range(minY, minY + self.__roomSizeY):
            for x in range(minX, minX + self.__roomSizeX):
                result[y + plusY][x + plusX] = "x"
        return result


    @staticmethod
    def __renderObject(self, map, plusX, plusY):
        """
        render all the objects by replacing all the object posns from tuple posn to
        object type
        @type     map:    2D list
        @param    map:    the information of a map
        @type   plusX:    int
        @param  pluxX:    the number to offset the boundary if the left most
                        position X of the given map is negative
        @type   plusY:    int
        @param  pluxY:    the number to offset the boundary if the left most
                        position Y of the given map is negative
        @rtype:           2D list
        @return:          updated map with the object in this room rendered on
        """
        result = map
        if self.__objects == None:
            return result
        for key, value in self.__objects.items():
            if key == "key":
                result[value[1] + plusY][value[0] + plusX] = "k"
            elif key == "exit":
                result[value[1] + plusY][value[0] + plusX] = "e"
        return result


    @staticmethod
    def __renderDoors(self, map, plusX, plusY):
        """
        render all the door tiles by replacing all the door posns from tuple
        posn to "2"
        @type     map:    2D list
        @param    map:    the information of a map
        @type   plusX:    int
        @param  pluxX:    the number to offset the boundary if the left most
                        position X of the given map is negative
        @type   plusY:    int
        @param  pluxY:    the number to offset the boundary if the left most
                        position Y of the given map is negative
        @rtype:            2D list
        @return:            updated map with the doors of this room rendered on
        """
        result = map
        for door in self.__doorsPosns:
            result[door[1] + plusY][door[0] + plusX] = "2"
        return result




    @staticmethod
    def __checkValidArgument(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects):
        """
        Check if all the argument inputted for this room is valid, meaning size
        should be greater than 2, none wall tiles should be inside of the room,
        doors should be in non wall tiles and also at the boundary of the room.
        Objects need to be in non wall tiles also
        @type    roomPosn:      list of tuple of int
        @param   roomPosn:      a list of room upper left points
        @type       sizeX:      int
        @param      sizeX:      the horizontal size of a room
        @type       sizeY:      int
        @param      sizeY:      the vertical size of a room
        @type       tiles:      list of tuple of int
        @param      tiles:      non wall tiles in a room
        @type   doorPosns:      list of tuple of int
        @param  doorPosns:      the positions of doors in a room
        @type     objects:      dictionary
        @param    objects:      object value and location information
        """
        if not(sizeX >= 2 and sizeY >= 2):
            raise ValueError("Size is invalid please enter again")
        if not Room.__checkValidNonWallTiles(tiles, roomPosn, sizeX, sizeY):
            raise ValueError("Invalid nonewalltiles")
        if not Room.__checkValidObjects(objects, tiles):
            raise ValueError("Invalid Objects")



    @staticmethod
    def __checkValidNonWallTiles(tiles, roomPosn, sizeX, sizeY):
        """
        check if all the non wall tiles is within the range of a room. The input
        non-wall tile list cannot be empty
        @type       tiles:  list of tuple of int
        @param      tiles:  non wall tiles hope to check
        @type    roomPosn:  tuple of int
        @param   roomPosn:  the upper left position of a room
        @type       sizeX:  int
        @param      sizeX:  horizontal length of a room
        @type:      sizeY:  int
        @param      sizeY:  vertical length of a room
        @rtype:             boolean
        @return:            whether given none wall tiles are the range of given room
        """
        if(len(tiles) == 0):
            return False
        else:
            for tile in tiles:
                if not Room.__checkPosnWithinRoom(tile, roomPosn, sizeX, sizeY):
                    return False
                    break
        return True



    @staticmethod
    def __checkValidObjects(objects, nonewalltiles):
        """
        check if the given object list are valid by looking if they are all within
        non wall tiles
        @type         objects:    dictionary
        @param        objects:    {posn: object} giving all the location of objects
        @type   nonewalltiles:    list of tuple of int
        @param  nonewalltiles:    list of posns of non wall tiles
        """
        # if a room doesn't have any objects, use empty list instead of None
        if objects == None:
            return True
        else:
            objectList = list(objects.values())
            return Room.__checkWithInNonWallTiles(objectList, nonewalltiles)




    def checkHallwayRoomOverlap(self, hallway):
        """
        iterate through each hallway tile and check if any overlap the room
        and check if the given hallway overlap this room
        @type   hallway:    list of tuple of int
        @param  hallway:    hallway tiles
        @rtype:             boolean
        @return:            whether given hallway overlaps with this room
        """
        for tile in hallway:
            if self.__checkPosnWithinRoom(tile, self.__roomPosn,
                    self.__roomSizeX, self.__roomSizeY):
                return True
                break
        return False



    def returnReachable(self, point):
        """
        check if the given point is reachable in this room, if it is not reachable
        return None, if it is inside the room but it is a wall, return "walls"
        else return top left cartisian position of this room
        @type   point:      tuple of int
        @param  point:      a position
        @rtype:             String if given point is a wall
                            tuple of int if given point is nonWallTile in this room
                            None if given point is not in the room
        @return:            the information of given point in this room
        """
        points = [point]
        if self.__checkWithInNonWallTiles(points,self.__nonWallTiles):
            return self.returnRoomPosn()
        elif self.__checkPosnWithinRoom(point, self.__roomPosn, self.__roomSizeX, self.__roomSizeY):
            return "walls"
        else:
            return None

    @staticmethod
    def __checkPosnWithinRoom(posn, origin, sizeX, sizeY):
        """
        check if the given posn is within the room
        @type       posn:     tuple of int
        @param      posn:     a position hope to be checked
        @type     origin:     tuple of int
        @param    origin:     upper left position point of the room
        @type      sizeX:     int
        @param     sizeX:     horizontal length of the room
        @type      sizeY:     int
        @param     sizeY:     vertical length of the room
        @rtype:               boolean
        @return:              whether given position is in the given room
        """
        inputPointX = posn[0]
        inputPointY = posn[1]
        originX = origin[0]
        originY = origin[1]
        withinX = inputPointX in range(originX, originX + sizeX)
        withinY = inputPointY in range(originY, originY + sizeY)
        return withinX and withinY


    def returnFreeTiles(self):
        """
        return all the tiles that is in none wall tiles, excluding all the tiles
        that is occupied by the object
        @rtype:     list of tuple of int
        @return:    all the positions of none wall tiles that are vacant
        """
        tiles = self.__nonWallTiles
        if self.__objects == None:
            return tiles
        else:
            objects = list(self.__objects.values())
            tiles = list(set(tiles) - set(objects))
            return tiles


    @staticmethod
    def __checkAllDoors(doorsPosns, nonewalltiles, roomPosn, sizeX, sizeY):
        """
        check if all doors is valid by taking look at each door and see if it is
        at the boundary of the room and to see if it is inside non wall tiles
        and also there should be at least one door
        @type       doorsPosns:     list of tuple of int
        @param      doorsPosns:     position of the doors in side the room
        @type    nonewalltiles:     list of tuple of int
        @param   nonewalltiles:     all the non wall tile position in the room
        @type         roomPosn:     tuple of int
        @param        roomPosn:     upper left position point of the room
        @type            sizeX:     int
        @param           sizeX:     horizontal length of the room
        @type            sizeY:     int
        @param           sizeY:     vertical length of the room
        @rtype:                     boolean
        @return:                    whether all the door position is valid
        """
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



    @staticmethod
    def __checkValidDoor(doorPosn, roomPosn, roomSizeX, roomSizeY):
        """
        check if the given door is valid
        @type       doorPosn:   tuple of int
        @param      doorPosn:   the position of the door
        @type       roomPosn:   tuple of int
        @param      roomPosn:   the upper left point position of the room
        @type       roomSizeX:  int
        @param      roomSizeX:  horizontal length of the room
        @type       roomSizeY:  int
        @param      roomSizeY:  vertical length of the room
        @rtype:                 boolean
        @return:                whether the given door position is valid
        """
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




    def maxXminXmaxYminY(self):
        """
        return the max X value in this room, which will be the x of the down right
        and max Y value in this room, which will be the y of the down right, same
        for min X and min Y.
        @rype:          list of tuple of int
        @return:        the boundary horizontal and vertical coorindate value
                    of this room
        """
        maxX = self.__roomPosn[0]+ self.__roomSizeX - 1
        minX = self.__roomPosn[0]
        maxY = self.__roomPosn[1] + self.__roomSizeY - 1
        minY = self.__roomPosn[1]
        return [maxX, minX, maxY, minY]



    @staticmethod
    def __checkWithInNonWallTiles(posns, nonewalltiles):
        """
        check if the given posn is within the non wall tiles
        @type           posns:  tuple of int
        @param          posns:  the position hope to be checked
        @type   nonewalltiles:  list of tuple of int
        @param  nonewalltiles:  all the non-wall tiles
        @rtype:                 boolean
        @return:                whether given posn is in the given non wall tiles
        """
        noneWallSet = set(nonewalltiles)
        posnSet = set(posns)
        return posnSet.issubset(noneWallSet)




    def returnRoomPosn(self):
        """
        Return the top left cartisian position of this room
        @rtype:     tuple of int
        @return:    the upper left point positon of this room
        """
        return copy.deepcopy(self.__roomPosn)




    def returnNoneWallTiles(self):
        """
        Return a copy of all the non wall tiles of this room
        @rtype:     list of tuples of int
        @return:    all the none wall tiles in this room
        """
        return copy.deepcopy(self.__nonWallTiles)
