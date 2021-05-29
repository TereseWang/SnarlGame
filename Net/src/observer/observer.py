from abc import ABC, abstractmethod
from src.state.gamestate import GameState
import os.path
# Import the pygame module
import pygame
from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel
from src.state.gamestate import Player, Adversary, GameState


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class ObserverInterface(ABC):


    @abstractmethod
    def renderMap(self, map, namelist):
        """
        renders the whole map
        @type       map:    2D Array
        @param      map:    map information with each cell contains info of a tile
        @type  namelist:    List of String
        @param namelist:    names of all players
        @rtype:             pygame screen
        @param:             the rendered game information
        """
        pass


    @abstractmethod
    def renderLevelPlayerView(self, map, posn, namelist):
        """
        renders the the player view that only contains tiles around this player
        @type       map:    2D Array
        @param      map:    map information with each cell contains info of a tile
        @type      posn:    tuple of int
        @param     posn:    position of the player
        @type  namelist:    List of String
        @param namelist:    names of all players
        @rtype:             pygame screen
        @param:             the rendered game information
        """
        pass
