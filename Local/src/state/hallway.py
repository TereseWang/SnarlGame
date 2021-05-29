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
        self.__waypoints = waypoints
        """need to check if all way points can connect together and generate
        a path between start and end point"""
        try:
            self.__path = Hallway.__generatePath(startpoint, endpoint, waypoints)
        except ValueError:
            raise ValueError("Waypoints cannot connect to the start end point")
        self.__startPoint = startpoint
        self.__endPoint = endpoint


    """
    check if the point is reachable in the hallway, if so return its start
    and end point
    point: a position represent in tuple(x, y) format
    """
    def returnReachable(self, point):
        if self.checkTraversable(point):
            return [self.__startPoint, self.__endPoint];
        return None

    """
    check if the point is reachable in the hallway
    point: a position represent in tuple(x, y) format
    """
    def checkTraversable(self, point):
        return point in self.__path

    """return all tiles that makes up this hallway"""
    def generteHallway(self):
        return copy.deepcopy(self.__path)

    """
    render the hallway by replacing all the map's posns where hallway tiles
    located with "+"
    map: a 2D array list of tuple coordinates
    minX: an integer indicating the most top left coordinate X of the map
    minY: an integer indicating the most top left coordinate Y of the map
    return type: 2D array list with hallway positions replaced with "+"
    """
    def renderHallway(self, map, minX, minY):
        result = map
        plusX = 0 - minX
        plusY = 0 - minY
        path = self.__path
        for tile in path[1:len(path) - 1]:
            result[tile[1] + plusY][tile[0] + plusX] = "+"
        return result

    """
    return the max X value in this room, which will be the x of the down right
    and max Y value in this room, which will be the y of the down right, same
    for min X and min Y.
    return a list of integers [maxX, minX, maxY, minY]
    """
    def maxXminXmaxYminY(self):
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

    """
    check if this hallway overlaps a given hallway by checking if any tiles
    in the hallway path overlaps with the input hallway's path tiles
    otherHallway: A Hallway class
    """
    def checkHallwayOverlapHallway(self, otherHallway):
        twoHallwayPath = self.__path + otherHallway.__path
        setTwoHallwayPath = set(twoHallwayPath)
        return len(twoHallwayPath) != len(setTwoHallwayPath)

    """
    check if this hallway overlaps the given room by checking if any tiles
    in the hallway path overlaps with the input room's tiles
    room: A Room Class
    """
    def checkHallwayOverlapRoom(self, room):
        path = self.__path[1:len(self.__path) - 1]
        return room.checkHallwayRoomOverlap(path)

    """
    checks if otherhallway overlaps any hallway in the hallway list
    hallways: List of Hallway
    otherhallway: Hallway
    """
    def checkHallwaysContainHallway(self,hallways):
        if(hallways == None):
            return False
        else:
            for hallway in hallways:
                if self.checkHallwayOverlapHallway(hallway):
                    return True
        return False
    """
    return the information of this hallway in standard JSON.
    """
    def returnJSON(self):
        result = {"type": "hallway","from": None,"to": None, "waypoints":[]}
        result["from"] = self.__startPoint
        result["to"] = self.__endPoint
        result["waypoints"] = self.__waypoints
        return result

    """
    Generate a path by connecting all the waypoints and start and end point
    startPoint: a posn in tuple(int, int) format
    endPoint: a posn in tuple(int, int) format
    waypoints: a list of posns in tuple(int, int) format, indicating waypoints
    """
    @staticmethod
    def __generatePath(startpoint, endpoint, waypoints):
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

    """
    Return a list of points that is next to each other horizontally or vertically
    which connect the given startPoint and endPoint
    startPoint: a posn in tuple(int, int) format
    endPoint: a posn in tuple(int, int) format
    """
    @staticmethod
    def __connectTwoPoints(startpoint, endpoint):
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
