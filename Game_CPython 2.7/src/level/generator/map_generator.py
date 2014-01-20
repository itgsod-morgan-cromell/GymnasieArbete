###########################################
## Dungeon Generator -- map_generator.py ##
###########################################
####### Breiny Games (c) 2011 #############
###########################################
## This file contains the classes and    ##
## functions used to generate a random   ##
## dungeon in plain text which can be    ##
## used by either the 'map_loader' module##
## to visually display the dungeon in a  ##
## pygame window or by the 'text_only.py'##
## module to print the map in plain text ##
###########################################





import random
import time
from astar import *
from distance_map import *





class Room:


    """
    The class for all of the rooms in a dungeon.
    

    Room((size_x, size_y), tiles)


    (size_x, size_y)
        -an ordered pair representing the size of the room.

    tiles
        -a 2D list containing numbers that represent tiles inside the room.
            0 = blank space (non-useable)
            1 = floor tile (walkable)
            2 = corner tile (non-useable)
            3 = wall tile facing NORTH.
            4 = wall tile facing EAST.
            5 = wall tile facing SOUTH.
            6 = wall tile facing WEST.
            7 = door tile.
            8 = stairs leading to a higher lever in the dungeon.
            9 = stairs leading to a lower level in the dungeon.
            10 = chest
            11 = path from up to down staircases (floor tile)
    """


    def __init__(self, (size_x, size_y), tiles):

        self.size = (size_x, size_y)
        self.tiles = tiles
        self.position = None





class Dungeon:


    """
    The Dungeon class.
    

    Dungeon((grid_size_x, grid_size_y),
             name,
             max_num_rooms,
             min_room_size,
             max_room_size)

    (grid_size_x, grid_size_y)
        - the total size/area of the map in tiles.
            e.g. (25, 20) would set the map to be 25 tiles wide and 20 tall.

    name
        - the name of the dungeon

    max_num_rooms
        - the maximum number of rooms for the dungeon to contain.

    min_room_size
        - the minimum size for each room.
            e.g. (3, 3) would set the minimum room size to 3 tiles by 3 tiles.

    max_room_size
        - the maximum size for each room.
            e.g. (7, 7) would set the maximum room size to 7 tiles by 7 tiles.

    (tile_w, tile_h)
        - the size of the tiles in pixels.



    Misc Information:

        -self.grid is the most important variable in this whole file. It is a 2
        dimensional list that stores the entire map and layout of the dungeon.
        Each number in the list represents a tile in the dungeon.
            0 = blank space (non-useable)
            1 = floor tile (walkable)
            2 = corner tile (non-useable)
            3 = wall tile facing NORTH.
            4 = wall tile facing EAST.
            5 = wall tile facing SOUTH.
            6 = wall tile facing WEST.
            7 = Monster
            8 = stairs leading to a higher lever in the dungeon.
            9 = stairs leading to a lower level in the dungeon.
            10 = chest
            11 = path from up to down staircases (floor tile)
            12 = door vertical

        -self.rooms stores the Room object from the Room class, which stores
         what tiles are room holds, the size of the room, and the coordinate
         of the top-left tile (number) of the room. The position and size
         variables are especially important because they are used together to
         calculate the section of the dungeon grid we look at to pick a random
         wall (number) to branch from in the get_branching_position() function.
            


    Functions:
    

        print_info(grid=True)
            - prints the name, size, number of rooms, and if passed 'True' for
              the grid argument, prints the actual layout of the dungeon, all
              to the python shell.
              

        generate_room((min_size_x, min_size_y), (max_size_x, max_size_y))
            - enerates a randomly sized list of numbers to represent a room.
              (see the Room class for more details on what the numbers mean.)

            (min_size_x, min_size_y)
                - the minimum size of each room to be generated.

            (max_size_x, max_size_y)
                - the maximum size of each room to be generated.


        get_branching_position()
            - picks a random room that has been placed, then picks a random
              (valid) wall tile (number) from the room, and returns the
              position in the dungeon grid that it is located at. Valid walls
              (numbers) include 3, 4, 5, 6. See the Room class for more info
              on what the numbers actually represent.


        get_branching_direction(branching_position)
            - returns the direction the passed 'wall tile' (numbers 3, 4, 5, 6
              in the grid list) is facing.

            branching_position
                - the coordinates of the 'wall tile' in the grid list we want
                  to find out which way is facing.


        space_for_new_room((new_room_size_x, new_room_size_y),
                            new_room_position)
            - checks to see if there is space to add a given room to the
              dungeon. Returns True if there is, False if otherwise.

            (new_room_size_x, new_room_size_y)
                - the size of the room to be checked.

            new_room_position
                - the coordinates of where the room would be. We start here,
                  then check the entire area of the grid the room covers
                  to see if it overlaps with any other rooms. If it doesn't
                  overlap with anything, return True. Otherwise return False.


        place_room(room, (grid_x, grid_y))
            - changes the grid list to add the given room to it.

            room
                - the room we want to add to the grid.

            (grid_x, grid_y)
                - the location inside the grid we want to change to add the
                  room to.


        connect_rooms(branching_pos, direction)
            - slightly changes the grid list to connect 2 rooms. Changes the
              wall tile, and the tile next to it in the direction it's
              facing, both to floor tiles (1's in the grid list).

            branching_pos
                - the location of the tile we just added a room to.

            direction
                - the direction the wall was facing before we added the room.

            *- think of it like this. We pick a random wall tile of a random
               room. This is the spot we want to add another room to. After we
               add the room to that spot, we now turn that spot from a wall tile
               into a floor tile (e.g. a 3 into a 1), then whichever way the
               tile was facing, we take the tile in that direction next to it
               and also turn it into a floor tile.


        set_staircases()
            - picks a random room, then a random floor tile (a 1 in the grid
              list) and turn it into a staircase going up (8 in the grid list).
              Then does the same thing again, but changes the next floor tile
              into a staircase going dowm (9 in the grid list).


        generate_dungeon()
            - uses all of the above functions, to generate a dungeon.
    """
    

    def __init__(self,(grid_size_x, grid_size_y), name,
                 max_num_rooms, min_room_size, max_room_size,
                 (tile_w, tile_h)):

        self.grid_size = (grid_size_x, grid_size_y)
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.name = name
        self.max_num_rooms = max_num_rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.rooms = []
        self.grid = []
        self.width = grid_size_x * tile_w
        self.height = grid_size_y * tile_h


    def print_info(self, grid=False):

        print "Printing Dungeon Info...\n\n"
        print "NAME:  " + str(self.name)
        print "SIZE:  " + str(self.grid_size[0]) + "x" + str(self.grid_size[1])
        print "ROOMS:  " + str(len(self.rooms)) + "\n\n"
        if grid:
            for row in self.grid:
                print row


    def generate_room(self, (min_size_x, min_size_y), (max_size_x, max_size_y)):

        size_x = random.randint(min_size_x, max_size_x)
        size_y = random.randint(min_size_y, max_size_y)
        tiles = []

        for y in range(0, size_y):
            row = []
            for x in range(0, size_x):
                if x == 0 and y == 0:
                    row.append(2)
                elif x == size_x-1 and y == 0:
                    row.append(2)
                elif x == 0 and y == size_y-1:
                    row.append(2)
                elif x == size_x-1 and y == size_y-1:
                    row.append(2)
                elif y == 0:
                    row.append(3)
                elif x == size_x-1:
                    row.append(4)
                elif y == size_y-1:
                    row.append(5)
                elif x == 0:
                    row.append(6)
                else:
                    row.append(1)
            tiles.append(row)

        return Room((size_x, size_y), tiles)


    def get_branching_position(self):

        branching_room = random.choice(self.rooms)
        branching_tile_position = (0, 0)
        for i in range(0, branching_room.size[0] * branching_room.size[1]):
            
            x = random.randint(branching_room.position[0],
                               branching_room.position[0] + branching_room.size[0]-1)
            y = random.randint(branching_room.position[1],
                               branching_room.position[1] + branching_room.size[1]-1)

            if self.grid[y][x] > 2:
                branching_tile_position = (x, y)
                break

        return branching_tile_position


    def get_branching_direction(self, branching_position):

        direction = None
        if self.grid[branching_position[1]][branching_position[0]] == 3:
            direction = "NORTH"
        elif self.grid[branching_position[1]][branching_position[0]] == 4:
            direction = "EAST"
        elif self.grid[branching_position[1]][branching_position[0]] == 5:
            direction = "SOUTH"
        elif self.grid[branching_position[1]][branching_position[0]] == 6:
            direction = "WEST"
        else:
            return False

        return direction


    def space_for_new_room(self, (new_room_size_x, new_room_size_y), new_room_position):

        new_room_size = (new_room_size_x, new_room_size_y)
        for y in range(new_room_position[1],
                       new_room_position[1] + new_room_size[1]):
            for x in range(new_room_position[0],
                           new_room_position[0] + new_room_size[0]):
                if x < 0 or x > self.grid_size[0] - 1:
                    return False
                if y < 0 or y > self.grid_size[1] - 1:
                    return False
                if self.grid[y][x] != 0:
                    return False

        return True


    def place_room(self, room, (grid_x, grid_y)):

        room.position = (grid_x, grid_y)

        room_tile_x = 0
        room_tile_y = 0
        for y in range(grid_y, grid_y + room.size[1]):
            for x in range(grid_x, grid_x + room.size[0]):
                self.grid[y][x] = room.tiles[room_tile_y][room_tile_x]
                room_tile_x += 1
            room_tile_y += 1
            room_tile_x = 0


    def connect_rooms(self, branching_pos, direction):

        chance = random.randint(1, 25)
        if chance == 25:
            self.grid[branching_pos[1]][branching_pos[0]] = 1
        else:
            self.grid[branching_pos[1]][branching_pos[0]] = 1

        if direction == "NORTH":
            self.grid[branching_pos[1]-1][branching_pos[0]] = 1
        elif direction == "EAST":
            self.grid[branching_pos[1]][branching_pos[0]+1] = 1
        elif direction == "SOUTH":
            self.grid[branching_pos[1]+1][branching_pos[0]] = 1
        elif direction == "WEST":
            self.grid[branching_pos[1]][branching_pos[0]-1] = 1


    def set_staircases(self):
        

        for i in range(0, len(self.rooms)):
            stairs_up_room = random.choice(self.rooms) 
            x = stairs_up_room.position[0] + (stairs_up_room.size[0]/2)
            y = stairs_up_room.position[1] + (stairs_up_room.size[1]/2)
            if self.grid[y][x] == 1:
                self.grid[y][x] = 8
                break

        for i in range(0, len(self.rooms)):
            stairs_down_room = random.choice(self.rooms)            
            x = stairs_down_room.position[0] + (stairs_down_room.size[0]/2)
            y = stairs_down_room.position[1] + (stairs_down_room.size[1]/2)
            if self.grid[y][x] == 1:
                self.grid[y][x] = 9
                break


    def find_path_between_staircases(self):

        astar = Pathfinder()

        start = None
        end = None
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[0])):
                if self.grid[y][x] == 8:
                    start = (x, y)
                elif self.grid[y][x] == 9:
                    end = (x, y)
                if start != None and end != None:
                    break
        
        path = astar.find_path(self.grid, start, end, [0, 2, 3, 4, 5, 6, 7])

        if path != None:
            for i in range(0, len(path)-1):
                self.grid[path[i][1]][path[i][0]] = 11
        else:
            print "No path possible."


    def generate_dungeon_map(self):

        self.rooms = []
        self.grid = []
        for y in range(0, self.grid_size[1]):
            row = []
            for x in range(0, self.grid_size[0]):
                row.append(0)
            self.grid.append(row)

        self.rooms.append(self.generate_room(self.min_room_size,
                                             self.max_room_size))

        self.place_room(self.rooms[-1],
                            (self.grid_size[0]/2 - (self.rooms[-1].size[0]/2),
                             self.grid_size[1]/2 - (self.rooms[-1].size[1]/2)))

        for i in range(0, ((self.grid_size[0] * self.grid_size[1]) * 2)):

            if self.max_num_rooms != 0:
                if len(self.rooms) == self.max_num_rooms:
                    break
            
            branching_pos = self.get_branching_position()
            direction = self.get_branching_direction(branching_pos)
            if direction:

                new_room_pos = (0, 0)
                new_room = self.generate_room(self.min_room_size,
                                              self.max_room_size)

                if direction == "NORTH":
                    new_room_pos = (branching_pos[0] - (new_room.size[0]/2),
                                    branching_pos[1] - new_room.size[1])
                elif direction == "EAST":
                    new_room_pos = (branching_pos[0] + 1,
                                    branching_pos[1] - (new_room.size[1]/2))
                elif direction == "SOUTH":
                    new_room_pos = (branching_pos[0] - (new_room.size[0]/2),
                                    branching_pos[1] + 1)
                elif direction == "WEST":
                    new_room_pos = (branching_pos[0] - (new_room.size[0]),
                                    branching_pos[1] - (new_room.size[1]/2))

                if self.space_for_new_room(new_room.size, new_room_pos):
                    self.place_room(new_room, new_room_pos)
                    self.rooms.append(new_room)
                    self.connect_rooms(branching_pos, direction)
                else:
                    i += 1


    def set_chests(self):

        map = distance_map(self.grid, [11], [0, 2, 3, 4, 5, 6, 7, 8, 9])
        distances = []

        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if map[y][x] not in distances and map[y][x] != -1:
                    distances.append(map[y][x])

        average = 0
        for i in distances:
            average += i
        average /= len(distances)-1

        possible_places = []
        for y in range(0, len(map)):
            for x in range(0, len(map[0])):
                if map[y][x] >= average:
                    possible_places.append((x, y))


        chests_to_place = len(self.rooms) / 5
        if chests_to_place <= 0:
            chests_to_place = 1
        for i in range(0, chests_to_place):

            chance = random.randint(0, 2)
            location = None
            if chance == 1:
                room = random.choice(self.rooms)
                x = random.randint(room.position[0],
                                   room.position[0] + (room.size[0]))
                y = random.randint(room.position[1],
                                   room.position[1] + (room.size[1]))
                location = (x, y)
            else:
                location = random.choice(possible_places)

            try:
                if self.grid[location[1]][location[0]] == 1:
                    self.grid[location[1]][location[0]] = 10
            except IndexError:
                print "Error creating chest at {0}, {1}".format(location[0], location[1])

    def set_monsters(self):
        monsters_to_place = len(self.rooms)*3
        if monsters_to_place <= 0:
            monsters_to_place = 1
        for i in range(0, monsters_to_place):
            room = random.choice(self.rooms)
            x = random.randint(room.position[0],
                               room.position[0] + (room.size[0]))
            y = random.randint(room.position[1],
                               room.position[1] + (room.size[1]))
            location = (x, y)
            try:
                if self.grid[location[1]][location[0]] == 1:
                    self.grid[location[1]][location[0]] = 7
            except IndexError:
                pass


    def generate_dungeon(self):

        print "\n\n* Generating dungeon...",
        start = time.time()
        self.generate_dungeon_map()
        end = time.time()
        print "  DONE!   in " + str(round(end-start, 3)) + " seconds"

        print "* Setting staircases...",
        start = time.time()
        self.set_staircases()
        end = time.time()
        print "  DONE!   in " + str(round(end-start, 3)) + " seconds"

        print "* Finding path...",
        start = time.time()
        self.find_path_between_staircases()
        end = time.time()
        print "        DONE!   in " + str(round(end-start, 3)) + " seconds"

        print "* Setting chests...",
        start = time.time()
        self.set_chests()
        end = time.time()
        print "      DONE!   in " + str(round(end-start, 3)) + " seconds"

        print "* Setting monsters...",
        start = time.time()
        self.set_monsters()
        end = time.time()
        print "    DONE!   in " + str(round(end-start, 3)) + " seconds"
