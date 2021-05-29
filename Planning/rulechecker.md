### RuleChecker Component:

#### -- check invalid game state:

  * map should be able to check if itself is a valid map.(no overlapping, all rooms

    and hallways connected)

  * check while initializing the game:

    player number is int and larger than 0

    final level is int and larger than 0
    
    there is no player or no adversary (error in genrating functions)



  * check while updating the level:

    if current level is larger than final level, or current level < 0

    there is no player or no adversary



  * during the moving players:

    if all players are expelled and game doesn't end






#### -- let the player make a valid move:

* get_valid_move(Posn):

  pass the current posn to map, get a lists of traversable tiles around the player.

  (The chosen tile can be occupied by a key, exit, or an adversary, or nothing.)

  split them into two lists according to the distance from player.

  return: 1. distance_one=[posn1, posn2, posn3, posn4]    2. distance_two=[posn1,..., posn8]




#### -- let the adversary make a valid move:

the adversary knows all the information in the map, and AI should give us valid movement.



#### -- respond to player's movement:

* check_spell(posn):

  pass in the tile position the player is moving to, see if there is an adversary.

  If it is, spell the player.


Pass to map: the tile the player is moving to

map should return an enum showing if there is an exit, a key or other objects there.

* check_find(enum):

  if enum is a key, set unlock the current level

  if enum is exit, go and check if current level is true. If it is, call next_level(). Otherwise, tell the user they have reached the exit.
  
  if received unknown enum, recognize as invalid game state.



* next_level():

  if current level equals final level, let player win the game.

  Otherwise, generate a new map and update all fields in the game state.

  (level increased by 1, active all players, place all players at new start level, unlock = False)
  
