from abc import ABC, abstractmethod
import os.path
# Import the pygame module
import pygame

from src.state.room import Room
from src.state.hallway import Hallway
from src.state.level import SnarlLevel
from src.state.gamestate import Player, Adversary, GameState
from src.observer.observer import ObserverInterface


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


class Observer(ObserverInterface):
    """
    wid: int
    height: int
    """
    def __init__(self, wid, height):
        self.screen = pygame.display.set_mode((wid, height))
        self.screen.fill((0, 0, 0))

    """
    renders the given map
    map: 2D array List of cells
    width: number, the width of each tile to render
    namelist: the list of player names
    observe: boolean, indicating whether this is a observer mode or player mode
    """
    def renderHelper(self, map, width, namelist, observe):
        WALL = pygame.image.load("src/observer/images/wall.jpg").convert_alpha()
        WALL = pygame.transform.scale(WALL, (width, width))
        ROAD = pygame.image.load("src/observer/images/road.jpg").convert_alpha()
        ROAD = pygame.transform.scale(ROAD, (width, width))

        role = []
        ROLE = pygame.image.load("src/observer/images/role.png").convert_alpha()
        ROLE = pygame.transform.scale(ROLE, (int(width*0.9), int(width*0.9)))
        role+=[ROLE]
        ROLE1 = pygame.image.load("src/observer/images/role2.png").convert_alpha()
        ROLE1 = pygame.transform.scale(ROLE1, (int(width*0.7), width))
        role+=[ROLE1]
        ROLE2 = pygame.image.load("src/observer/images/role3.png").convert_alpha()
        ROLE2 = pygame.transform.scale(ROLE2, (int(width*0.7), int(width*0.9)))
        role+=[ROLE2]
        ROLE3 = pygame.image.load("src/observer/images/role4.png").convert_alpha()
        ROLE3 = pygame.transform.scale(ROLE3, (width, int(width*0.9)))
        role+=[ROLE3]

        ZOMBIE = pygame.image.load("src/observer/images/zombie.png").convert_alpha()
        ZOMBIE = pygame.transform.scale(ZOMBIE, (width, width))
        GHOST = pygame.image.load("src/observer/images/ghost.png").convert_alpha()
        GHOST = pygame.transform.scale(GHOST, (width, width))
        KEY = pygame.image.load("src/observer/images/key.png").convert_alpha()
        KEY = pygame.transform.scale(KEY, (width, width))
        EXIT = pygame.image.load("src/observer/images/exit.png").convert_alpha()
        EXIT = pygame.transform.scale(EXIT, (width, width))
        x = width
        y = 0
        for row in map:
            rowString = ""
            for cell in row:
                if cell == "x":
                    self.screen.blit(WALL, (x, y))
                elif type(cell) != tuple:
                    self.screen.blit(ROAD, (x, y))

                if cell == "z":
                    self.screen.blit(ZOMBIE, (x, y))
                elif cell == "g":
                    self.screen.blit(GHOST, (x, y))

                if cell == "k":
                    self.screen.blit(KEY, (x, y))
                elif cell == "e":
                    self.screen.blit(EXIT, (x, y))

                if cell in namelist:
                    numIndex = namelist[cell].turn
                    self.screen.blit(role[numIndex], (x, y))
                    if observe:
                        base_font = pygame.font.Font(None, 20)
                        names_surface = base_font.render(cell, True, (255, 255, 255))
                        self.screen.blit(names_surface, (x, y))
                    else:
                        base_font = pygame.font.Font(None, 40)
                        names_surface = base_font.render(cell, True, (255, 255, 255))
                        self.screen.blit(names_surface, (x, y))

                x += width
            y += width
            x = width
        return self.screen

    # overriding abstract method
    def renderMap(self, map, namelist):
        return self.renderHelper(map, 40, namelist, True)

    # overriding abstract method
    def renderLevelPlayerView(self, map, posn, namelist):
        return self.renderHelper(map, 150, namelist, False)
