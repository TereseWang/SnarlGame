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
    """
    constructor
    @type namelist: List of String
    @param namelist: the list of player names to register
    @type level: SnarlLevel class
    @param level: the map of the game
    @type numturns: number
    @param numturns: the number of maximum turns player has
    @type adversaryList: A tuple of two list of tuples of two number
                        ([(number, number) ...],[(number, number) ...])
    @param adversaryList: Positions indicating the input location of all adversaries
    @type playerList: List of tuples of two number [(number, number) ...]
    @param playerList: Positions inidicating the input location of all players
    """
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
    @type namelist: List of String
    @param namelist: the list of player names to register
    @type playerList: List of tuples of two number [(number, number) ...]
    @param playerList: Positions inidicating the input location of all players
    @rtype: dictionary, key to be tuple of two number, value to be Player Class
    @return: a dictionary that contains info about each single player
    """
    def __register_players(namelist, playerList):
        result = {}
        for i in range(0, len(namelist)):
            player = Player(namelist[i], playerList[i])
            result[playerList[i]] = player
        return result

    """
    register a given number of adversaries
    @type adversaryList: A tuple of two list of tuples of two number
                        ([(number, number) ...],[(number, number) ...])
    @param adversaryList: Positions indicating the input location of all adversaries
    @rtype: dictionary, key to be tuple of two number, value to be Adversary Class
    @return: a dictionary that contains info about each single adversary
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
    return tiles that is around the given posn
    @type posn: tuple of two number (number, number)
    @param posn: the input position
    @rtype: list of list of tuples of two number [(number, number)...]
    @return: the tiles that surround the given posn within 5 X 5 range
    """
    def renderAround(self, posn):
        return self.__gamestate.renderAround(posn)

    """
    return this game manager's adversary list in adversary componenet format
    @rtype: List of AdversaryComponent class
    @return: return this manager's adversary list in adversary component format
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

    """
    return the current game state
    @rtype: GameState
    @return: the gamestate of this game
    @rtype: None
    @return: None
    """
    def returnGameState(self):
        return copy.deepcopy(self.__gamestate)

    """
    place the given object into the game state
    @type objects: List of dictionary, containing info about type and position
    @param objects: list of obejects to be placed into game state
    @rtype: None
    @return: None
    """
    def place_object(self, objects):
        for object in objects:
            type = object['type']
            posn = object['position']
            posn = (posn[1], posn[0])
            self.__gamestate.placeObject(type, posn)
            
    """
    move the player of given name to a given destination
    @type name: String
    @param name: the name of the player to be moved
    @type dest: a tuple of two number, (number, number)
    @param dest: the destination point to be moved
    @rtype: GameManager Class or A String
    @return: if the destination is valid return self, else return a string message
    """
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
    @type name: string
    @param name: the name of adversary to be move to
    @type dest: turple of two number, (number, number)
    @param dest: the destination to move the given adversary to
    @rtype: GameState Class or String
    @return: gamestate if the movement is valid, else, return a message
    """
    def move_adversary(self, name, dest):
        rule = RuleChecker(self.__gamestate)
        if dest == None:
            return self
        elif rule.checkValidAdversaryMovement(dest,name):
            self.__gamestate.moveAdversary(dest,name)
            return self
        else:
            return ("please re-enter movement")

    """
    let the given player interact with the tile they are standing on
    @type name: string
    @param name: the name of adversary to be move to
    @type dest: turple of two number, (number, number)
    @param dest: the destination to move the given adversary to
    @rtype: String
    @return: a message telling user how they interact with the tile they are
    standing on
    """
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
    @type dest: turple of two number, (number, number)
    @param dest: the destination to move the given adversary to
    @rtype: String
    @return: if adversary eject the player return player's name else return "ok"
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
    Expells the player at given position
    @type posn: tuple of two number, (number, number)
    @param posn: the position of the player to be removed
    """
    def __expell_player(self, posn):
        self.__gamestate.removePlayer(posn)
        return
