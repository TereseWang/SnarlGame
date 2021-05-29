#!/usr/bin/python3
import json
import sys
import parse_json as pj
from room import Room

"""
return list of traversable points by implementing the given json value to a
Room class and call the returnTraversablePoint function in room to return
a list of points that is traversable of the given point inside the jason value
roomJson: a jason list that contains information about a room and a posn to
return its traversable points
"""
def handleRoom(roomJson):
    result = []
    layout = roomJson[0]["layout"]
    origin = roomJson[0]["origin"]
    inputPoint = roomJson[1]
    boundsRow = roomJson[0]["bounds"]["rows"]
    boundsCol = roomJson[0]["bounds"]["columns"]

    """need to switch row and col to (x, y) format"""
    newOrigin = (origin[1], origin[0])
    newInputPoint = (inputPoint[1], inputPoint[0])

    """split the given layout into a 2D array list contains positions of
    doors, noneWallTiles, and objects"""
    doorNonWallObjectTiles = returnNonWallAndDoorTiles(layout,origin[0], origin[1])
    doorTiles = doorNonWallObjectTiles[1]
    noneWallTiles = doorNonWallObjectTiles[0]
    objects = doorNonWallObjectTiles[2]
    """build this Room and call the returnTraversablePoint function in room"""
    room = Room(newOrigin, boundsCol, boundsRow, noneWallTiles, doorTiles, objects)
    return room.returnTraversablePoint(newInputPoint)

"""
change the list of traversable points into the desired json value output
roomHandleResult: a list of [int, int] points indicating a list of positions
that is traversable of some point
roomJson: a jason list that contains information about a room and a posn to
return its traversable points
"""
def finalOutput(roomHandleResult, roomJson):
    origin = roomJson[0]["origin"]
    inputPoint = roomJson[1]
    result = []
    """if point is not inside the room"""
    if roomHandleResult == None:
        result += ["Failure: Point "]
        result += [inputPoint]
        result += [" is not in room at "]
        result += [origin]
    else:
        result += ["Success: Traversable points from "]
        result += [inputPoint]
        result += [" in room at "]
        result += [origin]
        result += [" are "]
        result += [roomHandleResult]
    return result

"""
return a list contains three list that contains information about the position
of the none wall tiles, doors, and obejcts
layout: a 2D array list contains information about the room
originX: int, X value of the top left coordinate
originY: int, Y value of the top left coordinate
"""
def returnNonWallAndDoorTiles(layout, originX, originY):
    noneWallTiles = []
    doorTiles = []
    objects = None
    for row in range(len(layout)):
        for col  in range(len(layout[row])):
            """if it contains a 1 or 2, it will be non wall tiles"""
            if layout[row][col] == 1 or layout[row][col] == 2:
                noneWallTiles += [(col + originY, row + originX)]
            """if it contains 2, then it will be door tiles"""
            if layout[row][col] == 2:
                doorTiles += [(col + originY, row + originX)]
    return [noneWallTiles, doorTiles, objects]

if __name__ == '__main__':
    userInput = ""
    for line in sys.stdin:
        userInput = userInput + line
    roomsJsonList = pj.parse_to_json(userInput)
    for roomJson in roomsJsonList:
        roomHandleResult = handleRoom(roomJson)
        final_out = finalOutput(roomHandleResult, roomJson)
        print(json.dumps(final_out))
