from src.state.level import SnarlLevel
from src.state.room import Room
from src.state.hallway import Hallway
import sys
import src.parse_json as pj
import math
import random
from scipy.spatial import Delaunay
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import json as js

#----------------------Part 1 Generate Randomly sized rooms -------------------
# Instead of generating a list of rooms, we decide to generate a list of room
# information, which each info will contain a posn indicating the position
# of the upper left of the room and the width and height of the room
class SnarlLevelGenerator():
    def __init__(self, numRooms, min, max, json, render):
        self.numRooms = numRooms
        self.min = min
        self.max = max
        self.json = json
        self.render = render

    """
    generate a list of rooms info based on the number of rooms wanted
    @rtype: List of tuple of ((number, number), number, number)
    @return: List of rooms info, which contains information about the room
    """
    def generateRoomsInfo(self):
        result = []
        for i in range(0, self.numRooms):
            info = self.generateSingleRoomInfo(max(self.max[0], self.max[1]))
            result += [info]
        return result

    """
    generate info for single room including a position within a circle of
    given radius with origin to be (0, 0) and the width and height of the room
    @type radius: integer
    @param radius: the radius of the circle
    @rtype: [(number, number), number, number]
    @return: [(x, y), width, height]
    """
    def generateSingleRoomInfo(self, radius):
        t = 2 * math.pi * random.uniform(0, 1)
        u = random.uniform(0, 1) + random.uniform(0, 1)
        r = None
        if u > 1:
            r = 2 - u
        else:
            r = u
        x = math.floor(radius * r * math.cos(t))
        y = math.floor(radius * r * math.sin(t))
        posn = (x, y)
        width = math.floor(random.uniform(self.min[0], self.max[0] + 1))
        height = math.floor(random.uniform(self.min[1], self.max[1] + 1))
        return [posn, width, height]

#--------------------------------Part 2 Seperate Rooms ------------------------
# We will sort the list of room info based on the position and then we will
# spread the rooms from upper left to down right, instead of from the center,
# for simplicity purpose, we will use room info here
    """
    First sort the list of room information, arrange them in the order from
    top left to the buttom right. Then, keep moving the rooms away from each
    other until there is more overlapping.
    @type listRooms: List of [(number, number), number, number]
    @param listRooms: list of room info in the form:
                        [(x0, y0), x, y]
                        (x0, y0): the tuple representing the origin of a room
                        x: int representing the width of a room
                        y: int representing the height of a room
    @rtype: List of [(number, number), number, number]
    @return: seperated list of rooms info 
    """
    def seperationMove(self, listRooms):
        listRooms = self.sortRoom(listRooms)
        listRooms = copy.deepcopy(listRooms)
        while(self.checkAllRoomsOverlapping(listRooms)):
            listRooms = self.seperationMoveHelper(listRooms)
            listRooms.reverse()
        return listRooms

    """
    Run a loop going through all the room information in the list. Use a helper
    function to find the normolized vector of the direction we should move the
    room to. Continue the process of find direction and move until there is no
    more overlapping or cannot move any more.
    inputlist: list of room info in the form:
    [(x0, y0), x, y]
    (x0, y0): the tuple representing the origin of a room
    x: int representing the width of a room
    y: int representing the height of a room
    """
    def seperationMoveHelper(self, inputlist):
        inputlist = copy.deepcopy(inputlist)
        for i in range (0, len(inputlist)):
            roomPosn = inputlist[i][0]
            dirNorm = self.findGoingDirectionNorm(inputlist, i)
            totalMove = (0,0)
            while(dirNorm[0] != 0 or dirNorm[1] != 0):
                inputlist[i][0] = (roomPosn[0] + dirNorm[0] , roomPosn[1] + dirNorm[1])
                roomPosn = inputlist[i][0]
                dirNorm = self.findGoingDirectionNorm(inputlist, i)
                # solve infinite loop
                if totalMove[0] == 0 and totalMove[1] == 0:
                    break
                totalMove = (totalMove[0] + dirNorm[0], totalMove[1] + dirNorm[1])
        return inputlist

    """
    Return a tuple representing the next movement of given room. Use all the
    room posns of rooms that overlap with the given one to find the next move.
    Make the given room going away from its neighbours.
    i: int, index of the room we are going to move in the given room info list
    list: list of room info in the form:
    [(x0, y0), x, y]
    (x0, y0): the tuple representing the origin of a room
    x: int representing the width of a room
    y: int representing the height of a room
    """
    def findGoingDirectionNorm(self, list, i):
        result = [0,0]
        for ii in range(0,len(list)):
            if ii != i:
                # if overlap exsist for these two rooms
                if self.checkRoomsOverlap(list[i], list[ii]) or self.checkRoomsOverlap(list[ii], list[i]):
                    if list[i][0][0] == list[ii][0][0] and list[i][0][1] == list[i][0][1]:
                        result[0] -= 1
                        result[1] -= 1
                    else:
                        # use the ii room posn to fix our norm vector
                        result[0] += list[ii][0][0] - list[i][0][0]
                        result[1] += list[ii][0][1] - list[i][0][1]
        return (result[0] * -1, result[1] * -1)

    """
    check if there is any room that overlap with any other room
    rooms: [(x, y), width, height] a list of rooms info which contains
            the position of the room in tuple style and width and height of
            this room
    """
    def checkAllRoomsOverlapping(self, rooms):
        for roomIndex in range(len(rooms) - 1):
            room = rooms[roomIndex]
            if self.checkRoomsContainRoom(rooms[roomIndex + 1:], room):
                return True
        return False

    """
    check if any of the given list of rooms overlap with the given room
    rooms: [(x, y), width, height] a list of rooms info which contains
            the position of the room in tuple style and width and height of
            this room
    otherRoom: [(x, y), width, height], one single room info that contains
            the position of the room in tuple style and width and height of
            this room
    """
    def checkRoomsContainRoom(self, rooms, otherRoom):
        for room in rooms:
            if self.checkRoomsOverlap(room, otherRoom) or self.checkRoomsOverlap(otherRoom, room):
                return True
        return False

    """
    check if the given two rooms overlap
    room1: [(x, y), width, height], one single room info that contains
            the position of the room in tuple style and width and height of
            this room
    room2: [(x, y), width, height], one single room info that contains
            the position of the room in tuple style and width and height of
            this room
    """
    def checkRoomsOverlap(self, room1, room2):
        posn = room2[0]
        upleft = room1[0]
        upright = (room1[0][0] + room1[1], room1[0][1])
        downleft = (room1[0][0], room1[0][1] + room1[2])
        downright = (room1[0][0] + room1[1], room1[0][1] + room1[2])

        checkUpLeft =  upleft[0] in range(posn[0] - 1, posn[0] + room2[1] + 1)
        checkUpLeft = checkUpLeft and upleft[1] in range(posn[1] - 1,posn[1]+room2[2] + 1)

        checkUpRight =  upright[0] in range(posn[0] - 1, posn[0] + room2[1] + 1)
        checkUpRight = checkUpRight and upright[1] in range(posn[1] - 1,posn[1]+room2[2] + 1)

        checkDownLeft = downleft[0] in range(posn[0] - 1, posn[0] + room2[1] + 1)
        checkDownLeft= checkDownLeft and downleft[1] in range(posn[1] - 1,posn[1]+room2[2] + 1)

        checkDownRight = downright[0] in range(posn[0] - 1, posn[0] + room2[1] + 1)
        checkDownRight = checkDownRight and downright[1] in range(posn[1] - 1,posn[1]+room2[2] + 1)

        checkUpLeftDownLeft = upleft[1] in range(posn[1] - 1,posn[1]+room2[2] + 1 - room1[2])
        checkUpLeftDownLeft = checkUpLeftDownLeft and downleft[0] < posn[0] and downright[0] > posn[0] + room2[1]

        return  checkUpLeft or checkUpRight or checkDownLeft or checkDownRight or checkUpLeftDownLeft

    """
    offset and sort the list. Making all the rooms order from the upper
    left to the buttom right.
    list:  a list of list in the form of:
    [[(x0, y0),x, y], [(x0, y0),x, y] ...]
    (x0, y0) is a tuple showing the upperleft posn of the room
    x is the width of the room
    y is the height of the room
    """
    def sortRoom(self, list):
        list.sort(key= lambda x: (x[0][0] - 0)**2 + (x[0][1] - 0)**2)
        return list

#----------------------Part 3 Generate Connect graph ---------------------------
    """
    turning the given list of rooms info into a connected simplices graph using
    delaunay triangulation

    listRoomInfo: [[(x0, y0),x, y], [(x0, y0),x, y] ...]
                (x0, y0) is a tuple showing the upperleft posn of the room
                x is the width of the room
                y is the height of the room
    return [[[x, y],
            [x1, y1],
            [x2, y2]] ...] a 3d array that each array inside the array has
            three numpy array which tells you which three points is conncted
            a dictionary {posn : False}, which will be used in transforming into
            minimum spanning tree
            a dictionary {posn : (x, y)}, which x will be the width and y
            will be the height
    """
    def delaunay(self, listRoomInfo):
        mid_points = []
        dict = {}
        dictInfo = {}
        for info in listRoomInfo:
            posn = info[0]
            width = info[1]
            height = info[2]
            midpoint = [posn[0] + (width - 1)/2, posn[1] + (height - 1)/2]
            dict[tuple(midpoint)] = False
            dictInfo[tuple(midpoint)] = info
            mid_points += [midpoint]
        tri_points = np.array(copy.deepcopy(mid_points))
        tri_option = Delaunay(tri_points, qhull_options="QJ Pp")
        return (tri_points[tri_option.simplices], dict, dictInfo)

#-----------------------Part4 Reduce number of connections in the graph---------
    """
    generate the minimum spanning tree of the given connected delaunay triangulation
    graph using Kruskal's algorithm
    tri: [[[x, y],
            [x1, y1],
            [x2, y2]] ...] a 3d array that each array inside the array has
            three numpy array which tells you which three points is conncted
            a dictionary {posn : False}, which will be used in transforming into
            minimum spanning tree
            a dictionary {posn : (x, y)}, which x will be the width and y
            will be the height
    """
    def minimumSpanningTree(self, tri):
        result = []
        #first: we will turn the 3d array list into an 2d array list which
        #will include all edges
        for triangle in tri[0]:
            point1 = tuple(triangle[0])
            point2 = tuple(triangle[1])
            point3 = tuple(triangle[2])
            pair1 = [point1, point2]
            pair2 = [point2, point3]
            pair3 = [point1, point3]
            pair1.sort(key= lambda x: (x[0] - 0)**2 + (x[1] - 0)**2)
            pair2.sort(key= lambda x: (x[0] - 0)**2 + (x[1] - 0)**2)
            pair3.sort(key= lambda x: (x[0] - 0)**2 + (x[1] - 0)**2)
            result += [tuple(pair1)]
            result += [tuple(pair2)]
            result += [tuple(pair3)]
        # remove the duplicated edges and sort the edges according to the
        # distance between its nodes in asecending order
        result = list(set(result))
        result.sort(key= lambda x: (x[0][0] - x[1][0])**2 + (x[0][1] - x[1][1])**2)

        # From least weighted edge, we add to our map, everytime when we
        # add the edge, we check if there is a cycle, if cycle exist we remove
        #that edge
        tree_map = []
        dict = tri[1]
        for i in range(0, len(result)):
            tree_map += [result[i]]
            if self.checkCycle(tree_map, dict):
                del tree_map[len(tree_map) - 1]
        return (tree_map, tri[2])

    """
    check if there's a cycle in the given graph using breadth first search
    dict: a dictionary which its key will be the position and value will be
    boolean indicating whether it has been visited
    """
    def checkCycle(self, tree_map, dict):
        dict = copy.deepcopy(dict)
        for pair in tree_map:
            point1 = pair[0]
            point2 = pair[1]
            if dict[point2]:
                return True
                break
            dict[point2] = True
        return False

#-----------------------Part5 Generate Hallways between rooms -------------------
    """
    Generate hallways for the monimum spanning tree. for each pair in the tree
    map, determine which kind of hallway will be used to connect and return a list
    of hallways and door posns.
    tree: a minimumSpanningTree cotanning connection information
    return type: (result, doors)
                 result: list of hallways in Hallway class
                 doors: list of position of doors in tuple form
    """
    def generateHallways(self, tree):
        midpoints = tree[1]
        tree_map = tree[0]
        result = []
        doors = []
        for pair in tree_map:
            point1 = pair[0]
            point2 = pair[1]
            hallwayInfo = self.generateSingleHallway(midpoints[point1], midpoints[point2], result)
            hallway = Hallway(hallwayInfo[0], hallwayInfo[1], hallwayInfo[2])
            result += [hallway]
            doors += [hallwayInfo[1]]
            doors += [hallwayInfo[2]]
        return (result, doors)

    """
    Generate a single hallway. First decide whether a waypoint(corner) is needed,
    if not, only generate a horizontal or vertical hallway. If a waypoint is needed,
    call a halper to find the waypoint and generate the hallway. While generating,
    check if the newly generated hallway overlaps with exsisting hallways or rooms.
    If, ther is any overlapping, repeate the process to find a proper hallway.
    info1: the midpoint of a room in tuple form
    info2: the midpoint of another room in tuple form
    result: a list of hallways in Hallway class, representing all the hallways
    that have been added to the level map.
    return type: [waypoint, door1, door2]
    waypoint: position of the corner in tuple form
    door1: a door position, also the starting point of a hallway, in tuple form
    door2: the other door position, also the ending point of a hallway, in tuple form
    """
    def generateSingleHallway(self, info1, info2, result):
        point1 = info1[0]
        point2 = info2[0]
        width1 = info1[1]
        width2 = info2[1]
        height1 = info1[2]
        height2 = info2[2]
        door1 = []
        door2 = []
        waypoints = []
        vertical = self.returnVerticalAlignment(point1, point2, width1, width2)
        horizontal = self.returnHorizontalAlignment(point1, point2, height1, height2)
        if len(vertical) > 0:
            if point1[1] > point2[1]:
                door1 = (vertical[0], point1[1])
                door2 = (vertical[0], point2[1] + height2  - 1)
            else:
                door1 = (vertical[0], point1[1] +  height1 - 1)
                door2 = (vertical[0], point2[1])
        elif len(horizontal) > 0:
            if point1[0] > point2[0]:
                door1 = (point1[0], horizontal[0])
                door2 = (point2[0] + width2 - 1, horizontal[0])
            else:
                door1 = (point1[0] + width1 - 1, horizontal[0])
                door2 = (point2[0], horizontal[0])
        else:
            listWayPoints = self.generateAllPossibleWayPoints(point1, point2, width1, width2, height1, height2)
            for waypoint in listWayPoints:
                waypoints = [waypoint]
                door1 = self.returnDirectedDoor(info1, waypoint)
                door2 = self.returnDirectedDoor(info2, waypoint)
                hallway = Hallway([waypoint], door1, door2)
                if not hallway.checkHallwaysContainHallway(result):
                    if not self.checkBoundaryPoint(info1, door1) and not self.checkBoundaryPoint(info2, door2):
                        return [waypoints, door1, door2]
        return [waypoints, door1, door2]

    """
    check if the given posn in on the boundary of the given room. This case will
    cause unusable hallways.
    roomInfo: [(x0, y0),x, y]
        (x0, y0) is a tuple showing the upperleft posn of the room
        x is the width of the room
        y is the height of the room
    posn: tuple of position we hope to check
    """
    def checkBoundaryPoint(self, roomInfo, posn):
        x = roomInfo[0][0]
        y = roomInfo[0][1]
        upperLeft = (x, y)
        width  = roomInfo[1]
        height = roomInfo[2]
        upperRight = (x + width - 1, y)
        downRight = (x + width - 1, y + height - 1)
        downLeft = (x, y + height - 1)
        return posn == upperLeft or posn == upperRight or posn == downRight or posn == downLeft

    """
    Return the door position in tuple. Check the location relationship between
    given point and room, decide where should be the door.
    roomInfo: [(x0, y0),x, y]
                (x0, y0) is a tuple showing the upperleft posn of the room
                x is the width of the room
                y is the height of the room
    posn: tuple of position we hope to connect to the given room
    """
    def returnDirectedDoor(self, roomInfo, posn):
        origin = roomInfo[0]
        width = roomInfo[1]
        height = roomInfo[2]
        minX = origin[0]
        minY = origin[1]
        maxX = minX + width - 1
        maxY = minY + height - 1
        if posn[0] > maxX and minY <= posn[1] <= maxY:
            return(maxX, posn[1])
        elif posn[0] < minX and minY <= posn[1] <= maxY:
            return(minX, posn[1])
        elif posn[1] > maxY and minX <= posn[0] <= maxX:
            return(posn[0], maxY)
        elif posn[1] < minY and minX <= posn[0] <= maxX:
            return(posn[0], minY)

    """
    Generates all possiable way points according to the relationship between two
    given rooms. Return a list of way point in tuple form.
    point1: upleft position of room1 in tuple form
    point2: upleft position of room2 in tuple form
    width1: int, width of room1
    width2: int, width of room2
    height1: int, height of room1
    height2: int, height of room2
    """
    def generateAllPossibleWayPoints(self, point1, point2, width1, width2, height1, height2):
        minX = min(point1[0], point2[0])
        minY = min(point1[1], point2[1])
        maxX = max(point1[0], point2[0])
        maxY = max(point1[1], point2[1])
        if (minX, minY) == point1:
            maxX = maxX + width2 - 1
            maxY = maxY + height2 - 1
        elif (minX, minY) == point2:
            maxX = maxX + width1 - 1
            maxY = maxY + height1 - 1
        elif (minX, minY) != point1 or (minX, minY) != point2:
            if point1[0] > point2[0]:
                maxX = maxX + width1 - 1
                maxY = maxY + height2 - 1
            else:
                maxX = maxX + width2 - 1
                maxY = maxY + height1 - 1
        result = []
        for y in range(minY, maxY):
            for x in range(minX, maxX):
                result += [(x, y)]

        room1Tiles = self.generateNoneWallTiles((point1[0] - 1, point1[1] - 1), width1 + 2, height1 + 2)
        room2Tiles = self.generateNoneWallTiles((point2[0] - 1, point2[1] - 1), width2 + 2, height2 + 2)
        result = list(set(result) - set(room1Tiles))
        result = list(set(result) - set(room2Tiles))
        waypoints = []
        alignment = []
        for point in result:
            v1 = self.returnVerticalAlignment(point1, point, width1, 3)
            v2 = self.returnVerticalAlignment(point2, point, width1, 3)
            h1 = self.returnHorizontalAlignment(point1, point, height1, 3)
            h2 = self.returnHorizontalAlignment(point2, point, height2, 3)
            if (len(v1) > 0 or len(v2) > 0) and (len(h1) > 0 or len(h2) > 0):
                waypoints += [point]
        return waypoints

    """
    Find the intersaction of two rooms in vertical direction.
    point1: upleft position of room1 in tuple form
    point2: upleft position of room2 in tuple form
    width1: int, width of room1
    width2: int, width of room2
    """
    def returnVerticalAlignment(self,point1, point2, width1, width2):
        x = range(point1[0] + 1,point1[0] + width1 - 1)
        y = range(point2[0] + 1,point2[0] + width2 - 1)
        xs = list(set(x).intersection(y))
        return xs

    """
    Find the intersaction of two rooms in horizontal direction.
    point1: upleft position of room1 in tuple form
    point2: upleft position of room2 in tuple form
    height1: int, height of room1
    height2: int, height of room2
    """
    def returnHorizontalAlignment(self, point1, point2, height1, height2):
        x = range(point1[1] + 1, point1[1] + height1 - 1)
        y = range(point2[1] + 1,point2[1] + height2 - 1)
        xs = list(set(x).intersection(y))
        return xs


#------------------------Final Part, Generate Level and Rooms-------------------
    """
    Run the procedural generation and return the SnarlLevel
    """
    def generateLevel(self):
        listinfo = self.generateRoomsInfo()
        seperated = self.seperationMove(listinfo)
        level = None
        if self.numRooms >= 4:
            delaunay = self.delaunay(seperated)
            tree = self.minimumSpanningTree(delaunay)
            try:
                hallways = self.generateHallways(tree)
                hallwayList = hallways[0]
                doors = hallways[1]
                roomList = self.generateRooms(seperated, doors)
                level = SnarlLevel(roomList, hallwayList)
                if self.render:
                    print(level.draw())
                if self.json:
                    print(js.dumps(level.returnJSON()))
            except Exception:
                self.generateLevel()
        elif 1 < self.numRooms <= 3:
            try:
                level = self.generateLessThanFourRoomOnly(seperated)
                if self.render:
                    print(level.draw())
                if self.json:
                    print(js.dumps(level.returnJSON()))
            except Exception:
                self.generateLevel()
        else:
            level = self.generateOneRoomOnly(seperated)
            if self.render:
                print(level.draw())
            if self.json:
                print(js.dumps(level.returnJSON()))
        return level

    """
    Handle the case of generating 2 and 3 rooms. Place the key and exit randomly
    in the rooms and generate hallways to connect them. Since these case cannot
    be rendered as a minimum spanning tree, this function is necessary to cover them.
    seperated: [[(x0, y0),x, y], [(x0, y0),x, y] ...]
                (x0, y0) is a tuple showing the upperleft posn of the room
                x is the width of the room
                y is the height of the room
    This is a list of seperated room information, no overlapping exsist
    """
    def generateLessThanFourRoomOnly(self, seperated):
        index = random.sample(range(0, len(seperated)), 2)
        key = index[0]
        exit = index[1]
        rooms = []
        doors = []
        hallways = []
        for i in range(0, len(seperated) - 1):
            hallwayInfo = self.generateSingleHallway(seperated[i], seperated[i + 1], hallways)
            hallway = Hallway(hallwayInfo[0], hallwayInfo[1], hallwayInfo[2])
            hallways += [hallway]
            doors += [hallwayInfo[1]]
            doors += [hallwayInfo[2]]

        for i in range(0, len(seperated)):
            info = seperated[i]
            roomPosn = info[0]
            sizeX = info[1]
            sizeY = info[2]
            tiles = self.generateNoneWallTiles(roomPosn, sizeX, sizeY)
            index = random.sample(range(0, len(tiles)), 2)
            objects = {}
            doorsPosns = []
            if key == i:
                objects["key"] = tiles[index[0]]
            if exit == i:
                objects["exit"] = tiles[index[1]]
            if objects == {}:
                objects = None

            for door in doors:
                if self.checkPosnWithinRoom(door, roomPosn, sizeX, sizeY):
                    doorsPosns += [door]
            room = Room(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects)
            rooms += [room]
        return SnarlLevel(rooms, hallways)

    """
    Handle the case of generating 1 room. Place the key and exit randomly
    in the room and generate a fake door. Since these case cannot be rendered
    as a minimum spanning tree, this function is necessary to cover them.
    seperated: [[(x0, y0),x, y]]
                (x0, y0) is a tuple showing the upperleft posn of the room
                x is the width of the room
                y is the height of the room
    """
    def generateOneRoomOnly(self, seperated):
        info = seperated[0]
        roomPosn = info[0]
        sizeX = info[1]
        sizeY = info[2]
        tiles = self.generateNoneWallTiles(roomPosn, sizeX, sizeY)
        index = random.sample(range(0, len(tiles)), 2)
        objects = {}
        objects["key"] = tiles[index[0]]
        objects["exit"] = tiles[index[1]]
        room = Room(roomPosn, sizeX, sizeY, tiles, [(roomPosn[0] + math.floor(sizeX / 2), roomPosn[1])], objects)
        level = SnarlLevel([room], [])
        return level

    """
    Turn the list of Room info into a list of Room object
    listRoomInfo: a list of room information that contains info including the
    position of the room, the width and height of this room, for example
    [(2, 3), 5, 4], (2, 3) will be the position and 5 is the width and 4 is the
    height
    """
    def generateRooms(self, listRoomInfo, doors):
        result = []
        key = 0
        exit = 0
        if len(listRoomInfo) != 1:
            index = random.sample(range(0, len(listRoomInfo)), 2)
            key = index[0]
            exit = index[1]
        for i in range(0, len(listRoomInfo)):
            info = listRoomInfo[i]
            roomPosn = info[0]
            sizeX = info[1]
            sizeY = info[2]
            tiles = self.generateNoneWallTiles(roomPosn, sizeX, sizeY)
            index = random.sample(range(0, len(tiles)), 2)
            doorsPosns = []
            objects = {}
            if key == i:
                objects["key"] = tiles[index[0]]
            if exit == i:
                objects["exit"] = tiles[index[1]]
            if objects == {}:
                objects = None

            for door in doors:
                if self.checkPosnWithinRoom(door, roomPosn, sizeX, sizeY):
                    doorsPosns += [door]
            room = Room(roomPosn, sizeX, sizeY, tiles, doorsPosns, objects)
            result += [room]
        return result

    """
    generate a list of non wall tiles based on the given position of the room
    and the width and height of the room.

    posn: position of the room in tuple style
    width: integer, the width of the room
    height: integer, the height of the room

    return the none wall tiles that within the room that has walls surround
    at the perimeter of the room
    """
    def generateNoneWallTiles(self, posn, width, height):
        result = []
        for y in range(posn[1] + 1, posn[1] + height - 1):
            for x in range(posn[0] + 1, posn[0] + width - 1):
                result += [(x, y)]
        return result

    """
    check if the given posn is within the given room position
    posn: a posn in tuple(int, int) format
    origin: upper left position point of this room
    sizeX: int indicating horizontal length of this room
    sizeY: int indicating vertical length of this room
    """
    def checkPosnWithinRoom(self, posn, origin, sizeX, sizeY):
        inputPointX = posn[0]
        inputPointY = posn[1]
        originX = origin[0]
        originY = origin[1]
        withinX = inputPointX in range(originX, originX + sizeX)
        withinY = inputPointY in range(originY, originY + sizeY)
        return withinX and withinY

if __name__ == "__main__":
    numRooms = 5
    min_size = [4, 4]
    max_size = [15, 15]
    json = False
    render = False

    for index in range (1, len(sys.argv)):
        argv = sys.argv[index]
        if argv in "--rooms":
            numRooms = int(sys.argv[index+1])
        elif argv in "--min":
            min_size = pj.parse_to_json(sys.argv[index+1])[0]
        elif argv in "--max":
            max_size = pj.parse_to_json(sys.argv[index+1])[0]
        elif argv in "--json":
            json = True
        elif argv in "--render":
            render = True

    if not json and not render:
        render = True

    min_size = [min_size[1], min_size[0]]
    max_size = [max_size[1], max_size[0]]
    generator = SnarlLevelGenerator(numRooms, min_size, max_size, json, render)
    generator.generateLevel()
