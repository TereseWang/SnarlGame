#!/usr/bin/python3
#from player import PlayerInterface
import pygame
import sys
import src.parse_json as pj
import src.testManager as tm
import src.testLevel as tl
import json
from src.state.gamestate import GameState
from src.manager.gameManager import GameManager
from src.player.LocalPlayer import Player
from src.adversary.adversaryComponent import AdversaryComponent
import copy

"""
localSnarl that store the information of a snarl game and handles functionality
of rendering and playing the game
"""
class localSnarl():
    def __init__(self, numplayers, levels, observer, start):
        self.totalPlayers = numplayers
        self.playerRecord = {}
        self.user_interface = True
        self.numplayers = numplayers
        self.manager = None
        self.levels = levels
        self.exited = False
        self.observer = observer
        self.currentLevel = start - 1
        self.players = {}
        self.currentPlayer = 0
        self.numMoves = 0
        self.status = "process"
        self.message = ""
        self.exited = 0
        self.adlist = []
        self.turn = "p"
        self.leaderBoard = {}

    """
    run the actual snarl game
    """
    def run_pygame(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode([1200, 800])
        user_input = ""
        player = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                """prompt user to enter user name """
                if self.user_interface:
                    user_input = self.handle_user_input(event, user_input)
                #player's round to move
                elif self.turn == "p":
                    player = self.handle_player_input(event, player)
                #adversary's round to move
                elif self.turn == "a" and self.numplayers != 0:
                    self.handle_adversary(event, player)

            """ prompt user to enter user name interface """
            if self.user_interface:
                self.run_user_interface(screen, user_input)
            # actual playing interface
            elif self.status == "process":
                screen.fill((0, 0, 0))
                player = list(self.players.values())[self.currentPlayer]
                self.run_player_interface(screen, player)
                pygame.display.flip()
            #win lose interface
            else:
                screen.fill((0, 0, 0))
                self.run_game_end_interface(screen)
                pygame.display.flip()

    """
    prompt user to enter user name in order to start the game, if the user
    enter the return key or click the button, store the name, else continue
    also initialize the game state until we have enough users to start the game

    user_input: string, the current text the user is typing
    event: pygame event
    """
    def handle_user_input(self, event, user_input):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[0:-1]
            elif event.key == pygame.K_RETURN and self.check_name(user_input):
                if len(self.players) == self.numplayers - 1:
                    self.user_interface = False
                    self.players[user_input] = None
                    self.playerRecord[user_input] = None
                    self.manager = self.init_state()
                    for name in self.name_list():
                        self.leaderBoard[name] = {"exit": 0, "key": 0}
                else:
                    self.players[user_input] = None
                    self.playerRecord[user_input] = None
                    user_input = ""
            elif len(user_input) < 10:
                user_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            button = pygame.Rect(500, 500, 200, 80)
            if button.collidepoint(mouse_pos) and self.check_name(user_input):
                if len(self.players) == self.numplayers - 1:
                    self.user_interface= False
                    self.players[user_input] = None
                    self.manager = self.init_state()
                else:
                    self.players[user_input] = None
                    user_input = ""
        return user_input

    """
    handles player movement
    let user to choose a position to move, if the movement is invalid
    return to the initial state and ask for reenter of the movement, if
    user clicked enter, the movement will be sent to manager to be evaluated
    if it is valid, movement will be made and move to next player in turn
    event: the pygame event
    player: the current player in turn, Player class in LocalPlayer.py
    """
    def handle_player_input(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                result = self.manager
                if self.origin != player.posn:
                    result = player.request_move(self.manager, player.posn)

                if result == "please re-enter movement":
                    self.numMoves = 0
                    player.posn =  self.origin
                    self.message = "Invalid Move, Try Again"
                else:
                    interaction = player.request_interaction(self.manager, player.posn)
                    self.handle_interaction(interaction, player, result)

            elif event.key == pygame.K_DOWN:
                self.message = ""
                posn = player.posn
                self.handle_move(player, (posn[0], posn[1]+1))
            elif event.key == pygame.K_UP:
                self.message = ""
                posn = player.posn
                self.handle_move(player, (posn[0], posn[1]-1))
            elif event.key == pygame.K_LEFT:
                self.message = ""
                posn = player.posn
                self.handle_move(player, (posn[0]-1, posn[1]))
            elif event.key == pygame.K_RIGHT:
                self.message = ""
                posn = player.posn
                self.handle_move(player, (posn[0]+1, posn[1]))

            if self.status == "process":
                player = list(self.players.values())[self.currentPlayer]
        return player

    """
    handles adversary movement
    event: pygame event
    player: current player in turn, for here this will be the last player
    in last player round, this will be player component class
    """
    def handle_adversary(self, event, player):
        for ad in self.adlist:
            if self.numplayers != 0:
                ad.request_move(self.manager)
                interaction = ad.request_interaction(self.manager)
                if interaction != "ok":
                    name = interaction
                    self.message = "Player " + name + " was expelled."
                    del self.players[name]
                    self.numplayers = self.numplayers - 1
                    if self.numplayers == 1:
                        self.currentPlayer = 0
                    if self.numplayers == 0:
                        self.handleLevelEnd()
                    else:
                        player = list(self.players.values())[self.currentPlayer]
                        self.origin = copy.deepcopy(player.posn)
                self.adlist = self.manager.handleAdversary()
        self.turn = "p"

    """
    render the view that prompt the user to enter the user name and start the
    game
    user_input: string, current text that user is entering
    """
    def run_user_interface(self, screen, user_input):
        screen.fill((0, 0, 0))
        color = pygame.Color((255, 255, 255))
        input_rect = pygame.Rect(500, 450, 200, 50)

        img = pygame.image.load("./src/observer/images/bg.jpg").convert_alpha()
        img = pygame.transform.scale(img, (1200, 800))
        screen.blit(img, [0, 0])

        title = pygame.image.load("./src/observer/images/crawl.png").convert_alpha()
        title = pygame.transform.scale(title, (800, 200))
        screen.blit(title, [200, 150])

        pygame.draw.rect(screen, color, input_rect, 2)
        base_font = pygame.font.Font(None, 50)
        text_surface = base_font.render(user_input, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        base_font = pygame.font.Font(None, 30)
        text_surface = base_font.render('"Enter Name To Start"', True, (255, 255, 255))
        screen.blit(text_surface, (500, 420))

        playbutton = pygame.image.load("./src/observer/images/play.png").convert_alpha()
        playbutton = pygame.transform.scale(playbutton, (200, 80))
        screen.blit(playbutton, [500, 500])

        index = 0
        base_font = pygame.font.Font(None, 40)
        for name in self.players.keys():
            name = "player: " + name + " joined"
            names_surface = base_font.render(name, True, (255, 255, 255))
            screen.blit(names_surface, (500, 600 + index))
            index += 40
        pygame.display.flip()

    """
    render the player view, if it is observer view render the whole map, else
    just render the 5*5 tiles surround the current player
    """
    def run_player_interface(self, screen, player):
        gamestate = self.manager.returnGameState()
        namelist = self.name_list()
        name = list(namelist.keys())[self.currentPlayer]
        if self.observer:
            player.renderObView(self.manager, self.players)
            img = pygame.image.load("./src/observer/images/posn.png").convert_alpha()
            img = pygame.transform.scale(img, (30, 15))
            screen.blit(img, [((player.posn[0] - 1) * 40), (player.posn[1] * 40) + 20])

        else:
            player.renderView(self.manager, self.players)
            img = pygame.image.load("./src/observer/images/posn.png").convert_alpha()
            img = pygame.transform.scale(img, (130, 25))
            screen.blit(img, [460, 420])

            base_font = pygame.font.Font(None, 40)
            movetitle = name + " move to..."
            names_surface = base_font.render(movetitle, True, (255, 255, 255))
            screen.blit(names_surface, (460, 360))

        index = 0
        base_font = pygame.font.Font(None, 60)
        names_surface = base_font.render("Player List", True, (255, 255, 255))
        screen.blit(names_surface, (950, 50+index))
        index += 60

        for n in namelist:
            if name == n:
                base_font = pygame.font.Font(None, 50)
                n = n + "'s turn"
                names_surface = base_font.render(n, True, (255, 0, 0))
                screen.blit(names_surface, (950, 50 + index))
                index += 50
            else :
                base_font = pygame.font.Font(None, 40)
                names_surface = base_font.render(n, True, (255, 255, 255))
                screen.blit(names_surface, (950, 50 + index))
                index += 40
                base_font = pygame.font.Font(None, 60)
                names_surface = base_font.render("Exit Status", True, (255, 255, 255))
                screen.blit(names_surface, (950, 300))

        if gamestate.getUnlock():
            base_font = pygame.font.Font(None, 40)
            names_surface = base_font.render("UnLocked", True, (0, 255, 0))
            screen.blit(names_surface, (950, 360))
        else:
            base_font = pygame.font.Font(None, 40)
            names_surface = base_font.render("Locked", True, (255, 0, 0))
            screen.blit(names_surface, (950, 360))
            base_font = pygame.font.Font(None, 50)
            text_surface = base_font.render(self.message, True, (255, 0, 0))
            screen.blit(text_surface, (300, 100))
        pygame.display.flip()

    """
    render the message telling the user whether they has lose or win the game
    and also render the leaderboard
    screen: pygame screen to render the view
    """
    def run_game_end_interface(self, screen):
        base_font = pygame.font.Font(None, 80)
        if self.status == "lose":
            text_surface = base_font.render('You Lose!', True, (255, 255, 255))
        else:
            text_surface = base_font.render('You Win!', True, (255, 255, 255))
        screen.blit(text_surface, (450, 100))

        index = 80
        base_font = pygame.font.Font(None, 60)
        for key, value in self.leaderBoard.items():
            text = key + ": Exited "+ str(value["exit"]) + " times, Keys Found " + str(value["key"]) + " times."
            text_surface = base_font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (200, 100 + index))
            index += 60

    """
    initialize a game manager to play the game and other
    """
    def init_state(self):
        level = self.levels[self.currentLevel]
        objects = level['objects']
        level = tl.handleLevel([level])
        gamestate = GameState(level, {}, {})
        players = gamestate.generatePlayer(self.totalPlayers)
        for object in objects:
            type = object['type']
            posn = object['position']
            posn = (posn[1], posn[0])
            gamestate.placeObject(type, posn)
        ads = gamestate.generateAdversary(self.currentLevel + 1)
        self.players = self.handlePlayers(list(self.players.keys()), players)
        self.playerRecord = self.handlePlayers(list(self.players.keys()), players)
        self.origin = copy.deepcopy(list(self.players.values())[self.currentPlayer].posn)
        manager = GameManager(list(self.players.keys()), level, 1000, ads, players)
        self.adlist = manager.handleAdversary()
        return manager

    """
    given an interaction and updating the game state according to the interaction
    if the interaction is ok, move to next player
    if the interaction is eject, eject the current player and move to next in turn
    same of exited, if the user found the key, update the unlock
    """
    def handle_interaction(self, interaction, player, result):
        self.manager = result
        self.numMoves = 0
        if interaction == "Eject":
            self.message = "Player " + player.name + " was expelled."
            del self.players[player.name]
            self.numplayers = self.numplayers - 1
            if self.numplayers == 1 or self.currentPlayer > self.numplayers - 1:
                self.currentPlayer = 0
                self.turn = "a"
            if self.numplayers == 0:
                self.handleLevelEnd()
            else:
                player = list(self.players.values())[self.currentPlayer]
                self.origin = copy.deepcopy(player.posn)
        elif interaction == "Key":
            self.message = "Player " + player.name + " found the key."
            self.leaderBoard[player.name]["key"] += 1
            if self.currentPlayer < self.numplayers - 1:
                self.currentPlayer += 1
            else:
                self.currentPlayer = 0
                self.turn = "a"
            player = list(self.players.values())[self.currentPlayer]
            self.origin = copy.deepcopy(player.posn)
        elif interaction == "Exit":
            self.message = "Player " + player.name + " exited."
            self.leaderBoard[player.name]["exit"] += 1
            del self.players[player.name]
            self.numplayers = self.numplayers - 1
            self.exited+=1
            if self.numplayers == 1 or self.currentPlayer > self.numplayers - 1:
                self.currentPlayer = 0
                self.turn = "a"
            if self.numplayers == 0:
                self.handleLevelEnd()
            else:
                player = list(self.players.values())[self.currentPlayer]
                self.origin = copy.deepcopy(player.posn)
        else:
            if self.currentPlayer < self.numplayers - 1:
                self.currentPlayer += 1
            else:
                self.currentPlayer = 0
                self.turn = "a"
            player = list(self.players.values())[self.currentPlayer]
            self.origin = copy.deepcopy(player.posn)

    """
    register the players into a dictionary with key to be the player name
    and value be the player component
    namelist: a list of player name
    posnlist: a list of posns to be given to the players
    """
    def handlePlayers(self, namelist, posnlist):
        result = {}
        for index in range(0, len(namelist)):
            player = Player(namelist[index], index, posnlist[index])
            result[namelist[index]] = player
        return result

    """
    restrict the tiles that can be chosen by player and update the movement
    for the player list
    player: player component, the current player in turn
    dest: the destination that user want to move to
    """
    def handle_move(self, player, dest):
        origin = copy.deepcopy(self.origin)
        distance = (origin[0] - dest[0])**2 + (origin[1] - dest[1])**2
        if distance <= 4:
            self.players[player.name] = player.move(dest)
            posn = player.posn
            self.numMoves = distance

    """
    update the state when the level end
    """
    def handleLevelEnd(self):
        if self.currentLevel == len(self.levels) - 1:
            if self.exited == 0:
                self.status = "lose"
            else:
                self.status = "win"
        else:
            if self.exited == 0:
                self.status = "lose"
            else:
                self.numplayers = self.totalPlayers
                self.manager = None
                self.currentLevel = self.currentLevel + 1
                self.players = copy.deepcopy(self.playerRecord)
                self.currentPlayer = 0
                self.numMoves = 0
                self.message = "Level " + str(self.currentLevel)
                self.exited = 0
                self.manager = self.init_state()

    """
    check if the user name entered is valid
    """
    def check_name(self, name):
        if len(name) <= 1:
            return False
        else:
            try:
                self.players[name]
                return False
            except KeyError:
                return True

    """
    return the name list of players that is in play
    """
    def name_list(self):
        result = {}
        index = 0
        for player in self.players.keys():
            result[player] = index
            index += 1
        return result

if __name__ == '__main__':
    levels = "snarl.levels"
    players = 1
    start = 1
    observer = False
    for index in range (1, len(sys.argv)):
        argv = sys.argv[index]
        if argv in "--levels":
            levels = sys.argv[index+1]
        elif argv in "--players":
            players = int(sys.argv[index+1])
        elif argv in "--start":
            start = int(sys.argv[index+1])
        elif argv in "--observe":
            observer = True

    with open(levels) as json_file:
        data = json_file.read()
        numlevels = int(data.split("\n", 1)[0])
        data = data.split("\n", 1)[1]
        data = pj.parse_to_json(data)
        localSnarl = localSnarl(players, data, observer, start)
        localSnarl.run_pygame()
