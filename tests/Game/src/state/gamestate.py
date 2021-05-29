#!/usr/bin/python3
from src.state.level import SnarlLevel
from src.state.room import Room
from src.state.hallway import Hallway
import random
import copy
import math

"""
A Player is composed of a position and we will add user name feature later,
it will also contain a boolean to check if this player had find an unlocked
exit to helps us to check if the game is over or not
"""
class  Player:
    '''
    Constructor arguments:
    :param  __position:     tuple of int, the position of this player
    :param  __name:         String, the name of this player
    :param  __exited        boolean, the status of this player
    '''
    def __init__(self, name, posn):
        self.__position = posn
        self.__name = name
        self.__exited = False


    def playerName(self):
        """
        return the name of this player
        @rtype:     String
        @return:    name of this player
        """
        return self.__name


    def playerPosition(self):
        """
        return the position of this player
        @rtype:     tuple of int
        @return:    position of this player
        """
        return copy.deepcopy(self.__position)


    def playerExited(self):
        """
        return if this player had find the unlocked exit
        @rtype:     boolean
        @return:    status of this player
        """
        return copy.copy(self.__exited)


    def move(self, movement):
        """
        update the movement
        """
        self.__position = movement


"""
A Adversary will composed of a position in tuple format and a type indicating
the type of adversary("zoombie", "ghost") and so
"""
class  Adversary:
    '''
    Constructor arguments:
    :param  __position:     tuple of int, the position of this adversary
    :param  __name:         String, the name of this adversary
    :param  __exited        boolean, the status of this adversary
    '''
    def __init__(self, posn, name, type):
        self.__position = posn
        self.__type = type
        self.__name = name

    def adversaryName(self):
        """
        return the name of this adversary
        @rtype:     String
        @return:    name of this adversary
        """
        return self.__name


    def adversaryPosns(self):
        """
        return the position of this adversary
        @rtype:     tuple of int
        @return:    position of this adversary
        """
        return copy.deepcopy(self.__position)

    def adversaryType(self):
        """
        return if this adversary had been killed
        @rtype:     boolean
        @return:    status of this adversary
        """
        return self.__type


    def move(self, movement):
        """
        update the movement to adversary's position
        """
        self.__position = movement




"""
A Game State is composed of a
map: 2D Array of tuple(int, int) including all items position in this game

"""
class GameState:
    '''
    Initialize the game by inputting a map, a total player number and an
    adversary number
    :param         level: A SnarlLevel
    :param     playerNum: int, total number of player will play this game
    :param  adversaryNum: int, total number of adversary in this game
    '''
    def __init__(self, level, playerList, adversaryList):
        self.__map = level
        self.__players = playerList   # {posn : Player}
        self.__adversaries = adversaryList #{posn : Adversary}
        self.__unlock = False



    def returnPlayerTiles(self, name, posn):
        """
        return the tiles surround the given player with the given name and
        given position
        @type       name:   String
        @param      name:   the name of the player
        @type       posn:   tuple of int
        @param      posn:   the position of the player
        @rtype:             2D Array
        @return:            all tiles around the given player
        """
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


    def renderAround(self,posn):
        """
        renders the tiles around given position. returns empty list if
        given position is not inside the current map.
        @type    posn:   tuple of int
        @param   posn:   position at the center
        @rtype:          2D List
        @return:         tiles around the given position
        """
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


    @staticmethod
    def __changeGameState(self, playerPosns, adversaryPosns, unlock, level):
        """
        change the current game state with list of players, list of adversaries
        unlock statue and the map
        @type       playerPosns:  dictionary {tuple:Player}
        @param      playerPosns:  {position, Player}
        @type    adversaryPosns:  dictionary {tuple:Adversary}
        @param   adversaryPosns:  {position, Adversary}
        @type            unlock:  boolean
        @param           unlock:  the exit states
        @type             level:  2D array
        @param            level:  level map info
        @rtype:                   GameState
        @return:                  the updated game state
        """
        self.__players = playerPosns
        self.__adversaries = adversaryPosns
        self.__unlock = unlock
        self.__level = level
        return self



    def checkNoneRepeatOccupy(self):
        """
        check if any names or positions of players and adversaries is repeated, meaning
        adversary standing on adversary or player standing on players, or player
        and player has repeated name, or adversary and adversary has repeated name
        @rtpe:      boolean
        @return:    whether there is occupy
        """
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



    def returnJsonPlayers(self):
        """
        return the players in json style
        @rtype:     JSON
        @return:    the player information in this game
        """
        result = []
        for posn, player in self.__players.items():
            playerJson = {
            "type": "player",
            "name": player.playerName(),
            "position": [posn[1], posn[0]]}
            result+=[playerJson]
        return result


    def returnJsonAdversaries(self):
        """
        return the adversary list in json style
        @rtype:     JSON
        @return:    the adversary information in this game
        """
        result = []
        for posn, ad in self.__adversaries.items():
            adJson = {
            "type": ad.adversaryType(),
            "name": ad.adversaryName(),
            "position": [posn[1], posn[0]]}
            result+=[adJson]
        return result


    def generatePlayer(self, playerNum):
        """
        randomly generate a list of positions based on the given player number
        @type     playerNum:   int
        @param    playerNum:   the number of the player
        @rtype:                List of tuple of int
        @return:               player initial positions
        """
        freetiles = self.__map.returnUpperLeftRoomFreeTiles()
        positions = random.sample(freetiles, playerNum)
        result = []
        for position in positions:
            result+= [position]
        return result



    def generateAdversary(self, levelNum):
        """
        randomly generate a list of positions based on the given level number
        return a tuple of 2 list, which first list will be a list of positions
        in tuple format corresponding to positions for zombies, the other
        will be for ghost
        @type     levelNum:   int
        @param    levelNum:   total number of levels of this game
        @rtype:               List of tuple of int
        @return:              adverasry initial positions
        """
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



    def getUnlock(self):
        """
        return the unlock status of this game
        @rtype:     boolean
        @return:    whether current exit is locked
        """
        if self.__unlock:
            return True
        else:
            return False


    def getPlayerLen(self):
        """
        get the number of players left in this level
        @rtype:     int
        @return:    total number of players
        """
        return len(self.__players)


    def getPlayerPosns(self):
        """
        get the positions of the each player in thie level
        @rtype:        list of tuple of int
        @return:       positions of each player in the level
        """
        return list(self.__players.keys())



    def updateUnlock(self,status):
        """
        update the unlock status of this game
        @type   status:   boolean
        @param  status:   the exit lock status
        """
        self.__unlock = status


    def draw(self):
        """
        draw this game state
        @rtype:     String
        @return:    all information in the map and player, adversary position
        """
        map = self.render()
        level = SnarlLevel([], [])
        return level.drawMap(map)




    def movePlayer(self, dest, name):
        """
        move the player with given name to given destination
        @type      dest:    tuple of int
        @param     dest:    the destination of this move
        @type      name:    String
        @param     name:    name of the player we want to move
        @rtype:             GameState
        @return:            updated game state
        """
        player = self.getPlayer(name)
        # change dictionary
        playerPosition = player.playerPosition()
        self.__players[dest] = player
        self.removePlayer(playerPosition)
        self.__players[dest].move(dest)
        return self


    def moveAdversary(self, dest, name):
        """
        move the adversary with given name to the given desination
        @type      dest:    tuple of int
        @param     dest:    the destination of this move
        @type      name:    String
        @param     name:    name of the adversary we want to move
        @rtype:             GameState
        @return:            updated game state
        """
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


    def checkValidPositions(self):
        """
        check if all players and adversary has valid positions
        @rtype:     boolean
        @return:    validity of all players and adversaries in the game
        """
        for player in self.__players.keys():
            if not self.checkValidPosition(player):
                return False
                break
        for adversary  in self.__adversaries.keys():
            if not self.checkValidPosition(adversary):
                return False
                break
        return True



    def placeObject(self, object, posn):
        """
        place the object to the given position in the map
        @type       object:     String
        @param      object:     type of the object, key or exit
        @type         posn:     tuple of int
        @param        posn:     position to place the object
        @rtype:                 boolean
        @return:                whether the placement is successful
        """
        return self.__map.placeObject(object,posn)






    def render(self):
        """
        render the game level with players and adversaries, replace all the empty
        tuple with p to represent players and replace all the empty tuple with a
        to represent adversaries
        @rtype:     2D list
        @return:    map information and player, adversary position info
        """
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



    def checkValidPosition(self, position):
        """
        check if the position is valid by checking if it is a wall or is a empty
        tuple, the map is a 2D array, if it is a wall, it will be "x", if it does
        not have anything, meaning is not a free tile, or an object, it will be just
        a tuple
        @type   position:   tuple of int
        @param  position:   position hope to be checked
        @rtype:             boolean
        @return:            whether the given position is valid
        """
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



    def removePlayer(self, posn):
        """
        remove the player from the players list
        @type   posn:   tuple of int
        @param  posn:   position of the player we want to move
        """
        if posn in self.__players.keys():
            del self.__players[posn]
        else:
            pass


    def moveGhostRandomly(self, ghost, posn):
        """
        send the given ghost to a random room. Make sure it doesn't step on
        a player, a wall tile or other adversaries.
        @type      posn:    tuple of int
        @param     posn:    the current position of the ghost
        @type     ghost:    Adversary
        @param    ghost:    ghost we want to move
        @rtype:             GameState
        @return:            updated game state
        """
        dest = self.__map.returnRandomPosn()
        object = self.returnObject(dest)
        while object != "1" and object != "2":
            dest = self.__map.returnRandomPosn()
            object = self.returnObject(dest)
        self.__adversaries[dest] = ghost
        self.removeAdversary(posn)
        self.__adversaries[dest].move(dest)
        return self




    def checkInsideMap(self, position):
        """
        make sure given position is in the range of current min and max x and y
        value.
        @type   position:   tuple of int
        @param  position:   position hope to be checked
        @rtype:             boolean
        @return:            whether the given position in the range
        """
        bound = self.__map.maxXminXmaxYminY()
        if position[0] > bound[0] or position[0] < bound[1]:
            return False
        if position[1] > bound[2] or position[1] < bound[3]:
            return False
        return True


    def removeAdversary(self, posn):
        """
        remove the adversary from the adversary list
        @type   posn:   tuple of int
        @param  posn:   position of the adversary we want to move
        """
        if posn in self.__adversaries.keys():
            del self.__adversaries[posn]



    def returnObject(self, position):
        """
        return the object in the given position
        @type   position:   tuple of int
        @param  position:   the position to find the object
        @rtype:             String
        @return:            object
        """
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




    def getAdversaryBasedOnPosn(self, posn):
        """
        get the adversary based on the given position
        @type    posn:  tuple of int
        @param   posn:  position of the adversary
        @rtype:         Adversary
        @return:        the adversary on the given position
        """
        try:
            adversary = copy.deepcopy(self.__adversaries[posn])
            return adversary
        except KeyError:
            return None



    def getPlayerBasedOnPosn(self, posn):
        """
        get the player based on the given position
        @type    posn:  tuple of int
        @param   posn:  position of the player
        @rtype:         Player
        @return:        the player on the given position
        """
        try:
            player = copy.deepcopy(self.__players[posn])
            return player
        except KeyError:
            return None



    def getPlayer(self, name):
        """
        get the player based on the given name
        @type    name:  String
        @param   name:  name of the player
        @rtype:         Player
        @return:        the player of given name
        """
        for player in self.__players.values():
            if player.playerName() == name:
                return player
                break
        return None



    def getAdversary(self, name):
        """
        get the adversary based on the given name
        @type    name:  String
        @param   name:  name of the adversary
        @rtype:         Adversary
        @return:        the adversary of given name
        """
        for adversary in self.__adversaries.values():
            if adversary.adversaryName() == name:
                return adversary
                break
        return None
