We use pygame to display all the view, so in order to actually player <br />
 the game, you need to run the following command in terminal: <br />

  -- pip install pygame<br />



To start the game, run following command in the terminal: <br />
(player# and level# are number of total players and the number <br />
  of initial level) <br />


Always start the server before client:
    python3 ./snarlServer ......    <br />
    python3 ./snarlClient ......    <br />
  "......" part is the IP address, port number, wait second mentioned as in the milestone requirements. <br />

  Run the server first in order to start the game, the observer functionality is incomplete so nothing will pops up for observe purpose, however server does keep track of the update inside of the terminal.

  Game for multiplayer seems to have some bug due to unknown reason, that after some movements, player will flash to some place and all the movement will be invalid after. Also just a reminder, when people has entered their name and the game has started, please just click window with mouse click to ensure the window will be refreshed. Since Game is played using tcp, it will allow user to connect to the game with different device as long as they are connecting to the same wifi and get the ip address correctly. 



Operations in the game:   <br />


  Register players: (Do the same for all player GUI window)
    enter player name, hit "enter"




Play the game:<br />
use the "up","down","right" and "left" keys to select the destination<br />
hit enter to confirm the movement<br />
<br />
All game information including the unlock status, expel player info<br />
will be displayed on the right side of the screen.<br />
