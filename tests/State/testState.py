from gamestate import GameState
from gamestate import Player
from gamestate import Adversary
from level import SnarlLevel
from ruleChecker import RuleChecker
from gameManager import GameManager
import testLevel as tl
import sys
import parse_json as pj
import json

"""
return final output by moving the player and return the interaction of the player
and potential objects in the given destination point
stateJson: a jason list that contains information about level, players, adversaries,
the name of the player to be moved and the destination position
"""
def finalOutput(stateJson):
    state = stateJson[0]
    level = state["level"]
    state = handleState(state)
    name = stateJson[1]
    dest = stateJson[2]
    point = (dest[1], dest[0])
    manager = GameManager(10)
    manager = manager.intermediate([],[], state)
    result = []
    try:
        move = manager.move_player(name, point)
        if move == "please re-enter movement":
            result += ["Failure", "The destination position"]
            result += [dest]
            result += [" is invalid."]
        else:
            result = handleSucess(manager, name, point, state, level)
    except ValueError:
        result += ["Failure", "Player"]
        result += [name]
        result += [" is not a part of the game."]
    return result

"""
return the output if the movement is Successful
manager: GameManager
name: string, the name of the player to be moved
point: tuple style, representing the point to be moved to
state: the GameState
level: the level json value
"""
def handleSucess(manager, name, point, state, level):
    result = []
    manager.respond_to_interaction(name, point)
    checker = RuleChecker(state, None)
    if checker.returnInteraction(point) == "ejected":
        result+=["Success", "Player "]
        result+=[name]
        result+=[" was ejected."]
        result+=[stateBackToJason(state, level)]
    elif checker.returnInteraction(point) == "exited":
        result+=["Success", "Player "]
        result+=[name]
        result+=[" exited."]
        result+=[stateBackToJason(state, level)]
    else:
        result+=["Success"]
        result+=[stateBackToJason(state, level)]
    return result

"""
turn the given game state and level json value into json format
state: GameState
level: json value represent the map
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
turn the given state json value to a GameState and place the objects into the map
state: Json Value represent the state
"""
def handleState(state):
    level = state["level"]
    players = state["players"]
    adversaries = state["adversaries"]
    exitState = state["exit-locked"]
    objects = level['objects']

    level = tl.handleLevel([level])
    players = handlePlayers(players)
    adversaries = handleAdversaries(adversaries)
    state = GameState(level, 1, 1).intermediate(players, adversaries, exitState)
    for object in objects:
        type = object['type']
        posn = object['position']
        posn = (posn[1], posn[0])
        state.placeObject(type, posn)
    return state

"""
turn the player json value to a dictionary with key to be the position of the player
and value to be the player
players: the player json list
"""
def handlePlayers(players):
    result = {}
    for player in players:
        name = player["name"]
        posn = player["position"]
        posn = (posn[1], posn[0])
        player = Player(name, posn)
        result[posn] = player
    return result

"""
turn the adversary json value to a dictionary with key to be the position of the
adversary and value to be the adversary
adversary: the adversary json list
"""
def handleAdversaries(adversaries):
    result = {}
    for adversary in adversaries:
        posn = adversary["position"]
        name = adversary["name"]
        type = adversary["type"]
        posn = (posn[1], posn[0])
        adversary = Adversary(posn, name, type)
        result[posn] = adversary
    return result


if __name__ == '__main__':
    userInput = ""
    for line in sys.stdin:
        userInput = userInput + line
    stateJsonList = pj.parse_to_json(userInput)
    for state in stateJsonList:
        result = finalOutput(state)
        print(json.dumps(result))
