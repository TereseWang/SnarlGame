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
    def renderView(self, manager, namelist):
        gamestate = manager.returnGameState()
        obs = Observer(1200, 800)
        return obs.renderLevelPlayerView(gamestate, self.posn, namelist)

    """
    render the observer view
    manager: GameManager
    namelist: a list of player names in string format
    return the screen of pygame rendering the observer view
    """
    def renderObView(self, manager, namelist):
        gamestate = manager.returnGameState()
        obs = Observer(1200, 900)
        return obs.renderMap(gamestate, namelist)
