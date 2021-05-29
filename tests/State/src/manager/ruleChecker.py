from gamestate import GameState
from gamestate import Player
from gamestate import Adversary

"""
RuleChecker takes in a gamestate and a string indicating which turn it is
gamemanager will create a RuleChecker each time when it makes movement
"""
class RuleChecker:
    def __init__(self, gamestate):
        RuleChecker.__validateState(gamestate)
        self.__gamestate = gamestate

    """
    validate the given game state by checking if all the positions in the game
    state is valid and also contain all unique names for both players and adversaries
    """
    def __validateState(gamestate):
        if not gamestate.checkValidPositions():
            raise ValueError("Someone is standing on the wall")
        elif not gamestate.checkNoneRepeatOccupy():
            raise ValueError("Someone is standing on others")

    """
    return the message to indicate the potential interactions with the given
    position
    posn: position in tuple style
    if there's adversary in position, return "ejected"
    if there's key in the position, return "unlock"
    if there's exit in the position, if the unlock is true, return "exited"
    else do nothing
    else if the position is valid, return "valid"
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
    exist, if given name does not exist, raise value error, if movement is
    invalid return false, a invalid movement is when player is trying to
    move to wall or non free tile or trying to stand on other players
    or trying to move distance more than 2 block
    dest: position in tuple style
    name: string, the name of the player to be moved
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
    check if the given movement of a zombie is valid. First check if the destination
    is a valid position in the map. Then check if the movement follows the rules
    of zombie movement.
    zombie: Adversary
    dest: turple
    """
    def checkValidZoombieMove(self, zombie, dest):
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
    is a valid position in the map. Then check if the movement follows the rules
    of ghost movement.
    ghost: Adversary
    dest: turple
    """
    def checkValidGhostMove(self, ghost, dest):
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

    """
    check if the given adversary has no valid movement
    adversary: Adversary
    """
    def checkNonValidMovement(self, adversary):
        adPosn = adversary.adversaryPosns()
        adtype = adversary.adversaryType()
        if adtype == "zombie":
            for x in range(adPosn[0]-1, adPosn[0]+2, 2):
                if self.checkValidZoombieMove(adversary, (x,adPosn[1])):
                    return False
            for y in range(adPosn[1]-1, adPosn[1]+2,2):
                if self.checkValidZoombieMove(adversary, (adPosn[0],y)):
                    return False

        if adtype == "ghost":
            for x in range(adPosn[0]-1, adPosn[0]+2, 2):
                if self.checkValidGhostMove(adversary, (x,adPosn[1])):
                    return False
            for y in range(adPosn[1]-1, adPosn[1]+2,2):
                if self.checkValidGhostMove(adversary, (adPosn[0],y)):
                    return False
        return True


    """
    check if the given movement for the adversary with given name if valid,
    check if the destination is valid and also check if the given name exist
    if given name does not exit, raise error, if movement is invalid return False
    an invalid movement is when adversary is trying to move to wall or none free
    tiles or trying to stand on other adversaries or trying to move distance more
    than 1 block
    dest: position in tuple style
    name: string, the name of the player to be moved
    """
    def checkValidAdversaryMovement(self, dest, name):
        adversary = self.__gamestate.getAdversary(name)
        if adversary == None:
            raise ValueError("Cannot find with the given adversary")
        adPosn = adversary.adversaryPosns()
        # cannot skip a move, unless there is no valid move in any cardinal direction.
        if adPosn[0] == dest[0] and adPosn[1] == dest[1]:
            return self.checkNonValidMovement(adversary)
        # movement > 1 tile
        if abs(adPosn[0] - dest[0]) + abs(adPosn[1] - dest[1]) > 1:
            return False
        adtype = adversary.adversaryType()
        # check for more details
        if adtype == "zombie":
            return self.checkValidZoombieMove(adversary,dest)
        elif adtype == "ghost":
            return self.checkValidGhostMove(adversary,dest)
        else:
            return False
