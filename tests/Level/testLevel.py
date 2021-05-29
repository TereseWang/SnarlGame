#!/usr/bin/python3
from room import Room
from hallway import Hallway
from level import SnarlLevel
import parse_json as pj
import json
import sys

"""
return final output
levelJson: a jason list that contains information about level including rooms
hallways and objects
return the final output that combine the result of checkTraversable, whether
the given point is on an object tile, and the type of the segment in the level
that point is located, and any rooms that is reachable to the point
"""
def finalOutput(levelJson):
    level = handleLevel(levelJson)
    result = {}
    point = levelJson[1]
    newPoint = (point[1], point[0])
    result["traversable"] = level.checkTraversable(newPoint)
    result["object"] = handleObject(levelJson, point)
    result["type"] = level.returnType(newPoint)
    reachable = level.returnReachable(newPoint, result["type"])
    newReachable = []
    for point in reachable:
        point1 = (point[1], point[0])
        newReachable += [point1]
    result["reachable"] = newReachable
    return result

"""
implementing the given json value to a Level Class
levelJson: a jason list that contains information about level including rooms
hallways and objects
"""
def handleLevel(levelJson):
    rooms = levelJson[0]["rooms"]
    hallways = levelJson[0]["hallways"]
    objects = levelJson[0]["objects"]
    roomList = []
    hallwayList = []
    for room in rooms:
        roomList+=[handleRoom(room)]
    for hallway in hallways:
        hallwayList+=[handleHallway(hallway)]
    level = SnarlLevel(roomList, hallwayList)
    return level

"""
if the given point is inside the level and also it is on object tile, return
the object type
levelJson: a jason list that contains information about level including rooms
hallways and objects
point: a point represent the position we are checking in tuple(x, y) style
"""
def handleObject(levelJson, point):
    objects = levelJson[0]["objects"]
    result = None
    for object in objects:
        if point == object["position"]:
            result = object["type"]
            break
    return result

"""
implementing the given json value to a Room class
roomJson: a jason list that contains information about a room and a posn to
return the implemented Room
"""
def handleRoom(roomJson):
    layout = roomJson["layout"]
    origin = roomJson["origin"]
    boundsRow = roomJson["bounds"]["rows"]
    boundsCol = roomJson["bounds"]["columns"]

    """need to switch row and col to (x, y) format"""
    newOrigin = (origin[1], origin[0])

    """split the given layout into a 2D array list contains positions of
    doors, noneWallTiles, and objects"""
    doorNonWallObjectTiles = returnNonWallAndDoorTiles(layout,origin[0], origin[1])
    doorTiles = doorNonWallObjectTiles[1]
    noneWallTiles = doorNonWallObjectTiles[0]
    """build this Room and call the returnTraversablePoint function in room"""
    room = Room(newOrigin, boundsCol, boundsRow, noneWallTiles, doorTiles, None)
    return room


"""
implementing the given json value to a Hallway Class
hallwayJson: a jason list that contains information about hallway including
start end point and also waypoints
"""
def handleHallway(hallwayJson):
    waypoints = hallwayJson["waypoints"]
    startPoint = hallwayJson["from"]
    endPoint = hallwayJson["to"]
    newWayPoints = []
    for waypoint in waypoints:
        newWayPoints += [(waypoint[1], waypoint[0])]
    newStartPoint = (startPoint[1], startPoint[0])
    newEndPoint = (endPoint[1], endPoint[0])
    newHallway = Hallway(newWayPoints, newStartPoint, newEndPoint)
    return newHallway

"""
return a list contains two list that contains information about the position
of the none wall tiles,and doors
layout: a 2D array list contains information about the room
originX: int, X value of the top left coordinate
originY: int, Y value of the top left coordinate
"""
def returnNonWallAndDoorTiles(layout, originX, originY):
    noneWallTiles = []
    doorTiles = []
    for row in range(len(layout)):
        for col  in range(len(layout[row])):
            """if it contains a 1 or 2, it will be non wall tiles"""
            if layout[row][col] == 1 or layout[row][col] == 2:
                noneWallTiles += [(col + originY, row + originX)]
            """if it contains 2, then it will be door tiles"""
            if layout[row][col] == 2:
                doorTiles += [(col + originY, row + originX)]
    return [noneWallTiles, doorTiles]


if __name__ == '__main__':
    userInput = ""
    for line in sys.stdin:
        userInput = userInput + line
    levelJsonList = pj.parse_to_json(userInput)
    for level in levelJsonList:
        result = finalOutput(level)
        print(json.dumps(result))
