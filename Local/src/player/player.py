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
