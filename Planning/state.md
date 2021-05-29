GameWorld

Below is the model of the game, visualization not included. The game states will be a class that stores all the necessary
information to run this game. To ensure the security of the data, all fields in Map cannot be mutated. Also, to support the
unknown part of moving adversaries, the adversary will be able to retrive all data from the GameWorld.

Fields:


    player[]     players       -- list of players involved

    adversary{}  adversaries   -- dictionary of all adversaries players need to face, key is positon and value is adversary

    Map          map           -- a map containing all location information(rooms, hallways, objects, key, doors)

    Boolean      unlock        -- boolean to show whether the map of current level is unlocked

    int          level         -- current level

    int          finalLevel    -- total levels in this game
    
    Boolean      turn          -- current turn of Player or Adversary


Functions:

First of all, we need to initialize a new game:

    __init__(int finalLevel, int playerNumber):
    
      if the input is valid, use it as the finalLevel
      
      set the current level to 1, players = [], adversaries = {}, unlock = False

      generateNewMap()                      -- generates a new map and update the level when the game starts or plays exit current level

      initPlayers(Posn, playNumber)         -- interact with users and add new player to the player[], place players at the start point

      initAdversary()                       -- use the map and level to generate adversary dictionary


Then we can start play the game:


    move()                -- move players and adversaries, respond to all the movements

    first, go through the list of players. If one player is not spelled, then move him:

        In map class, we need functions like:
        retriveLocInfo(Posn)  -- retrives the location information on a given position(object information not included)
        from map, so the game can display the tiles around the player and the player can make a valid move


        movePlayer(Posn[])    -- pass in all valid positions and let the player to move. One move can have the following results:
        1. spell this player is he runs into an adversary
        2. if the player doesn't got spelled, send the current player position to map and check if he finds any objects, map returns 
        an Enum to us. 
          

        checkFind(Enum)       -- update the unlock info or call nextLevel().
          1. find a key -> unlock = true
          2. find the exit -> 
                 (i). unlocked -> nextLevel
                 (ii). locked -> tell the user they find the exit
          3. other objects(weapons,props) -> call related Functions
          
          
    When a player reaches an unlocked exit, move them to next level 
        
        nextLevel()           -- increase current level by 1, if it is larger than finalLevel, call endGame("win").
                                if not win, genrate a new map, activate all players, and place players at the start point.


    after moving all players, go through the player list again and move all adversaries around them:


    Here, the way we call moveAdversary() might change according to the code provided for the movement of adversaries.
    Basically, we hope to only move adversaries around the players to avoid unecessary work. Thus, for each player,
    we use its posn to find nearby adversaries in the dictionary, then we call moveAdversary() and pass in the position of this player.


        moveAdversary(Posn)    -- pass in a position of a player and let the adversaries move, spell this player if an
                      adversary hits him
                      
    

    everytime after we spell a player, call this function:

        checkAllSpell()       -- check if all players are spelled, if so, call endGame("lost").

    if all players are spelled or players exit the final level, let them lose/win the game

        endGame(String)       -- end the game, render the end scene and interact with user to decide whether to start a new game.
