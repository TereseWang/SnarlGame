from abc import ABC, abstractmethod
from src.state.gamestate import GameState
from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel
from src.state.gamestate import Player, Adversary, GameState
from src.player.player import PlayerInterface
from src.observer.LocalObserver import Observer
import json
import copy

class Player(PlayerInterface):
    def __init__(self, name, turn, posn):
        """
        Constructor
        @type name: String
        @param name: Player Name
        @type turn: Number
        @param turn: Number indicating the turn number, start from 0
        @type posn: Tuple of two numbers, (number, number)
        @param posn: position of the player
        """
        self.name = name
        self.turn = turn
        self.posn = posn
        self.expeled = False

    """
    move the player to the given dest
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: Player Component Class
    @return: move the player and return self
    """
    def move(self, dest):
        self.posn = dest
        return self

    """
    move the player to the given dest and update in the given manager
    @type manager: GameManager Class
    @param manager: The manager class to update the movement
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: GameManager Class
    @return: update the manager class and return it
    """
    def request_move(self, manager, dest):
        if dest == None:
            manager = manager.move_player(self.name, self.posn)
        else:
            manager = manager.move_player(self.name, dest)
        return manager

    """
    request interaction for the player
    @type manager: GameManager Class
    @param manager: The manager class to update the movement
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: String
    @return: message for interaction between player and the destination tile
    """
    def request_interaction(self, manager, dest):
        return manager.respond_to_interaction(self.name, dest)

    """
    render the player view
    @type manager: GameManager Class
    @param manager: GameManager
    @type namelist: List of String
    @param namelist: a list of player names in string format
    @rtype: PyGame.screen
    @return: return the screen of pygame rendering the observer view
    """
    def renderView(self, map, namelist):
        obs = Observer(1200, 800)
        return obs.renderLevelPlayerView(map, self.posn, namelist)

    """
    render the observer view
    @type manager: GameManager Class
    @param manager: GameManager
    @type namelist: List of String
    @param namelist: a list of player names in string format
    @rtype: PyGame.screen
    @return: return the screen of pygame rendering the observer view
    """
    def renderObView(self, map, namelist):
        return obs.renderMap(map, namelist)
