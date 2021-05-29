The Observer component observes GameState. It should have functions<br /> returning all necessary views. It doesn't need to store the gamestate.<br />
## Fields:
   gamestate   GameState of current game
   
## Functions:<br />
### For visualizing the game: <br />
   renders an initial view brefore game actually starts.
   `renderInitView()`<br />


   renders a view of a player when it is his turn to move the view should include tiles <br /> and adversaries around him.<br />
    
   In the future, more functionalities can be added here. For example: Showing the <br /> direction of other players(since gamestate has all player info)<br />
   Showing the direction of key/exit/object ...<br />
    <br />
   input: name      -- String<br />
   `renderLevelPlayerView(gamestate,name)` <br />


   renders an end view when players win the game show the whole map and congratulation message <br /> 
   `renderWinView(gamestate)` <br />


   renders an end view when players lose the game show the whole map and lose message<br />
   `renderLoseView()`<br />


   renders whole gamestate, including the map and all players and adversaries locations<br />
   `renderWholeMap()`<br />
   
   
### For testing <br />

  return all the locations of alive players.  <br />
  output: dictionary {posn: player}  <br />
  where posn is a turple and player is a Stirng of player name 
  <br>
`allPlayersLocation()`<br>

 return the location for each adversary, 
 output: dictionary {posn: adversary}  <br />
  where posn is a turple and adversary is a Stirng of adversary name <br>
`allAdversariesLocation()`<br>

 return the status for each player,
 output: dictionary {player: status}  <br />
  where player is a name(String) and status is either "expelled" or "alive" <br>
`allPlayersStatus()`<br>

return whether the exit is unlocked.<br>
`exitUnlocked()`<br>

return whether this level has ended or not. True if player pass the level or all <br>
players are expelled. Otherwise, return False<br>
`levelEnded()`<br>
