from src.state.gamestate import GameState
from src.state.gamestate import Player
from src.state.gamestate import Adversary
from src.manager.ruleChecker import RuleChecker
from src.state.level import SnarlLevel
from src.state.room import Room
from src.state.hallway import Hallway
import random
import copy

class AdversaryComponent:

    def __init__(self, name, gamestate,posn,type):
        self.name = name
        self.gamestate = gamestate
        self.posn = posn
        self.type = type


    """
    update the level information to this adversary
    gamestate: GameState
    """
    def update_level(self, gamestate):
        self.gamestate = gamestate

    """
    decide a movement according to current level map information, return
    a position of tuple style. An adversary should always moving towards the
    closest player. return a list of desination positions in the order of best movement
    to lease efficient movement.
    """
    def decide_move(self):
        dest = self.find_cloest()
        current = copy.deepcopy(self.posn)
        up = (current[0],current[1] - 1)
        down = (current[0],current[1] + 1)
        right = (current[0]+1,current[1])
        left = (current[0]-1,current[1])
        result = None
        if dest[0] > current[0]:
            if dest[1] > current[1]:
                result = [right, down, up, left]
            elif dest[1] < current[1]:
                result = [right, up, down, left]
            else:
                result = [right, left, up, down]
        elif dest[0] < current[0]:
            if dest[1] > current[1]:
                result = [left, down, up, right]
            elif dest[1] < current[1]:
                result = [left, up, down, right]
            else:
                result = [left, right, up, down]
        else:
            if dest[1] > current[1]:
                result = [down, up, right, right]
            elif dest[1] < current[1]:
                result = [up, down, right, right]
            else:
                result = [up, down, right, right]
        return result

    """
    Go through all the player information, return the closest player position to
    this adversary.
    """
    def find_cloest(self):
        posns = self.gamestate.getPlayerPosns()
        init = posns[0]
        dest = self.posn
        distance = (init[0] - dest[0])**2 + (init[1] - dest[1])**2
        result = posns[0]
        for p in posns:
            if distance > (p[0] - self.posn[0])**2 + (p[1] - self.posn[1])**2:
                result = p
                distance = (p[0] - self.posn[0])**2 + (p[1] - self.posn[1])**2
        return result

    """
    request a movement to the given game GameManager.
    gamemanager: GameManager
    dest: destination in tuple style
    """
    def request_move(self, gamemanager):
        posn = self.decide_move()
        for p in posn:
            newState = gamemanager.move_adversary(self.name, p)
            if not newState == "please re-enter movement":
                self.update_posn(p)
                return
        # in case four posns are all invalid movement, adversary should stay
        return gamemanager.move_adversary(self.name, None)

    def request_interaction(self, manager):
        dest = self.posn
        return manager.adversary_interaction(dest)

    """
    update the new position of this adversary
    posn: position of tuple style
    """
    def update_posn(self, posn):
        self.posn = posn
