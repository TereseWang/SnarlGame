#!/usr/bin/python3
import socket
import pickle as pickle
import sys
#from player import PlayerInterface
import pygame
import sys
import src.testManager as tm
import src.testLevel as tl
import src.parse_json as pj
import json
from src.state.gamestate import GameState
from src.manager.gameManager import GameManager
from src.player.LocalPlayer import Player
from src.adversary.adversaryComponent import AdversaryComponent
import copy

"""
The client for the Snarl game. A client is able to connect to the game server
and render the view for players after the game starts.
"""
class snarlClient:
    def __init__(self, server):
        """
        Constructor arguments:
        @param  server:    Network, TCP connection server
        """
        self.name = ""
        self.server = server
        self.user_interface = True
        self.playerRecord = {}
        self.players = {}
        self.joined = False
        self.turn = ""
        self.status = "process"
        self.currentPlayer = 0
        self.id = 0
        self.view = None
        self.namelist = []
        self.message = ""
        self.unlock = False
        self.origin = None
        self.numMoves = 0
        self.leaderBoard = {}
        self.currentLevel = 0

    """
    run the pygame. Interact with the user according  current game state
    and turn.
    """
    def run_pygame(self):
        reply = self.server.connect()
        self.update_server_reply(reply)
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode([1200, 800])
        user_input = ""
        player = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.server.disconnect()
                    sys.exit()
                    pygame.quit()

                """
                Communicate with the client. Let the players and adversaries
                move in turn. Update all the infrmation.
                """
                if self.user_interface:
                    user_input = self.handle_user_input(event, user_input)
                elif self.name == self.turn and self.status == "process":
                    if self.origin == None:
                        self.origin = self.players[self.name].posn
                    reply = self.server.send("update")
                    self.update_server_reply(reply)
                    player = self.handle_player_input(event, player)
                elif self.status != "win" and self.status != "lose":
                    reply = self.server.send("update")
                    self.update_server_reply(reply)

                """
                Handles several rendering cases during the game.
                """
                if self.user_interface:
                    reply = self.server.send("update")
                    self.update_server_reply(reply)
                    self.run_user_interface(screen, user_input)
                elif self.status == "process" and self.players[self.name].expeled:
                    screen.fill((0, 0, 0))
                    base_font = pygame.font.Font(None, 40)
                    text_surface = base_font.render('Wait For Other Player to Finish', True, (255, 255, 255))
                    screen.blit(text_surface, (500, 420))
                    pygame.display.flip()
                # Render the Name inforamtion of this player
                elif self.status == "process" and self.name != "" and self.name in self.players.keys():
                    screen.fill((0, 0, 0))
                    player = list(self.players.values())[self.currentPlayer]
                    self.run_player_interface(screen, player)
                    base_font = pygame.font.Font(None, 40)
                    text_surface = base_font.render('You Are ' + self.name, True, (255, 255, 255))
                    screen.blit(text_surface, (500, 50))
                    pygame.display.flip()
                # render the view for players failed to join before the start of the game
                elif self.status == "process" and self.name == "":
                    screen.fill((0, 0, 0))
                    base_font = pygame.font.Font(None, 30)
                    text_surface = base_font.render('Game Has Already Started', True, (255, 255, 255))
                    screen.blit(text_surface, (500, 420))
                    pygame.display.flip()
                # render the view for players that have been expelled
                else:
                    screen.fill((0, 0, 0))
                    self.run_game_end_interface(screen)
                    pygame.display.flip()

        self.server.disconnect()


    """
    Handles user input. Catches all the key input to register users.
    Checks for the limited timer and number of players. After the user
    typing in their user name, listen to the mouse click on "load" button
    to start player registration.
    @type       event:      pygame event
    @param      event:      user key input caught by pygame
    @type  user_input:      String
    @param user_input:      the input of user
    @rtype:                 String
    @return:                the user input
    """
    def handle_user_input(self, event, user_input):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[0:-1]
            elif event.key == pygame.K_RETURN:
                self.name = user_input
                reply = self.server.send("name: " + self.name)
                self.update_server_reply(reply)
            elif len(user_input) < 10:
                user_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            button = pygame.Rect(500, 500, 200, 80)
            if button.collidepoint(mouse_pos):
                self.name = user_input
                reply = self.server.send("name: " + self.name)
                self.update_server_reply(reply)
        return user_input

    """
    handles player movement
    let user to choose a position to move, if the movement is invalid
    return to the initial state and ask for reenter of the movement, if
    user clicked enter, the movement will be sent to manager to be evaluated
    if it is valid, movement will be made and move to next player in turn
    @type       event:      pygame event
    @param      event:      user key input caught by pygame
    @type      player:      LocalPlayer Component
    @param     player:      current player in turn
    @rtype:                 LocalPlayer Component
    @return:                current player in turn
    """
    def handle_player_input(self, event, player):
        player = self.players[self.name]
        if event.type == pygame.KEYDOWN:
            """
            Request a actual move after the user hits "enter". Catch the reaply
            from server and interact with the user.
            """
            if event.key == pygame.K_RETURN:
                player = self.players[self.name]
                resp = self.server.send([list(player.posn), list(self.origin)], pick=True)
                resp = self.server.send("update")

                self.update_server_reply(resp)
                if self.status == "process":
                    if resp[10] == "Invalid":
                        self.numMoves = 0
                        self.message = "Invalid Move, Please Enter Again"
                        print(self.message)
                    elif "Level" in resp[10]:
                        self.unlock = False
                        print(resp)
                        print("next level")
                        print(self.status)
                        self.origin = self.players[self.name].posn
                    else:
                        self.origin = self.players[self.name].posn
            elif event.key == pygame.K_DOWN:
                print("typed here")
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
    restrict the tiles that can be chosen by player and update the movement
    for the player list
    @type      player:      LocalPlayer Component
    @param     player:      current player in turn
    @type        dest:      tuple of int
    @param       dest:      destination of player's movement
    """
    def handle_move(self, player, dest):
        if self.origin == None:
            self.origin = copy.deepcopy(player.posn)
        origin = copy.deepcopy(self.origin)
        distance = (origin[0] - dest[0])**2 + (origin[1] - dest[1])**2
        if distance <= 4:
            self.players[player.name] = player.move(dest)
            reply = self.server.send(self.players, pick=True)
            self.update_server_reply(reply)
            posn = player.posn
            self.numMoves = distance

    """
    render the message telling the user whether they has lose or win the game
    and also render the leaderboard
    @type   screen:     pygame screen
    @param  screen:     screen where all game info is rendered
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
    render the player view, if it is observer view render the whole map, else
    just render the 5*5 tiles surround the current player
    @type   screen:     pygame screen
    @param  screen:     screen where all game info is rendered
    @type      player:      LocalPlayer Component
    @param     player:      current player in turn
    """
    def run_player_interface(self, screen, player):
        namelist = self.namelist
        name = self.turn
        player.renderView(self.view, self.players)

        """
        sets up the circle that marks up the desination of current movement.
        """
        if self.turn == self.name:
            img = pygame.image.load("src/observer/images/posn.png").convert_alpha()
            img = pygame.transform.scale(img, (130, 25))
            screen.blit(img, [460, 420])
            base_font = pygame.font.Font(None, 40)
            movetitle = name + " move to..."
            names_surface = base_font.render(movetitle, True, (255, 255, 255))
            screen.blit(names_surface, (460, 360))

        """
        Renders the player list and current turn.
        """
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
                if self.players[n].expeled:
                    names_surface = base_font.render(n + " expelled", True, (255, 255, 255))
                else:
                    names_surface = base_font.render(n, True, (255, 255, 255))
                screen.blit(names_surface, (950, 50 + index))
                index += 40
                base_font = pygame.font.Font(None, 60)

        """
        Render all game inforamtion.
        """
        names_surface = base_font.render("Exit Status", True, (255, 255, 255))
        screen.blit(names_surface, (950, 300))

        names_surface = base_font.render("Level: " + str(self.currentLevel + 1), True, (255, 255, 255))
        screen.blit(names_surface, (100, 100))

        if self.unlock:
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
    Render the player registration UI. Updating all the newly registerd players.
    @type      screen:      pygame screen
    @param     screen:      screen where all game info is rendered
    @type  user_input:      String
    @param user_input:      the input of user
    """
    def run_user_interface(self, screen, user_input):
        screen.fill((0, 0, 0))
        color = pygame.Color((255, 255, 255))
        input_rect = pygame.Rect(500, 450, 200, 50)

        img = pygame.image.load("src/observer/images/bg.jpg").convert_alpha()
        img = pygame.transform.scale(img, (1200, 800))
        screen.blit(img, [0, 0])

        title = pygame.image.load("src/observer/images/crawl.png").convert_alpha()
        title = pygame.transform.scale(title, (800, 200))
        screen.blit(title, [200, 150])

        """
        Render the view for a new player to register
        """
        if not self.joined:
            pygame.draw.rect(screen, color, input_rect, 2)
            base_font = pygame.font.Font(None, 50)
            text_surface = base_font.render(user_input, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            base_font = pygame.font.Font(None, 30)
            text_surface = base_font.render('"Enter Name To Start"', True, (255, 255, 255))
            screen.blit(text_surface, (500, 420))

            playbutton = pygame.image.load("src/observer/images/play.png").convert_alpha()
            playbutton = pygame.transform.scale(playbutton, (200, 80))
            screen.blit(playbutton, [500, 500])

        """
        Render the list of joined players
        """
        index = 0
        base_font = pygame.font.Font(None, 40)
        for name in self.players.keys():
            name = "player: " + name + " joined"
            names_surface = base_font.render(name, True, (255, 255, 255))
            screen.blit(names_surface, (500, 600 + index))
            index += 40
        pygame.display.flip()


    """
    Keep track of server reply. Listen to the reply and update all the data in
    this client.
    @type   reply:      tuple
    @param  reply:      the reply from server
    """
    def update_server_reply(self, reply):
        if type(reply) == tuple:
            self.players = reply[0]
            self.user_interface = reply[1]
            self.turn = reply[2]
            self.status = reply[3]
            self.playerRecord = reply[4]
            self.currentPlayer = reply[5]
            self.id = reply[6]
            self.view = reply[7]
            self.namelist = reply[8]
            self.unlock = reply[9]
            if reply[10] == "joined":
                self.joined = True
            self.leaderBoard = reply[11]
            self.currentLevel = reply[12]
        else:
            print(reply)

"""
This class works to connect the Client and Server. It sets up the ip address
and port to start the TCP connection.
"""
class Network:
    def __init__(self, ip, port):
        """
        Constructor arguments:
        :param  address:    String, IP address
        :param  port:       int, port
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip
        self.port = port
        self.addr = (self.host, self.port)

    """
    connect the client to the stored ip address. Return the string massage
    of the connection result.
    @rtype:           tuple
    @return:          reply from the server
    """
    def connect(self):
        self.client.connect(self.addr)
        message = self.send("connected")
        return message

    """
    close the connection and return the string message of result.
    """
    def disconnect(self):
        self.send("disconnect")
        self.client.close()


    """
    try to send updates from this client to the server, catch the error
    and print all expections in terminal.
    @type    data:    bytes
    @param   data:    data need to send to the Server
    @type    pick:    boolean
    @param   pick:    whether it is pickled or unpickled
    @rtype:           tuple
    @return:          reply from the server
    """
    def send(self, data, pick=False):
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048)
            try:
                reply = pickle.loads(reply)
                return reply
            except Exception as e:
                print(e)
            return reply
        except socket.error as e:
            print(e)

if __name__ == '__main__':
    address = "127.0.0.1"
    port = 45678
    for index in range (1, len(sys.argv)):
        argv = sys.argv[index]
        if argv in "--address":
            address = sys.argv[index+1]
        elif argv in "--port":
            port = int(sys.argv[index+1])
    server = Network(address, port)
    game = snarlClient(server)
    game.run_pygame()
