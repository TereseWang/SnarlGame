## Part 1
#### Players
Player Location, Player ID/UserName to distinguish between players, Expelled or not.
#### Adversaries 
Fields: Adversaries Location, Monster type (may be zombies or ghosts).
They should also be able to retrieve all info of current map.
#### Map
Map is composed of different rooms or hallways. It stores the information about key location, exit location, start location.
It cannot be mutated but can send out the information to game World.
#### Game World 
A GameWorld stores all the information of this game, including all players and adversaries, 
map, current level, total level, game state("win", "progress", "lose"), turn (players' turn 
or adversaries' turn), exit of current level is locked or not. The gameworld gets 
data from map to unlock the exit, determine players' or adversaries' movements, expel players and move to next level.

## Part 2
We will have a main gameworld class composed of a Map(Listof(Rooms), keyLocation, ExitLocation, StartLocation), 
a list of Players(String ID, Posn Location, Bool Expelled), a list of Adversaries(String Type, Posn Location), 
Boolean Gamestate, Int currentLevel, Int finalLevel, String currentTurn. 

When the game is initialized, map will be genralized by connecting rooms and hallways together, locations of objects, 
exit, key will be generated randomly. Map class should also be able to send out map info around a given location, so users 
will see the surrounding envrionemnt.

Player class, player can call move function (mutate the position when gameworld told it to do), update whether it 
is expelled. Player class also can call a function that gets a list of the objects around them and valid tiles they 
can move to.

Adversaries will be implemented similar to player, which is able to move around.

For Gameworld class, we will have a initilazation function where all the adversaries should be generated, functions to 
update the level and players location and generate a new map. Gameworld lets the players and adversaries move in turn. 
It retrives data from the map and respond to all movements of players or adversaries. Gameworld should also update the 
game state when all players is expelled (losing the game) or reached the unlocked exit of the final level (winning the game)


