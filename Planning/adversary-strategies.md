Strategy of moving an adversary:

An adversary keeps track of all player positions and the level map
information. The basic rule of moving an adversary is always move towards the player who is closest to it.

Example:

moving towards the closest player


if the player is on the right side of the adversary, move
towards right first

x x x x x                   x x x x x
x     p x                   x     p x
x   a   x       ---->       x     a x
x       x                   x       x
x       x                   x       x
x p     x                   x p     x
x x x x x                   x x x x x


x x x x x                   x x x x x
x       x                   x       x
x   a   x       ---->       x     a x
x     p x                   x     p x
x       x                   x       x
x p     x                   x p     x
x x x x x                   x x x x x


if the player is on the left side of the adversary, move towards left
first and then move upwards or downwards

x x x x x                   x x x x x
x       x                   x       x
x   a   x       ---->       x a     x
x p     x                   x p     x
x x x x x                   x x x x x


x x x x x                   x x x x x
x p     x                   x p     x
x   a   x       ---->       x a     x
x       x                   x       x
x x x x x                   x x x x x



If the adversary cannot step on a tile occupied by another adversary,
In this case, the first choice of a zombie's movement is invalid. It
move upwards instead to avoid stepping onto another adversary.
x x x x x                   x x x x x
x p     x                   x p z   x
x a z   x       ---->       x a     x
x       x                   x       x
x x x x x                   x x x x x

This wouldn't bother the ghost:
x x x x x                   x x x x x
x p     x                   x p     x
x a g   x       ---->       xa/g    x
x       x                   x       x
x x x x x                   x x x x x


Since a zombie cannot leave the room, if the closest player is in
another room, it will still move towards the player(Since it cannot
skip a move if there is valid movement)
x x x x x         x x x x x
x       x         x p     x
x z     2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x       x         x p     x
x   z   2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x


Cases are the same for the invalid movement case:
x x x x x         x x x x x
x       x         x p     x
x z     2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x       x         x p     x
x   z   2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x


cannot hit a wall
x x x x x         x x x x x
x     z x         x p     x
x       2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x       x         x p     x
x     z 2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x


(no valid movement, surrounded by adversaries)
x x x x x         x x x x x
x a     x         x p     x
x z a   2 + + + + 2       x
x a     x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x a     x         x p     x
x z a   2 + + + + 2       x
x a     x         x       x
x x x x x         x x x x x


This wouldn't happen for a ghost because a ghost can walk
on hallways and move into wall tiles:


x x x x x         x x x x x
x     g x         x p     x
x       2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x       g         x p     x
x       2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
HERE, THE GHOST WILL BE SEND TO A RANDOM ROOM




x x x x x         x x x x x
x       x         x p     x
x     g 2 + + + + 2       x
x       x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x       x         x p     x
x       g + + + + 2       x
x       x         x       x
x x x x x         x x x x x

            |
            |
            |
            V
x x x x x         x x x x x
x       x         x p     x
x       2 g + + + 2       x
x       x         x       x
x x x x x         x x x x x


A ghost can walk on another adversary

x x x x x         x x x x x
x a     x         x p     x
x g a   2 + + + + 2       x
x a     x         x       x
x x x x x         x x x x x
             |
             |
             |
             V
x x x x x         x x x x x
x a     x         x p     x
x  a/g  2 + + + + 2       x
x a     x         x       x
x x x x x         x x x x x
