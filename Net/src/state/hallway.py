from src.state.room import Room
import copy
import math
"""
A Hallway class is composed of waypoints indicating direction of how hallway
is linked, a startPoint in tuple(int, int) format indicating the start
position of this hallway in some room, a endPoint is in tuple(int, int) format
indicating the end position of this hallway in some room
"""
class Hallway:
    def __init__(self, waypoints, startpoint, endpoint):
        '''
        Constructor arguments:
        :param  __waypoints:    list of tuple of int, all the corner position
                            of the hallway
        :param  __path:     list of tuple of int, all the positions this hallway
                        goes through
        :param  __startPoint:   tuple of int, the start point of this hallway
        :param  __endPoint:  tuple of int, the end point of this hallway
        '''
        self.__waypoints = waypoints
        # need to check if all way points can connect together and generate
        # a path between start and end point
        try:
            self.__path = Hallway.__generatePath(startpoint, endpoint, waypoints)
        except ValueError:
            raise ValueError("Waypoints cannot connect to the start end point")
        self.__startPoint = startpoint
        self.__endPoint = endpoint



    @staticmethod
    def __generatePath(startpoint, endpoint, waypoints):
        """
        Generate a path by connecting all the waypoints and start and end point
        @type   startPoint:     tuple of int
        @param  startPoint:     start the of the path
        @type     endPoint:     tuple of int
        @param    endPoint:     end position of the path
        @type    waypoints:     list of tuple of int
        @param   waypoints:     all the corners of the path
        @rtype:                 list of tuple of int
        @return:                all points in the path
        """
        result = []
        waypoints = [startpoint] + waypoints
        waypoints += [endpoint]
        result += [startpoint]
        try:
            for index in range(len(waypoints) - 1):
                startPoint = waypoints[index]
                endPoint = waypoints[index + 1]
                path = Hallway.__connectTwoPoints(startPoint, endPoint)
                if startPoint[0] > endPoint[0] or startPoint[1] > endPoint[1]:
                    list.reverse(path)
                path = path[1:len(path)]
                result += path
        except ValueError:
            raise ValueError("Invalid waypoints, cannot connect")
        return result


    @staticmethod
    def __connectTwoPoints(startpoint, endpoint):
        """
        Return a list of points that is next to each other horizontally or vertically
        which connect the given startPoint and endPoint
        @type   startPoint:     tuple of int
        @param  startPoint:     start the of the path
        @type     endPoint:     tuple of int
        @param    endPoint:     end position of the path
        @rtype:                 list of tuple of int
        @return:                all points in the path to connect given points
        """
        min_x = min(startpoint[0], endpoint[0])
        max_x = max(startpoint[0], endpoint[0])
        min_y = min(startpoint[1], endpoint[1])
        max_y = max(startpoint[1], endpoint[1])
        if startpoint[1] ==  endpoint[1]:
            return [(x, startpoint[1]) for x in range(min_x, max_x + 1)]
        elif startpoint[0] ==  endpoint[0]:
            return [(startpoint[0], y) for y in range(min_y, max_y + 1)]
        else:
            raise ValueError("Points are not vertical or horizontal. ")




    def maxXminXmaxYminY(self):
        """
        return the max X value in this hallway, which will be the x of the down right
        and max Y value in this hallway, which will be the y of the down right, same
        for min X and min Y.
        @rype:          list of tuple of int
        @return:        the boundary horizontal and vertical coorindate value
                    of this hallway
        """
        maxX = self.__path[0][0]
        minX = self.__path[0][0]
        maxY = self.__path[0][1]
        minY = self.__path[0][1]
        for tile in self.__path:
            maxX = max(maxX, tile[0])
            minX = min(minX, tile[0])
            maxY = max(maxY, tile[1])
            minY = min(minY, tile[1])
        return [maxX, minX, maxY, minY]



    def returnJSON(self):
        """
        return the information of this hallway in standard JSON.
        @rtype:     JSON
        @return:    information of this hallway
        """
        result = {"type": "hallway","from": None,"to": None, "waypoints":[]}
        result["from"] = self.__startPoint
        result["to"] = self.__endPoint
        result["waypoints"] = self.__waypoints
        return result





    def renderHallway(self, map, minX, minY):
        """
        render the hallway by replacing all the map's posns where hallway tiles
        located with "+". Render the hallway on given map.
        @type   map:    2D list
        @param  map:    all map informations
        @type  minX:    int
        @param minX:    the most top left coordinate X of the map
        @type  minY:    int
        @param minY:    the most top left coordinate Y of the map
        @rtype:         2D list
        @return:        a new map with all hallway positions replaced with "+"
        """
        result = map
        plusX = 0 - minX
        plusY = 0 - minY
        path = self.__path
        for tile in path[1:len(path) - 1]:
            result[tile[1] + plusY][tile[0] + plusX] = "+"
        return result


    def checkHallwaysContainHallway(self,hallways):
        """
        checks if otherhallway overlaps any hallway in the hallway list
        @type   hallways:   list of Hallway
        @param  hallways:   other hallways hope to check for overlapping
        @rtype:             boolean
        @return:            whether the overlapping exsist
        """
        if(hallways == None):
            return False
        else:
            for hallway in hallways:
                if self.checkHallwayOverlapHallway(hallway):
                    return True
        return False



    def checkHallwayOverlapHallway(self, otherHallway):
        """
        check if this hallway overlaps a given hallway by checking if any tiles
        in the hallway path overlaps with the input hallway's path tiles
        @type   otherHallway:   Hallway
        @param  otherHallway:   the other hallway hope to check for overlapping
        @rtype:                 boolean
        @return:                whether the overlapping exsist
        """
        twoHallwayPath = self.__path + otherHallway.__path
        setTwoHallwayPath = set(twoHallwayPath)
        return len(twoHallwayPath) != len(setTwoHallwayPath)



    def checkHallwayOverlapRoom(self, room):
        """
        check if this hallway overlaps the given room by checking if any tiles
        in the hallway path overlaps with the input room's tiles
        @type   room:   Room
        @param  room:   the room hope to check for overlapping
        @rtype:         boolean
        @return:        whether there is overlapping
        """
        path = self.__path[1:len(self.__path) - 1]
        return room.checkHallwayRoomOverlap(path)




    def returnReachable(self, point):
        """
        check if the point is reachable in the hallway, if so return its start
        and end point. If not, return None.
        @type   point:  tuple of int (x,y)
        @param  point:  a position in the map
        @rtype:         list of tuple of int
        @return:        [start point, end point]
        """
        if self.checkTraversable(point):
            return [self.__startPoint, self.__endPoint];
        return None



    def checkTraversable(self, point):
        """
        check if the point is reachable in the hallway
        @type   point:  tuple of int (x,y)
        @param  point:  a position in the map
        @rtype:         boolean
        @return:        whether given point is reachable by this hallway
        """
        return point in self.__path


    def generteHallway(self):
        """
        return the copy of all tiles that makes up this hallway
        @rtype:     list of tuple of int
        @return:    the path of this hallway
        """
        return copy.deepcopy(self.__path)
