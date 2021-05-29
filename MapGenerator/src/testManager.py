#!/usr/bin/python3
import json
import sys
import src.parse_json as pj
import src.testLevel as tl
from src.manager.gameManager import GameManager

"""
@type manager: Json Value
@param manager: Json value representing the game manager
@rtype: Json Value
@return: the final output of the manager after running a series of moves
"""
def finalOutput(manager):
    namelist = manager[0]
    level = manager[1]
    levelClass = tl.handleLevel([level])
    numturns = manager[2]
    pointList = manager[3]
    playerList = pointList[0:len(namelist)]
    adversaryList = pointList[len(namelist):]
    playerList = handlePosnList(playerList)
    adversaryList = handlePosnList(adversaryList)
    movement = manager[4]
    manager = GameManager(namelist, levelClass, numturns, adversaryList, playerList)
    objects = level['objects']
    manager.place_object(objects)
    state = manager.returnGameState()
    initial = []
    for name in namelist:
        currentPosn = state.getPlayer(name).playerPosition()
        initial += [playerUpdate(name, state, currentPosn)]

    result = handleTurn(numturns, namelist, manager, movement)

    state = manager.returnGameState()
    for name in namelist:
        if state.getPlayer(name) != None:
            currentPosn = state.getPlayer(name).playerPosition()
            result += [playerUpdate(name, state, currentPosn)]

    del result[0]
    result = initial + result
    del result[len(result) - 1]
    finalJason = handleFinal(manager, result, level)
    return finalJason

"""
makes moves for each turn
@type numturns: Number
@param numturns: the maximum number of turns available to play
@type namelist: List of Strings
@param namelist: List of names representing list of players
@type manager: GameManager Class
@param manager: the manager class to call manager functions
@type movement: List of dictionary
@param movement: a list of movement in jason value that need to take action
"""
def handleTurn(numturns, namelist, manager, movement):
    result = []
    for turn in range(0, returnShortestList(movement)):
        if turn > numturns - 1:
            return result
            break
        move = movePlayers(namelist, manager, turn, movement)
        if manager.checkLevelEnd():
            result += move
            break
        if move == "Invalid Behavior" or move == "outbound":
            break
        else:
            result += move
    return result

"""
@type movementList: Json Value
@param movementList: a list of movements in jason format
@rtype: Number
@return: shortest list's length of the given movement list
"""
def returnShortestList(movementList):
    return min([len(ls) for ls in movementList])

"""
handle the result of running all the moves
@type manager: GameManager
@param manager: Manager Class
@type result: List of Tuples
@param result: list representing a series of result and movement update
@type level: Jason Value
@param level: the level of the game
@rtype: Json Value
@return: if the trace is a single tuple add it to the result list,
if it is an update do the same thing, if it is a series of actions for
same player, split them and do action for each
"""
def handleFinal(manager, result, level):
    state = manager.returnGameState()
    stateJason = stateBackToJason(state, level)
    traces = []
    for trace in result:
        if type(trace) == tuple:
            trace = handleMove(trace)
            traces+= [trace]
        elif type(trace) == list:
            if type(trace[0]) == tuple:
                for t in trace:
                    t = handleMove(t)
                    traces += [t]
            else:
                traces += [trace]
        else:
            traces+= [trace]
    return [stateJason] + [traces]

"""
@type move: [name, move performed, result]
@param move: turn the given move result into jason format
@rtype: Json Value
@return: the json format of the given movement
"""
def handleMove(move):
    name = move[0]
    actorMove = move[3]
    result = move[2]
    return [name, actorMove, result]

"""
turn the given game state and level json value into json format
@type state: GameState Class
@param state: the game state
@type level: Json Value
@param level: Value represent the map
@rtype: Json Value
@return: turn the game state into desired json value
"""
def stateBackToJason(state, level):
    output = {
    "type": "state",
    "level": level,
    "players": [],
    "adversaries": [],
    "exit-locked": state.getUnlock()
    }
    output["players"] = state.returnJsonPlayers()
    output["adversaries"] = state.returnJsonAdversaries()
    return output

"""
move the players for one single turn
@type namelist: List of String
@param namelist: a list of names representing the players
@type manager: GameManager Class
@param manager: the game manager to call the functions
@type turn: Number
@param turn: the current turn to perform the action
@type movement: List
@type movement: the list of movements for each different player
"""
def movePlayers(namelist, manager, turn, movement):
    result = []
    gamestate = manager.returnGameState()
    for index in range(0, gamestate.getPlayerLen()):
        name = namelist[index]
        player = gamestate.getPlayer(name)
        if player != None:
            currentPosn = player.playerPosition()
        else:
            currentPosn = None
        result += [playerUpdate(name, gamestate, currentPosn)]
        movementList = movement[index]
        next = None

        if turn <= len(movementList) - 1:
            next = findNextValidPosn(manager, name, movementList, turn)
        else:
            return "outbound"
            break

        if next != "Invalid Behavior":
            result+=[next]
            dest = next[len(next) - 1]
            if dest != None and len(dest) == 2:
                dest = [dest[0], dest[1]]
            elif dest!= None and len(dest) != 2:
                dest = dest[len(dest) - 1]
                dest = [dest[0], dest[1]]
            result+=[playerUpdate(name, gamestate, dest)]
            if manager.checkLevelEnd():
                break
        else:
            return "Invalid Behavior"
            break
    return result

"""
find the  next valid posn, if the movement is invalid, iterate to next movement
until find a valid movement, after moves, return response
@type manager: GameManager Class
@param manager: the game manager to perform functions
@type name: String
@param name: the name of the player that will be moved
@type movementList: List of movements
@param movementlist: the list of movements to move
@type turn: Number
@param turn: the current turn of the game
@rtype: Tuple
@return: (Name: String, Result: result of calling move_player, Respond: movement
            interaction, Movement, turn: current turn, currentPosn: the current position)
"""
def findNextValidPosn(manager, name, movementList, turn):
    if turn <= len(movementList) - 1:
        currentMovement = movementList[turn]
        dest = currentMovement["to"]
        result = None
        respond = None
        currentPosn = None
        if dest == None:
            result = manager.move_player(name, None)
            respond = "OK"
        else:
            dest = (dest[1], dest[0])
            if manager.returnGameState().getPlayer(name) != None:
                result = manager.move_player(name, dest)
                respond = manager.respond_to_interaction(name, dest)

        if result == "please re-enter movement":
            gamestate = manager.returnGameState()
            player = gamestate.getPlayer(name)
            if player != None:
                currentPosn = player.playerPosition()
            current = [(name, result, "Invalid", movementList[turn], turn, currentPosn)]
            del movementList[turn]
            next = findNextValidPosn(manager, name, movementList, turn)
            return current + [next]
        else:
            gamestate = manager.returnGameState()
            player = gamestate.getPlayer(name)
            if player != None:
                currentPosn = player.playerPosition()
            return (name, result, respond, movementList[turn], turn, currentPosn)
    else:
        return("Invalid Behavior")

"""
return the update for the given player, with a layout that is 5X5 grids around
the player, actors is a list of actors except themselves around the player,
objects is a list of objects surround the player
@type name: String
@param name: the name of the player to get the update
@type state: GameState Class
@param state: the game state to call the function
@type posn: tuple of two number, (number, number)
@param posn: the current position of the player
@rtype: Dictionary
@return: a dictionary that contains information about the player
"""
def playerUpdate(name, state, posn):
    tiles = []
    objects = []
    actors = []
    if posn != None:
        posn = (posn[0], posn[1])
        tiles = state.returnPlayerTiles(name, posn)[0]
        objects = state.returnPlayerTiles(name, posn)[1]
        actors = state.returnPlayerTiles(name, posn)[2]
        posn = [posn[1], posn[0]]
    update = {
         "type": "player-update",
         "layout": tiles,
         "position": posn,
         "objects": objects,
         "actors": actors
         }
    return [name, update]

"""
handle the list of posns by reversing x and y values
@type list: a list of tuple of two numbers
@param list: list of positions to handle
@rtype: a list of tuple of two numbers
@return: the original list by reversing x and y values
"""
def handlePosnList(list):
    result = []
    for posn in list:
        position = (posn[1], posn[0])
        result += [position]
    return result

if __name__ == '__main__':
    userInput = ""
    for line in sys.stdin:
        userInput = userInput + line
    managerJsonList = pj.parse_to_json(userInput)
    for manager in managerJsonList:
        result = finalOutput(manager)
        print(json.dumps(result))
