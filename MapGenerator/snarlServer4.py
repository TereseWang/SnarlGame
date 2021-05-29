#!/usr/bin/python3
import socket
from _thread import *
import pickle
import time
import sys
import src.parse_json as pj
import src.testLevel as tl
import json
from threading import Timer,Thread,Event
from src.state.gamestate import GameState
from src.manager.gameManager import GameManager
from src.player.LocalPlayer import Player
from src.adversary.adversaryComponent import AdversaryComponent
import copy
#from player import PlayerInterface
import pygame
from snarlGen import SnarlLevelGenerator

"""
Snarl Server component that will display images and keep track of the information
for this client
"""
class snarlServer:
    """
    Constructor
    @type address: String
    @param address: the ip address to connect to
    @type port: Number
    @param port: The port number socket connect to
    @type levels: Json Value
    @param levels: stored map
    @type observer: boolean
    @param observer: whether it is observer mod
    @type wait: Number
    @param wait: the number of seconds to wait to start the game
    @type totalLevel: Number
    @param totalLevel: the number of levels for this game
    """
    def __init__(self, address, port, numplayers, levels, observer, wait, generate, totalLevel):
        self.port = port
        self.ip = address
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = 0
        self._id = 0
        self.numplayers = numplayers
        self.levels = levels
        self.observer = observer
        self.wait = wait
        self.playerRecord = {}
        self.players = {}
        self.user_interface = True
        self.turn = "p"
        self.namelist = []
        self.playerMap = {}
        self.status = "process"
        self.totalPlayers = numplayers
        self.currentLevel = 0
        self.currentPlayer = 0
        self.thread = Timer(self.wait, self.end_timer)
        self.manager = None
        self.adlist = []
        self.unlock = False
        self.message = ""
        self.leaderBoard = {}
        self.exited = 0
        self.generate = generate
        self.totalLevel = totalLevel
        self.tempNameList = None

    """
    when the time has passed, or user has waited enough time, initilize the game
    state and start the game
    @rtype: None
    @return: None
    """
    def end_timer(self):
        self.user_interface = False
        self.manager = self.init_state()
        self.user_interface = False
        for name in self.namelist:
            self.leaderBoard[name] = {"exit": 0, "key": 0}
        self.message = ""
        self.thread = None

    """
    To create multiple threads in order to updata for players concurrently
    @rtype: None
    @return: None
    """
    def play_game(self):
        self.bind_server()
        while True:
            if self.thread and self.thread.is_alive() and len(self.namelist) < self.totalPlayers:
                self.thread.cancel()
                self.thread = Timer(self.wait, self.end_timer)
            elif len(self.namelist) < self.totalPlayers:
                self.thread == None

            host, addr = self.s.accept()
            print("Connected to", addr)
            self.message = ""
            if len(self.namelist) < self.totalPlayers:
                start_new_thread(self.threaded_client, (host, self._id))

    """
    bind to the server
    @rtype: None
    @return: None
    """
    def bind_server(self):
        try:
            self.s.bind((self.ip, self.port))
            self.s.listen(5)
        except socket.error as e:
            print(e)
            quit()

    """
    single thread that handles game for each single player
    @type conn: socket connection
    @param conn: the socket connection
    @type _id: Number
    @param _id: thread id for the current threaded player
    """
    def threaded_client(self, conn, _id):
        name = ""
        data = conn.recv(16)
        if data.decode("utf-8") == "connected":
            conn.send(self.player_data(_id, name))
        while True:
            if self.status == "win" or self.status == "lose":
                conn.send(self.player_data(_id, name))
                break
            if self.turn == "adversary":
                self.handle_adversary(conn)
                send_data = self.player_data(_id, name)
            else:
                data = conn.recv(1024)
                try:
                    data = data.decode("utf-8")
                except Exception:
                    data = pickle.loads(data)

                if type(data) == dict:
                    self.players = data
                    send_data = self.player_data(_id, name)
                elif type(data) == list:
                    if self.observer:
                        print("moved to")
                        print(data)
                    dest = data[0]
                    origin = data[1]
                    dest = (dest[0], dest[1])
                    origin = (origin[0], origin[1])
                    self.handle_user_movement(dest, origin, _id, conn, name)
                elif "update" == data:
                    self.message = ""
                    send_data = self.player_data(_id, name)
                elif data == "disconnect":
                    break
                elif "name: " in data and self.check_name(data[5:]):
                    self.message = ""
                    name = data[6:]
                    self.handle_name(data, conn, _id)
                conn.send(send_data)
        self.handle_user_quiting(conn, _id, name)
        return None
    """
    the data that combined into a tuple and turn into byte data type in order
    to be ready to sent back to the user
    @type _id: Number
    @param _id: the thread id of this player
    @type name: String
    @param name: the name of the player to send the data in string format
    @rtype: Decode value of tuple
    @return: the decoded value of the data to be sent to client
    """
    def player_data(self, _id, name):
        current_player_name = self.turn
        message = self.message
        map = None
        if self.manager and self.status == "process":
            player = self.players[name]
            try:
                self.playerMap[name] = self.manager.renderAround(player.posn)
                map = self.playerMap[name]
            except KeyError:
                pass
            if self.turn != "adversary":
                current_player_name = self.tempNameList[self.currentPlayer]

        return pickle.dumps((self.players,
                             self.user_interface,
                             current_player_name,
                             self.status,
                             self.playerRecord,
                             self.currentPlayer,
                             _id,
                             map,
                             self.tempNameList,
                             self.unlock,
                             message,
                             self.leaderBoard,
                             self.currentLevel))

    """
    handles adversary movement
    @type conn: socket connection
    @param conn: the socket connection
    @rtype: None
    @return: None
    """
    def handle_adversary(self, conn):
        for ad in self.adlist:
            if self.numplayers != 0:
                ad.request_move(self.manager)
                interaction = ad.request_interaction(self.manager)
                if interaction != "ok":
                    name = interaction
                    self.tempNameList.remove(name)
                    self.players[name].expeled = True
                    self.numplayers = self.numplayers - 1
                    if self.numplayers == 1:
                        self.currentPlayer = 0
                    elif self.numplayers == 0:
                        self.handleLevelEnd()
                self.adlist = self.manager.handleAdversary()
        if len(self.tempNameList) != 0:
            self.turn = self.tempNameList[self.currentPlayer]
        elif len(self.tempNameList) == 0:
            self.handleLevelEnd()

    """
    handle player movement, call the manager to move the player and return
    corresponding message as needed
    @type dest: tuple of two number, (number, number)
    @param dest: the position that player is about to move to
    @type origin: tuple of two number, (number, number)
    @param origin: tuple, the original position that player located
    @type _id: Number
    @param _id: the thread id of current player
    @type conn: socket connection
    @param conn: the socket connection port to send the data
    @type name: String
    @param name: the name of the player
    """
    def handle_user_movement(self, dest, origin, _id, conn, name):
        player = self.players[self.tempNameList[self.currentPlayer]]
        result = None
        if origin[0] != dest[0] or origin[1] != dest[1]:
            result = player.request_move(self.manager, dest)

        if result == "please re-enter movement":
            self.players[player.name].posn = origin
            self.message = "Invalid"
            conn.send(self.player_data(_id, name))
        else:
            self.message = ""
            self.players[player.name].posn = dest
            interaction = player.request_interaction(self.manager, dest)
            self.handle_interaction(interaction, player, self.manager, _id, conn, name)

    """
    update the name to the current thread and initilize the game if the number
    of player ready is equal to the total number of players needed, or if
    certain amount of time had passed, also restart the timer when user
    has registered their user name
    @type data: String
    @param data: the message recieved from the client part with the name
    @type conn: socket connection
    @param conn: the socket connection
    @type _id: Number
    @param _id: the thread id
    @rtype: None
    @return: None
    """
    def handle_name(self, data, conn, _id):
        name = data[6:]
        self.players[name] = None
        self.playerMap[name] = None
        self.namelist += [name]
        self.connections += 1
        self._id += 1
        print(name + " connected to the game.")
        self.message = "joined"
        conn.send(self.player_data(_id, name))
        if len(self.namelist) >= self.numplayers:
            self.thread.cancel()
            self.thread = None
            print("called init at handle name")
            self.manager = self.init_state()
            self.user_interface = False
            for name in self.namelist:
                self.leaderBoard[name] = {"exit": 0, "key": 0}
            self.message = ""
            conn.send(self.player_data(_id, name))
        else:
            self.thread.start()


    """
    initialize a game manager to play the game and other
    rtype: GameManager Class
    return: initialized game manager
    """
    def init_state(self):
        gamestate = None
        if self.generate:
            generator = SnarlLevelGenerator((self.currentLevel + 1) * 2, [5, 5], [8, 8], False, False)
            level = generator.generateLevel()
            gamestate = GameState(level, {}, {})
        else:
            level = self.levels[self.currentLevel]
            objects = level['objects']
            level = tl.handleLevel([level])
            gamestate = GameState(level, {}, {})
            for object in objects:
                type = object['type']
                posn = object['position']
                posn = (posn[1], posn[0])
                gamestate.placeObject(type, posn)

        self.totalPlayers = len(self.namelist)
        self.numplayers = len(self.namelist)
        players = gamestate.generatePlayer(self.totalPlayers)
        ads = gamestate.generateAdversary(self.currentLevel + 1)
        self.players = self.handlePlayers(list(self.players.keys()), players)
        self.playerRecord = self.handlePlayers(list(self.players.keys()), players)
        self.tempNameList = copy.deepcopy(self.namelist)
        manager = GameManager(list(self.players.keys()), level, 1000, ads, players)
        if self.observer:
            print(gamestate.draw())
        self.turn = self.namelist[0]
        self.currentPlayer = 0
        self.adlist = manager.handleAdversary()
        for name in self.namelist:
            playerPosn = self.players[name].posn
            self.playerMap[name] = manager.renderAround(playerPosn)
        return manager


    """
    given an interaction and updating the game state according to the interaction
    if the interaction is ok, move to next player
    if the interaction is eject, eject the current player and move to next in turn
    same of exited, if the user found the key, update the unlock
    @type interaction: String
    @param interaction: the interaction message
    @type player: Player Component Class
    @param player: the current player
    @type result: GameManager
    @param result: the result manager after moving the player
    @type _id: Number
    @param _id: the thread id
    @type conn: socket connection
    @param conn: the socket connection
    @type name: String
    @param name: the name of the current player
    @rtype: None
    @return: None
    """
    def handle_interaction(self, interaction, player, result, _id, conn, name):
        self.manager = result
        if interaction == "Eject":
            self.message = "Player " + player.name + " was expelled."
            del self.tempNameList[self.currentPlayer]
            self.players[player.name].expeled = True
            self.numplayers = self.numplayers - 1
            if len(self.tempNameList) == 0:
                if self.observer:
                    print("GameEnd1")
                self.handleLevelEnd()
                return

            if self.numplayers == 1 or self.currentPlayer > self.numplayers - 1:
                self.currentPlayer = 0
                self.turn = self.tempNameList[self.currentPlayer]
            else:
                player = list(self.players.values())[self.currentPlayer]
        elif interaction == "Key":
            self.message = "Player " + player.name + " found the key."
            if self.observer:
                print(self.message)
            self.unlock = True
            self.leaderBoard[player.name]["key"] += 1
            conn.send(self.player_data(_id, name))
            if self.currentPlayer < self.numplayers - 1:
                self.currentPlayer += 1
            else:
                self.currentPlayer = 0
            player = list(self.players.values())[self.currentPlayer]
        # reach an unlocked exit
        elif interaction == "Exit" and self.unlock:
            self.message = "Player " + player.name + " exited."
            self.leaderBoard[player.name]["exit"] += 1
            self.exited+=1
            self.players[player.name].expeled = True
            del self.tempNameList[self.currentPlayer]
            self.numplayers = self.numplayers - 1
            if len(self.tempNameList) == 0:
                if self.observer:
                    print("Gameend")
                self.handleLevelEnd()
                return
            if self.numplayers == 1 or self.currentPlayer > len(self.tempNameList) - 1:
                self.currentPlayer = 0
                self.turn = "adversary"
            else:
                player = list(self.players.values())[self.currentPlayer]
                self.origin = copy.deepcopy(player.posn)
        else:
            if self.currentPlayer < self.numplayers - 1:
                self.currentPlayer += 1
                self.turn = self.tempNameList[self.currentPlayer]
            else:
                self.currentPlayer = 0
                self.turn = "adversary"
            player = list(self.players.values())[self.currentPlayer]
        if self.observer:
            print(self.manager.returnGameState().draw())
        conn.send(self.player_data(self.currentPlayer, name))

    """
    update the state when the level end
    @rtype: None
    @return: None
    """
    def handleLevelEnd(self):
        self.currentLevel = self.currentLevel + 1
        print("currentlevel: " + str(self.currentLevel))
        print("totalLevel: " + str(self.totalLevel - 1))
        if self.exited == 0:
            self.status = "lose"
            return
        elif self.currentLevel >= self.totalLevel - 1:
            self.status = "win"
            return
        else:
            self.numplayers = self.totalPlayers
            self.tempNameList = copy.deepcopy(self.namelist)
            self.manager = None
            self.players = copy.deepcopy(self.playerRecord)
            self.currentPlayer = 0
            self.turn = self.tempNameList[self.currentPlayer]
            self.numMoves = 0
            self.message = "Level " + str(self.currentLevel)
            self.unlock = False
            self.exited = 0
            self.manager = self.init_state()
            return

    """
    handles user quiting, tried, but didn't quit get on how to close the thread
    as well as the server itself
    @type conn: socket connection
    @param conn: the socket connection
    @type _id: Number
    @param _id: the thread id
    @type name: String
    @param name: the name of the current player
    @rtype: None
    @return: None
    """
    def handle_user_quiting(self, conn, _id, name):
        print("game quited")
        try:
            if name == "":
                pass
            else:
                del self.players[name]
                del self.namelist[_id]
                self._id -= 1
                if len(list(self.players.keys())) == 0:
                    self.user_interface = True
        except IndexError:
            pass
        conn.send(self.player_data( _id, name))
        if self.status != "win" and self.status != "lose":
            conn.close()
        print("Player has left the game")

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
    check if the user name entered is valid
    @type name: String
    @param name: the player name to be checked
    @rtype: Boolean
    @return: if the length of player name entered is greater than 1 and not repeated
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

if __name__ == "__main__":
    levels = "snarl.levels"
    players = 1
    wait = 60
    observer = False
    address = "127.0.0.1"
    port = 45678
    generate = False

    for index in range (1, len(sys.argv)):
        argv = sys.argv[index]
        if argv in "--levels":
            levels = sys.argv[index+1]
        elif argv in "--clients":
            players = int(sys.argv[index+1])
        elif argv in "--wait":
            wait = int(sys.argv[index+1])
        elif argv in "--observe":
            observer = True
        elif argv in "--address":
            address = sys.argv[index+1]
        elif argv in "--port":
            port = int(sys.argv[index+1])
        elif argv in "--generate":
            generate = True

    if generate:
        server = snarlServer(address, port, players, None, observer, wait, generate, 2)
        server.play_game()
    else:
        with open(levels) as json_file:
            data = json_file.read()
            numlevels = int(data.split("\n", 1)[0])
            data = data.split("\n", 1)[1]
            data = pj.parse_to_json(data)
            server = snarlServer(address, port, players, data, observer, wait, generate, numlevels)
            server.play_game()
