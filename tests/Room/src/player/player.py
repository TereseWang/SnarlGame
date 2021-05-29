from abc import ABC, abstractmethod
from gamestate import GameState
from room import Room
from hallway import Hallway
from level import SnarlLevel
from gamestate import Player, Adversary, GameState
import json
import copy



class PlayerInterface(ABC):
    """
    request a movement to the given destination
    manager: GameManager
    dest_json: json showing the destination
    """
    @abstractmethod
    def request_move(self, manager, dest_json):
        pass


    """
    renders tiles around this player.
    manager: GameManager
    """
    @abstractmethod
    def renderView(self, manager):
        pass

    """
    update the position
    posn: turple
    """
    def updatePosn(self, posn):
        self.posn = posn

    """
    expel this player
    """
    def expel(self):
        self.expel = False

    """
    get the name of this player
    """
    def get_name(self):
        return self.name


    """
    find the current position of this player
    """
    def find_posn(self):
        return copy.deepcopy(self.posn)
