Adversary <br />
* An adversary gets the full level information (comprised of rooms, hallways and objects) at the beginning of a level<br />
* An adversary gets an update on all player locations, but only when it’s about to make a turn <br />

Since the adversary keeps track of all game informaiton, <br />
including the locations of objects. Thus, we put SnarlLevel as a <br /> field in the adversary component
  Fields:
    map:          SnarlLevel
    name:         string
    posn:         position (turple)
    alive:        boolean
    type:         string

    <br />


    Functions:
    <br />
    """
    request a movement. Since all players are stored in GameManager, <br />
    GameManager will tell the adversary all player locations<br />
    manager: GameManager
    posn: turple     destination of this movement
    """
    def request_move(manager, posn)
    <br />

    <br />
    """
    Use the map info and all players' location to determin next movement.<br />
    player_loc: list of posns(turple)
    """
    def determin_move(player_loc)
    <br />


    <br />
    """
    update the movement, change current posn.
    posn: turple
    """
    def update_move(posn)
    <br />


    <br />
    """
    kill or activate this adversary. Change the alive field.
    boo: boolean
    """
    def change_alive(boo)
    <br />
