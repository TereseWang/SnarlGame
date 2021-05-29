Player : represents the interests of the human behind the keyboard in the game. <br />
A Player needs to receive updates from the Game Manager at appropriate moments. <br />
When it’s the Player’s turn, it needs to communicate the chosen action to the Game Manager. <br />
<br />

  Fields: <br />
  
    Posn        position            // the position of this player 
    
    boolean     expelled            // whether this player is expelled 
    
    
<br />
Functions: <br />
// takes in tiles that are valid to move to around this players <br />
// update the position <br />
move_player(Posn[] valid_tiles) <br />

<br />
// renders all the tiles around this player and the player location in<br />
// relation to level's origin<br />
render(Posn[] tiles)<br />
<br />
// expell this player, turn the expelled : False -> True<br />
expell()<br />
<br />
// activate this player, turn the expelled: True -> False<br />
activate()<br />
