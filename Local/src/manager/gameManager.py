from src.state.gamestate import GameState
from src.state.gamestate import Player
from src.state.gamestate import Adversary
from src.manager.ruleChecker import RuleChecker
from src.state.level import SnarlLevel
from src.state.room import Room
from src.state.hallway import Hallway
import random
import copy
from src.observer.LocalObserver import Observer
import pygame
from src.adversary.adversaryComponent import AdversaryComponent
'''
A GameManager is able toregister players and adversaries and start and supervise
a Snarl game. It stores the gamestate and keeps updating it after any operation.
It is composed of a Player list, an Adversary list, a GameState, a String representing
current status and integers representing current and total level.
'''
class GameManager:
    def __init__(self, namelist, level, numturns, adversaryList, playerList):
        self.__adversaryList = GameManager.__register_adversaries(adversaryList);
        self.__playerList = GameManager.__register_players(namelist, playerList);
        self.__numturns = numturns;
        self.__level = level;
        self.__gamestate = GameState(level, self.__playerList, self.__adversaryList);
        self.__exit = False;
        checker = RuleChecker(self.__gamestate)

    """
       Register between 1 and 4 players using the given names. Each name should
    be unique
       takes in a list of String representing player names.
    """
    def __register_players(namelist, playerList):
        if len(namelist) > 4:
            return None
        result = {}
        for i in range(0, len(namelist)):
            player = Player(namelist[i], playerList[i])
            result[playerList[i]] = player
        return result

    """
    register a given number of adversaries, takes in a integer
    """
    def __register_adversaries(adversaryList):
        zlist = adversaryList[0]
        glist = adversaryList[1]
        result = {}
        for i in range(0, len(zlist)):
            posn = zlist[i]
            name = "z" + str(i)
            adversary = Adversary(posn, name, "zombie")
            result[posn] = adversary
        for i in range(0, len(glist)):
            posn = glist[i]
            name = "g" + str(i)
            adversary = Adversary(posn, name, "ghost")
            result[posn] = adversary
        return result

    """
    return this game manager's adversary list in adversary componenet format
    """
    def handleAdversary(self):
        result = []
        for adversary in self.__adversaryList.values():
            name = adversary.adversaryName()
            posn = adversary.adversaryPosns()
            type = adversary.adversaryType()
            component = AdversaryComponent(name, self.__gamestate, posn, type)
            result += [component]
        return result

    """ move the player of given name to a given destination
        name shoule be a String and destination should be a turple"""
    def move_player(self, name, dest):
        rule = RuleChecker(self.__gamestate)
        if dest == None:
            return self
        elif rule.checkValidPlayerMovement(dest,name):
            self.__gamestate.movePlayer(dest,name)
            return self
        else:
            return("please re-enter movement")

    """
    move the adversary of given name to a given destination
    name: string
    dest: turple
    """
    def move_adversary(self, name, dest):
        rule = RuleChecker(self.__gamestate)
        if dest == None:
            return copy.deepcopy(self.__gamestate)
        elif rule.checkValidAdversaryMovement(dest,name):
            self.__gamestate.moveAdversary(dest,name)
            return copy.deepcopy(self.__gamestate)
        else:
            return ("please re-enter movement")

    """ let the given player interact with the tile they are standing on
        name should be String and destination should be turple """
    def respond_to_interaction(self,name,dest):
        rule = RuleChecker(self.__gamestate)
        object = rule.returnInteraction(dest)
        if object == "ejected":
            self.__expell_player(dest)
            return "Eject"
        elif object == "unlock":
            self.__gamestate.updateUnlock(True)
            return "Key"
        elif object == "exited":
            self.__expell_player(dest)
            self.__exit = True;
            return "Exit"
        elif object == "locked":
            return "exit locked"
        else:
            return "OK"

    """
    return "ok" if nothing has touched, else return the name of the player being
    expelled
    dest: the destination position to be moved to in tuple format
    """
    def adversary_interaction(self, dest):
        rule = RuleChecker(self.__gamestate)
        object = rule.returnAdInteraction(dest)
        if object == "moved":
            return "ok"
        else:
            self.__expell_player(dest)
            return object.playerName()
    """
    return whether someone had exit the game
    """
    def __returnExitStatus(self):
        return self.__exit

    """
    return the number of players left in the game
    """
    def __returnPlayerLen(self):
        return self.__gamestate.getPlayerLen()

    """
    check if the level ended or not
    """
    def checkLevelEnd(self):
        levelend = self.__returnExitStatus() and self.__returnPlayerLen() == 0
        return levelend

    """
    check if all the players has been expelled or not
    """
    def checkEnd(self):
        end = self.__returnPlayerLen() == 0
        return end

    """ expells the player at given position, position should be turple """
    def __expell_player(self, posn):
        self.__gamestate.removePlayer(posn)
        return

    """ end the current level and move to next level. End the game if hit the last level """
    def __nextLevel(self):
        return

    """
    return the current game state
    """
    def returnGameState(self):
        return copy.deepcopy(self.__gamestate)

    def renderAround(self, posn):
        return self.__gamestate.renderAround(posn)
    """
    place the given object into the game state
    objects: list of object in jason format
    """
    def place_object(self, objects):
        for object in objects:
            type = object['type']
            posn = object['position']
            posn = (posn[1], posn[0])
            self.__gamestate.placeObject(type, posn)

if __name__ == '__main__':
    room1 = Room((3, 0), 4, 5, [(4, 1), (5, 1), (4, 2), (5, 2),
                    (4, 3), (5, 3), (6, 3), (4, 4)], [(4, 4), (6, 3)], None);
    room2 = Room((7, 5), 4, 4, [(8, 5), (8, 6), (9, 6), (10, 6), (8, 7), (9, 7)],
                    [(8, 5), (10, 6)], None)
    room3 = Room((12, 11), 3, 3, [(13, 11), (13, 12), (12, 12)], [(13, 11),
                    (12, 12)], {"exit": (13, 12)})
    room4 = Room((2, 10), 5, 5, [(4, 10), (3, 11), (4, 11), (5, 11), (3, 12),
                    (4, 12), (5, 12), (6, 12), (3, 13), (4, 13), (5, 13),
                    (4, 14)],[(4, 10), (4, 14), (6, 12)], None)
    room5 = Room((8, 15), 4, 4, [(8, 16), (9, 16), (10, 16), (11, 16)],
                    [(8, 16), (11, 16)], {"key" : (10, 16)})
    room6 = Room((13, 15), 6, 4, [(13, 16), (14, 16), (15, 16), (16, 16),
                    (17, 16), (14, 17), (15, 17), (16, 17), (17, 17)],
                    [(13, 16)], None)
    hallway = Hallway([(8, 3)], (6, 3), (8, 5))
    hallway1 = Hallway([(13, 6)], (10, 6), (13, 11))
    hallway2 = Hallway([(4, 6), (2, 6), (2, 8), (4, 8), (4, 9)], (4, 4), (4, 10))
    hallway3 = Hallway([(8, 12), (8, 10), (10, 10), (10, 12)], (6, 12), (12, 12))
    hallway4 = Hallway([(4, 16)], (4, 14), (8, 16))
    hallway5 = Hallway([], (11, 16), (13, 16))
    level = SnarlLevel([room1, room2, room3, room4, room5, room6],[hallway,
                            hallway1, hallway2, hallway3, hallway4, hallway5])
    namelist = ["dio", "ferd"]
    adversaryList = [(17, 16), (14, 17), (15, 17)]
    playerList = [(4, 1), (5, 1)]
    manager = GameManager(namelist, level, 4, adversaryList, playerList)
