#!/usr/bin/python3
from level import SnarlLevel
from room import Room
from hallway import Hallway
import random
import copy
import math

"""
A Player is composed of a position and we will add user name feature later,
it will also contain a boolean to check if this player had find an unlocked
exit to helps us to check if the game is over or not
"""
class  Player:
    def __init__(self, name, posn):
        self.__position = posn
        self.__name = name
        self.__exited = False

    """return the name of this player"""
    def playerName(self):
        return self.__name

    """return the position of this player"""
    def playerPosition(self):
        return copy.deepcopy(self.__position)

    """return if this player had find the unlocked exit"""
    def playerExited(self):
        return copy.copy(self.__exited)

    """update the movement"""
    def move(self, movement):
        self.__position = movement

"""
A Adversary will composed of a position in tuple format and a type indicating
the type of adversary("zoombie", "ghost") and so
"""
class  Adversary:
    def __init__(self, posn, name, type):
        self.__position = posn
        self.__type = type
        self.__name = name

    """return the name of this adversary"""
    def adversaryName(self):
        return self.__name

    """return the position of the adversary"""
    def adversaryPosns(self):
        return copy.deepcopy(self.__position)

    """return the type of this adversary"""
    def adversaryType(self):
        return self.__type

    """update the movement to adversary's position"""
    def move(self, movement):
        self.__position = movement

"""
A Game State is composed of a
map: 2D Array of tuple(int, int) including all items position in this game

"""
class GameState:
    """
    Initialize the game by inputting a map, a total player number and an
    adversary number
    level: A SnarlLevel
    playerNum: int, total number of player will play this game
    adversaryNum: int, total number of adversary in this game
    """
    def __init__(self, level, playerList, adversaryList):
        self.__map = level
        self.__players = playerList   # {posn : Player}
        self.__adversaries = adversaryList #{posn : Adversary}
        self.__unlock = False

    """
    return the players in json style
    """
    def returnJsonPlayers(self):
        result = []
        for posn, player in self.__players.items():
            playerJson = {
            "type": "player",
            "name": player.playerName(),
            "position": [posn[1], posn[0]]}
            result+=[playerJson]
        return result

    """
    return the adversary list in json style
    """
    def returnJsonAdversaries(self):
        result = []
        for posn, ad in self.__adversaries.items():
            adJson = {
            "type": ad.adversaryType(),
            "name": ad.adversaryName(),
            "position": [posn[1], posn[0]]}
            result+=[adJson]
        return result

    """
    return the tiles surround the given player with the given name and given position
    name: the name of the player in string
    posn: the position of the player in tuple format
    """
    def returnPlayerTiles(self, name, posn):
        layout = []
        actors = []
        objects = []
        for y in range(posn[1] - 2, posn[1] + 3):
            row = []
            for x in range(posn[0] - 2, posn[0] + 3):
                object = self.returnObject((x, y))
                if object == "x":
                    row+=[0]
                elif type(object) == tuple:
                    row+=[0]
                elif object == None:
                    row+=[0]
                elif object == "1":
                    row+=[1]
                elif object == "2":
                    row+=[2]
                elif object == "k":
                    objects += [{"type": "key", "position" : [y, x]}]
                    row+=[1]
                elif object == "e":
                    objects += [{"type": "exit", "position" : [y, x]}]
                    row+=[1]
                elif object == "+":
                    row+=[1]

                if self.getPlayerBasedOnPosn((x, y)) != None:
                    actorname = self.getPlayerBasedOnPosn((x, y)).playerName()
                    if name != actorname:
                        actors += [{"type" : "player", "name" : actorname, "position" : [y, x]}]

                if self.getAdversaryBasedOnPosn((x, y)) != None:
                    ad = self.getAdversaryBasedOnPosn((x, y))
                    adname = ad.adversaryName()
                    adtype = ad.adversaryType()
                    actors += [{"type" : adtype, "name" : adname, "position" : [y, x]}]
            layout += [row]
        return [layout, objects, actors]

    """
    randomly generate a list of positions based on the given player number
    playerNum: the number of players need to have a position
    return a list of posns in tuple format
    """
    def generatePlayer(self, playerNum):
        freetiles = self.__map.returnUpperLeftRoomFreeTiles()
        positions = random.sample(freetiles, playerNum)
        result = []
        for position in positions:
            result+= [position]
        return result

    """
    randomly generate a list of positions based on the given level number
    return a tuple of 2 list, which first list will be a list of positions
    in tuple format corresponding to positions for zombies, the other
    will be for ghost
    levelNum: int, the total number of levels of this game
    """
    def generateAdversary(self, levelNum):
        freetiles = self.__map.returnDownRightRoomFreeTiles()
        numZombies = math.floor(levelNum / 2) + 1
        numGhosts = math.floor((levelNum - 1) / 2)
        zPositions = []
        gPositions = []
        if numZombies != 0:
            zPositions = random.sample(freetiles, numZombies)
        if numGhosts != 0:
            gPositions = random.sample(freetiles, numGhosts)
        return (zPositions, gPositions)

    """
    return the unlock status of this game
    """
    def getUnlock(self):
        if self.__unlock:
            return True
        else:
            return False

    """
    update the unlock status of this game
    """
    def updateUnlock(self,status):
        self.__unlock = status

    """
    remove the player from the players list
    posn: position point in tuple style
    """
    def removePlayer(self, posn):
        if posn in self.__players.keys():
            del self.__players[posn]
        else:
            pass

    """
    remove the adversary from the adversary list
    posn: position point in tuple style
    """
    def removeAdversary(self, posn):
        if posn in self.__adversaries.keys():
            del self.__adversaries[posn]


    """
    move the player with given name to given destination
    dest: position in tuple style
    name: string, the name of the player that need to be moved
    """
    def movePlayer(self, dest, name):
        player = self.getPlayer(name)
        # change dictionary
        playerPosition = player.playerPosition()
        self.__players[dest] = player
        self.removePlayer(playerPosition)
        self.__players[dest].move(dest)
        return self

    """
    send the given ghost to a random room
    ghost: Adversary of type ghost
    posn: current position of this adversary in tuple style
    """
    def moveGhostRandomly(self, ghost, posn):
        dest = self.__map.returnRandomPosn()
        object = self.returnObject(dest)
        while object != "1" and object != "2":
            dest = self.__map.returnRandomPosn()
            object = self.returnObject(dest)
        self.__adversaries[dest] = ghost
        self.removeAdversary(posn)
        self.__adversaries[dest].move(dest)
        return self

    """
    move the adversary with given name to the given desination
    dest: position in tuple style
    name: stringm the name of the adversary that need to be moved
    """
    def moveAdversary(self, dest, name):
        adversary = self.getAdversary(name)
        adPosn = adversary.adversaryPosns()
        adType = adversary.adversaryType()
        if self.returnObject(dest) == "x" and adType == "ghost":
            return self.moveGhostRandomly(adversary, adPosn)
        else:
            self.removeAdversary(adPosn)
            self.__adversaries[dest] = adversary
            self.__adversaries[dest].move(dest)
            return self

    """
    place the object to the given position in the map
    object: string, indicating the type of the object, either being key or exit
    posn: position to be moved to in tuple style
    """
    def placeObject(self, object, posn):
        return self.__map.placeObject(object,posn)

    """
    get the adversary based on the given position
    position: position in tuple style
    """
    def getAdversaryBasedOnPosn(self, posn):
        try:
            adversary = copy.deepcopy(self.__adversaries[posn])
            return adversary
        except KeyError:
            return None

    """
    get the player based on the given position
    position: position in tuple style
    """
    def getPlayerBasedOnPosn(self, posn):
        try:
            player = copy.deepcopy(self.__players[posn])
            return player
        except KeyError:
            return None

    """
    get the player based on the given name
    name: string, player name need to be find
    """
    def getPlayer(self, name):
        for player in self.__players.values():
            if player.playerName() == name:
                return player
                break
        return None

    """
    get the adversary based on the given name
    name: string, adversary name need to be find
    """
    def getAdversary(self, name):
        for adversary in self.__adversaries.values():
            if adversary.adversaryName() == name:
                return adversary
                break
        return None

    """
    check if all players and adversary has valid positions
    """
    def checkValidPositions(self):
        for player in self.__players.keys():
            if not self.checkValidPosition(player):
                return False
                break
        for adversary  in self.__adversaries.keys():
            if not self.checkValidPosition(adversary):
                return False
                break
        return True

    """
    check if the position is valid by checking if it is a wall or is a empty
    tuple, the map is a 2D array, if it is a wall, it will be "x", if it does
    not have anything, meaning is not a free tile, or an object, it will be just
    a tuple
    position: given position in tuple style
    """
    def checkValidPosition(self, position):
        if not self.checkInsideMap(position):
            return False
        object = self.returnObject(position)
        if object == "x":
            return False
        elif type(object) == tuple:
            return False
        elif object == None:
            return False
        else:
            return True

    """
    make sure given position is in the range of current min and max x and y
    value. return boolean
    position: given position in tuple style
    """
    def checkInsideMap(self, position):
        bound = self.__map.maxXminXmaxYminY()
        if position[0] > bound[0] or position[0] < bound[1]:
            return False
        if position[1] > bound[2] or position[1] < bound[3]:
            return False
        return True
    """
    return the object in the given position
    position: given position in tuple style
    """
    def returnObject(self, position):
        map = self.__map.renderLevel()
        bound = self.__map.maxXminXmaxYminY()
        minX = bound[1]
        minY = bound[3]
        plusX = 0 - minX
        plusY = 0 - minY
        result = None
        try:
            result =  map[position[1] + plusY][position[0] + plusX]
        except IndexError:
            result =  (position[1] + plusY, position[0] + plusX - 1)
        return result

    """
    check if any names or positions of players and adversaries is repeated, meaning
    adversary standing on adversary or player standing on players, or player
    and player has repeated name, or adversary and adversary has repeated name
    """
    def checkNoneRepeatOccupy(self):
        adversaryNames = []
        playerNames = []
        for adversary in self.__adversaries.values():
            adversaryNames += [adversary.adversaryName()]
        for player in self.__players.values():
            playerNames += [player.playerName()]

        repeatPlayerName = len(set(playerNames)) == len(playerNames)
        repeatAdversaryName = len(set(adversaryNames)) == len(adversaryNames)
        repeatAdLocation = len(set(self.__adversaries.keys()))==len(self.__adversaries.keys())
        repeatPlLocation = len(set(self.__players.keys())) == len(self.__players.keys())
        return repeatPlayerName and repeatAdversaryName and repeatAdLocation and repeatPlLocation


    """
    draw this game state
    """
    def draw(self):
        map = self.render()
        level = SnarlLevel([], [])
        return level.drawMap(map)

    """
    render the game level with players and adversaries, replace all the empty
    tuple with p to represent players and replace all the empty tuple with a
    to represent adversaries
    """
    def render(self):
        result = self.__map.renderLevel()
        bound = self.__map.maxXminXmaxYminY()
        minX = bound[1]
        minY = bound[3]
        plusX = 0 - minX
        plusY = 0 - minY
        for player in self.__players.values():
            playerPosn = player.playerPosition()
            result[playerPosn[1] + plusY][playerPosn[0] + plusX] = player.playerName()
        for adversary in self.__adversaries.values():
            adPosn = adversary.adversaryPosns()
            adType = adversary.adversaryType()
            if adType == "zombie":
                result[adPosn[1] + plusY][adPosn[0] + plusX] = "z"
            else:
                result[adPosn[1] + plusY][adPosn[0] + plusX] = "g"
        return result


    """
    renders the tiles around given position. returns empty list if
    given position is not inside the current map.
    posn: turple
    """
    def renderAround(self,posn):
        layout = []
        actors = []
        for y in range(posn[1] - 2, posn[1] + 3):
            row = []
            index = 0
            for x in range(posn[0] - 2, posn[0] + 3):
                object = self.returnObject((x, y))
                if object == None:
                    row+=[None]
                else:
                    row+=[object]

                if self.getPlayerBasedOnPosn((x, y)) != None:
                    actorname = self.getPlayerBasedOnPosn((x, y)).playerName()
                    row[index]= actorname

                if self.getAdversaryBasedOnPosn((x, y)) != None:
                    ad = self.getAdversaryBasedOnPosn((x, y))
                    adname = ad.adversaryName()
                    adtype = ad.adversaryType()
                    if adtype == "zombie":
                        row[index]="z"
                    else:
                        row[index]="g"
                index+=1
            layout += [row]
        return layout

    """
    change the current game state with list of players, list of adversaries
    unlock statue and the map
    playerPosn: dictionary with key to be player position and value to be player
    adversaryPosns: dictionary with key to be adversary position and value to be adversary
    unlock: true or false indicating the state of the unlock
    level: the 2d array representing the map
    """
    @staticmethod
    def __changeGameState(self, playerPosns, adversaryPosns, unlock, level):
        self.__players = playerPosns
        self.__adversaries = adversaryPosns
        self.__unlock = unlock
        self.__level = level
        return self

    """
    get the number of players left in this level
    """
    def getPlayerLen(self):
        return len(self.__players)

    """
    get the positions of the each player in thie level
    return a list of positions in tuple format
    """
    def getPlayerPosns(self):
        return list(self.__players.keys())
