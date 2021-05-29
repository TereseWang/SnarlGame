from src.state.gamestate import GameState
from src.state.gamestate import Player
from src.state.gamestate import Adversary

"""
RuleChecker takes in a gamestate and a string indicating which turn it is
gamemanager will create a RuleChecker each time when it makes movement
"""
class RuleChecker:
    """
    Constructor
    @type gamestate: GameState Class
    @param gamestate: the gamestate to check with
    """
    def __init__(self, gamestate):
        RuleChecker.__validateState(gamestate)
        self.__gamestate = gamestate

    """
    validate the given game state by checking if all the positions in the game
    state is valid and also contain all unique names for both players and adversaries
    @type gamestate: GameState Class
    @param gamestate: the gamestate to check with
    @rtype: None
    @return: None
    """
    def __validateState(gamestate):
        if not gamestate.checkValidPositions():
            raise ValueError("Someone is standing on the wall")
        elif not gamestate.checkNoneRepeatOccupy():
            raise ValueError("Someone is standing on others")

    """
    return the message to indicate the potential interactions with the given
    position for player
    @type posn: tuple of two number, (number, number)
    @param posn: the position of tile to interact with
    @rtype: String
    @return: the message to indicate the potential interactions with the given
    position
    """
    def returnInteraction(self, posn):
        object = self.__gamestate.returnObject(posn)
        adversary = self.__gamestate.getAdversaryBasedOnPosn(posn)
        unlock = self.__gamestate.getUnlock()
        if adversary != None:
            return "ejected"
        elif object == "k":
            return "unlock"
        elif object == "e":
            if unlock:
                return 'exited'
            else:
                return 'locked'
        return "valid"

    """
    return the message to indicate the potential interactions with the given
    position for adversary
    @type posn: tuple of two number, (number, number)
    @param posn: the position of tile to interact with
    @rtype: String or Player Class
    @return: the message to indicate the potential interactions with the given
    elif adversary expell the player return the player class
    """
    def returnAdInteraction(self, posn):
        object = self.__gamestate.returnObject(posn)
        player = self.__gamestate.getPlayerBasedOnPosn(posn)
        if player != None:
            return player
        else:
            return "moved"

    """
    check if the given movement for the player with given name is valid
    check if the given destination is valid and also check if the given name
    exist
    @type dest: tuple of two number, (number, number)
    @param dest: the destination position to be moved to
    @type name: String
    @param name: the name of the player to move
    @rtype: Boolean
    @return: check if the given name exist and also check if the movement is
    valid or not
    """
    def checkValidPlayerMovement(self, dest, name):
        player = self.__gamestate.getPlayer(name)
        if player == None:
            return False
        playerPosn = player.playerPosition()
        try:
            if not self.__gamestate.checkValidPosition(dest):
                return False
            if self.__gamestate.getPlayerBasedOnPosn(dest) != None:
                return False
            distance = (dest[0] - playerPosn[0])**2 + (dest[1] - playerPosn[1])**2
            if distance > 4:
                return False
        except IndexError:
            return False
        return True

    """
    check if the given movement for the adversary with given name is valid
    check if the given destination is valid and also check if the given name
    exist
    @type dest: tuple of two number, (number, number)
    @param dest: the destination position to be moved to
    @type name: String
    @param name: the name of the player to move
    @rtype: Boolean
    @return: check if the given name exist and also check if the movement is
    valid or not
    """
    def checkValidAdversaryMovement(self, dest, name):
        adversary = self.__gamestate.getAdversary(name)
        if adversary == None:
            raise ValueError("Cannot find with the given adversary")
        adPosn = adversary.adversaryPosns()
        if adPosn[0] == dest[0] and adPosn[1] == dest[1]:
            return self.__checkNonValidMovement(adversary)
        # movement > 1 tile
        if abs(adPosn[0] - dest[0]) + abs(adPosn[1] - dest[1]) > 1:
            return False
        adtype = adversary.adversaryType()
        # check for more details
        if adtype == "zombie":
            return self.__checkValidZoombieMove(adversary,dest)
        elif adtype == "ghost":
            return self.__checkValidGhostMove(adversary,dest)
        else:
            return False

    """
    check if the given adversary has no valid movement
    @type adversary: Adversary Class
    @param adversary: the adversary to check with position
    @rtype: Boolean
    @return: whether if the movement for adversary is valid
    """
    def __checkNonValidMovement(self, adversary):
        adPosn = adversary.adversaryPosns()
        adtype = adversary.adversaryType()
        if adtype == "zombie":
            for x in range(adPosn[0]-1, adPosn[0]+2, 2):
                if self.__checkValidZoombieMove(adversary, (x,adPosn[1])):
                    return False
            for y in range(adPosn[1]-1, adPosn[1]+2,2):
                if self.__checkValidZoombieMove(adversary, (adPosn[0],y)):
                    return False
        if adtype == "ghost":
            for x in range(adPosn[0]-1, adPosn[0]+2, 2):
                if self.__checkValidGhostMove(adversary, (x,adPosn[1])):
                    return False
            for y in range(adPosn[1]-1, adPosn[1]+2,2):
                if self.__checkValidGhostMove(adversary, (adPosn[0],y)):
                    return False
        return True

    """
    check if the given movement of a zombie is valid. First check if the destination
    is a valid position in the map.
    @type zombie: Adversary Class
    @param zombie: the adversary class to check with position
    @type dest: tuple of two number, (number, number)
    @param dest: the destination position to check with
    @rtype: Boolean
    @return: check whether the given destination for zombie is valid
    """
    def __checkValidZoombieMove(self, zombie, dest):
        # check not on another adversary
        if self.__gamestate.getAdversaryBasedOnPosn(dest) is not None:
            return False
        # check not on the wall or out of the map
        if not self.__gamestate.checkValidPosition(dest):
            return False
        object = self.__gamestate.returnObject(dest)
        # zombie cannot pass a door
        if object == "+":
            return False
        if object == "2":
            return False
        return True

    """
    check if the given movement of a ghost is valid. First check if the destination
    is a valid position in the map.
    @type ghost: Adversary Class
    @param ghost: the adversary class to check with position
    @type dest: tuple of two number, (number, number)
    @param dest: the destination position to check with
    @rtype: Boolean
    @return: check whether the given destination for ghost is valid
    """
    def __checkValidGhostMove(self, ghost, dest):
        # check out of map
        if self.__gamestate.getAdversaryBasedOnPosn(dest) is not None:
            return False
        if not self.__gamestate.checkInsideMap(dest):
            return False
        # check if it runs out of the room area
        object = self.__gamestate.returnObject(dest)
        if type(object) == tuple:
            return False
        elif object == None:
            return False
        return True
