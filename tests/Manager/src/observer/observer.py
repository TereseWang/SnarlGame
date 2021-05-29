from abc import ABC, abstractmethod
from gamestate import GameState
import os.path
# Import the pygame module
import pygame
from room import Room
from hallway import Hallway
from level import SnarlLevel
from gamestate import Player, Adversary, GameState


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

    """
    renders the whole map.
    gamestate: GameState
    """
    @abstractmethod
    def renderMap(self, gamestate, namelist):
        pass

    """
    renders tiles near the given position
    gamestate: GameState
    posn: turple
    """
    @abstractmethod
    def renderLevelPlayerView(self, gamestate, posn, namelist):
        pass
