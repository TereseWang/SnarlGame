Basically we follow all the steps provided on course website.

1. Generate randomly sized rooms at random points within a circle of a given radius.

    we generate twice as the required number of rooms so that
    we can pick "main" rooms from them later to avoid our rooms
    getting too close.

2. Separate rooms by moving them apart until they don’t overlap.

    We follow the idea of separation behavior, find the
    normalized vector and move until we cannot find any
    overlapping cases. We came into several problems.

    First is the infinite loop. This is caused by our simple way of
    determine the movement. We first used for loops to make sure that every
    room after our chosen room does not overlaps this room. Since moving one
    room will affect the distance and overlapping relationship between this room
    and all its neighbors. We were unable to remove all overlapping. We fixed
    this using the idea normalized vector. We take all its close neighbors location
    and decide the next move.

    Second is still infinite loop or huge runtime cause by some rooms moving back
    to the origin at some point. So we keep track of its origin before getting into
    loops.


3. Generate a connected graph out of rooms, taking the topology into consideration.

    We only take the "main" rooms out form all the seperated rooms. we sort all
    the rooms with its location, ordering them from upper left to buttom right.
    Then take the ordinary index. This gives much space between our rooms.
    Delaunay Triangulation was used here.  It returns a plot showing the all
    the main rooms. Also, this graph gives us tree for future generating.

4. Reduce the number of connections in the graph.

    KST algorithm used. First of all, we sort all the edges by the length.
    We keep adding the edge to the graph starting from the shortest edge.
    Every time adding a new edge, we check if there is a cycle, if not continue.
    Otherwise, we add the second shortest edge instead and check. This part returns
    tree_map of pairs of connection information.

5. Generate hallways between connected rooms.

   We uses the information from part 4 to generate hallways. Each time we connect
   2 rooms. First we check if these two rooms can be connected through a simple
   horizontal or vertical line. If not, we look for a way point, a corner, for
   our hallway. A difficult part here is checking whether the hallway is valid
   and to handle invalid case. Since every room is connected to its closest neighbor
   according to the KST algo, it should not happen that there doesn't exist a
   valid hallway for two rooms. However, in some edge cases, when some other room
   is very large and takes up too much space, this will happen. In this case, we
   decided to regenerate the map.
