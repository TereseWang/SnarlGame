We use pygame to display all the view, so in order to actually play <br />
 the game, you need to run the following command in terminal: <br />

  -- pip install pygame<br />

To start the game, run following command in the terminal with github releases: <br />
(player# and level# are number of total players and the number <br />
  of initial level) <br />


  Player View Version:
     ./localSnarl --levels snarl.levels --players player# --start level#    <br />

    Whole Map View Version
      ./localSnarl --levels snarl.levels --players player# --start level# --observe   <br />

Operations in the game:   <br />

  Register players:  
    enter player1 name, hit "enter" or click the button
      ... ...
    enter playerN name, hit "enter" or click the button


Play the game:<br />
use the "up","down","right" and "left" keys to select the destination<br />
hit enter to confirm the movement<br />
if the movement is invalid, it will return back to original position<br />
and ask the user to reenter the movement <br />
only tiles that is within range of 2 tiles can be selected <br />
after all players moved, adversaries will move at the same time <br />
<br />
All game information including the unlock status, expel player info<br />
will be displayed on the right side of the screen.<br />
