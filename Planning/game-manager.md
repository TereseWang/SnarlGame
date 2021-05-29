Game Manager: accept players to the game and start a game with a single level. <br />
Players should provide a unique name when registering.<br />
<br />
Fields: 

    Player{}      players            // a set of players    
    
    GameState     gameworld          // game state, a game with a single level 
    
    int           total_level        // total levels players need to pass before they win 
    
    int           current_level      // current level 
    
    int           difficulty         // the difficulty of the game [1,5] 

<br />
Functions:<br />
// let the user choose the difficulty and total levels of the game, init the class<br />
init(int total_level, int difficulty)<br />
  current_level = 0;<br />
  players = {};<br />
  gameworld = null;<br />

<br />
// interact with users, takes in the names of players, check for uniqueness<br />
// generate the player list<br />
accept_player(String[] arg)<br />

<br />
// use players and current_level to start a game with a single level<br />
// determine the number of adversaries using difficulty<br />
start_game()<br />

<br />
// if players pass the last level, let them win<br />
win()<br />

<br />
// if the players fail to pass current game world, they lose the game.v
lose()<br />
