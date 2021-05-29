from abc import ABC, abstractmethod
from gamestate import GameState
from room import Room
from hallway import Hallway
from level import SnarlLevel
from gamestate import Player, Adversary, GameState
from player import PlayerInterface
from LocalObserver import Observer
import json
import copy

class Player(PlayerInterface):

    def __init__(self, name, turn, posn):
        """
        :param name: string representation of the player
        :param turn: num indicates the turn number, start from 0
        :param position: turple
        :expeled: boolean indicats whether this player is expelled
        """
        self.name = name
        self.turn = turn
        self.posn = posn
        self.expeled = False

    """
    move the player to the given dest
    dest: position in tuple format
    """
    def move(self, dest):
        self.posn = dest
        return self

    #overiding abstract class
    def request_move(self, manager, dest):
        if dest == None:
            manager = manager.move_player(self.name, self.posn)
        else:
            manager = manager.move_player(self.name, dest)
        return manager

    def request_interaction(self, manager, dest):
        return manager.respond_to_interaction(self.name, dest)

    #overiding abstract class
    def renderView(self, map, namelist):
        obs = Observer(1200, 800)
        return obs.renderLevelPlayerView(map, self.posn, namelist)

    """
    render the observer view
    manager: GameManager
    namelist: a list of player names in string format
    return the screen of pygame rendering the observer view
    """
    def renderObView(self, map, namelist):
        return obs.renderMap(map, namelist)
