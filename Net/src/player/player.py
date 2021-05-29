from abc import ABC, abstractmethod
from src.state.gamestate import GameState
from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel
from src.state.gamestate import Player, Adversary, GameState
import json
import copy

class PlayerInterface(ABC):
    """
    move the player to the given dest
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: Player Component Class
    @return: move the player and return self
    """
    @abstractmethod
    def move(self, dest):
        pass

    """
    move the player to the given dest and update in the given manager
    @type manager: GameManager Class
    @param manager: The manager class to update the movement
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: GameManager Class
    @return: update the manager class and return it
    """
    @abstractmethod
    def request_move(self, manager, dest):
        pass

    """
    request interaction for the player
    @type manager: GameManager Class
    @param manager: The manager class to update the movement
    @type dest: tuple of two numbers, (number, number)
    @param dest: the destination to move to
    @rtype: String
    @return: message for interaction between player and the destination tile
    """
    @abstractmethod
    def request_interaction(self, manager, dest):
        pass

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
        pass

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
        pass
