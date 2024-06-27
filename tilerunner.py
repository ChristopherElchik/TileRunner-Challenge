# MAIN FILE FOR STUDENTS
import random
import tkinter as tk
import copy

# This is your starter code for the tile runner challenge. We already implemented the
# environment for you. Your ONLY job is to add code to the nextMove() function in the Robot class.
# Here is a general outline of the file:
#
# - Tile class: This class holds the information about an individual tile on the grid. You can use
# the get_status() function to get the status of a tile. A tile can have one of the following statuses:
# WALL, VISITED, or UNVISITED. You can also view the tiles around a tile via the get_above(), get_right(), etc.
# If you call the get_above() function on a tile where there is no tile above it, it will return None (this
# applies to the other directions, too). You should not change any of the code in this class.
#
# - Environment class: This class handles the grid of tiles (called map), which is stored in a 2D array.
# You will have access to this array from the robot class, but you shouldn't need to use it, as you can
# already see your immediate surroundings via the getters from the Tile class. You should not change
# any of the code in this class.
#
# - Robot class: This class controls the location and movements of your robot. All of your code MUST be
# inside of this class for it to be graded properly. You will write code in the nextMove() function, where
# you will tell the robot to do one of the following: MOVE_RIGHT, MOVE_LEFT, MOVE_UP, MOVE_DOWN, or STAY_STILL.
# Your robot will keep track of its current location in a variable called self.pos, which will always be stored
# as a Tile, meaning you can use Tile's functions to look at the tiles around you (e.g., self.pos.get_right()
# to get the tile to your right). You can write code outside the nextMove() function if you wish (i.e., if
# your algorithm needs to keep track of the robot's history), but your code MUST be inside the Robot class.
# Be sure to not change the move() function.
#
# - Grid class: The Grid class handles the visual interface of the tile runner challenge, as well as the
# elements behind the scenes, such as the robot's statistics and overall score. DO NOT change this class.
#
# Below are some global variables you can edit depending on how you want to test your robot.

# Toggles visualization of robot. Set this to false to disable the
# visual simulation. 
VISUALIZE = True

# Number of iterations the simulation will run (when VISUALIZE = False). Our grading script will
# run 100 iterations to see how consistent your robot is.
ITERATIONS = 100

# This is the file of the map to be used. You can change this to
# use any map you want. Feel free to test your robot on custom maps!
# When grading, we will test your robot on many maps of different sizes and difficulties.
#
# All maps must be a .txt file, where each character represents a tile. Your arrangement of
# characters must be in a rectangle. Your tiles can be represented by one of three characters:
# 'U' for an unvisited tile, 'V' for a visited tile, and 'W' for a wall. You can use the
# sample files as a reference.
#
# Note: Your robot will ALWAYS start in the top left corner.
MAP_FILE = "maps/MAP_20.txt"

# Size of each tile in pixels (Feel free to adjust to fit your screen)
TILE_SIZE = 50

# Set to true to results of non-visual simulation
PRINT_RESULTS = True

# constants to define the robot's movement. Your nextMove() function
# MUST return one of these. DO NOT change these values!
STAY_STILL = 0
MOVE_UP = 1
MOVE_RIGHT = 2
MOVE_DOWN = 3
MOVE_LEFT = 4

# constants that hold the statuses of tiles... DO NOT CHANGE THESE
WALL = 0  # 'W' in file
UNVISITED = 1  # 'U' in file
VISITED = 2  # 'V' in file

# Directions dictionary, maps a move to a vector... DO NOT CHANGE THESE
DIRECTIONS = {
    MOVE_UP: (-1, 0),
    MOVE_DOWN: (1, 0),
    MOVE_LEFT: (0, -1),
    MOVE_RIGHT: (0, 1),
    STAY_STILL: (0, 0)
}

# Number of moves the user can make until the program cuts off. Our grading script will allow 200 moves.
MOVES = 200

# Delay (in milliseconds) between robot moves in the visual simulation. A higher delay causes a slower robot.
DELAY = 20

# Tile info
class Tile:

    def __init__(self, status: int, row: int, col: int):
        self.status = status
        self.row = row
        self.col = col
        self.above = None
        self.below = None
        self.left = None
        self.right = None

    # Returns status of tile
    def get_status(self):
        return self.status

    # sets status of tile. We will do this for you. DO NOT use this function!
    def set_status(self, status):
        self.status = status

    # returns row of tile
    def get_row(self):
        return self.row

    # sets row of tile. This is done for you. DO NOT use this function!
    def set_row(self, row: int):
        self.row = row

    # returns column of tile.
    def get_col(self):
        return self.col

    # sets column of tile. This is done for you. DO NOT use this function!
    def set_col(self, col: int):
        self.col = col

    # Returns the tile above this tile
    def get_above(self):
        return self.above

    # Sets the tile above this tile. This is done for you. DO NOT use this function!
    def set_above(self, above):
        self.above = above

    # Returns the tile below this tile
    def get_below(self):
        return self.below

    # Sets the tile below this tile. This is done for you. DO NOT use this function!
    def set_below(self, below):
        self.below = below

    # Returns the tile to the left of this tile
    def get_left(self):
        return self.left

    # Sets the tile to the left of this tile. This is done for you. DO NOT use this function!
    def set_left(self, left):
        self.left = left

    # Returns the tile to the right of this tile
    def get_right(self):
        return self.right

    # Sets the tile to the right of this tile. This is done for you. DO NOT use this function!
    def set_right(self, right):
        self.right = right
    
    # Returns the status of the tile as a string
    def __str__(self) -> str:
        return f"{['W', 'U', 'V'][self.status]}"
  

# Environment setup
class Environment:

    def __init__(self):

        # 2d array of tiles
        self.map = []

        with open(MAP_FILE, "r") as mapFile:
            # add code here to work with the file
            lines = mapFile.readlines()

            mapArray = [list(line.strip()) for line in lines]

        # validate map
        for row in mapArray:
            if len(row) != len(mapArray[0]):
                raise Exception("Map is not rectangular")
            for char in row:
                if char not in {'U', 'V', 'W'}:
                    raise Exception("Map contains invalid characters")

        # create array of tiles to represent environment
        for r, row in enumerate(mapArray):
            rowTiles = []
            for c, colChar in enumerate(row):
                rowTiles.append(
                    Tile({
                        'U': UNVISITED,
                        'V': VISITED,
                        'W': WALL
                    }[colChar], r, c))
            self.map.append(rowTiles)

        # set neighbors
        for r in range(len(self.map)):
            for c in range(len(self.map[0])):
                if r > 0:
                    self.map[r][c].set_above(self.map[r - 1][c])
                if c > 0:
                    self.map[r][c].set_left(self.map[r][c - 1])
                if r < len(self.map) - 1:
                    self.map[r][c].set_below(self.map[r + 1][c])
                if c < len(self.map[0]) - 1:
                    self.map[r][c].set_right(self.map[r][c + 1])
        
        # keeps a savestate of the original map incase we run multiple iterations
        self.original_map = copy.deepcopy(self.map)

    # Sets a tile's status to VISITED. This is done for you. DO NOT use this function!
    def visitTile(self, tile: Tile):
        tile.set_status(VISITED)

    # resets environment for multiple simulations. DO NOT use this function!
    def reset_map(self):
        self.map = copy.deepcopy(self.original_map)
    
    # Formats each row of the environment as a comma-separated list of tile-statuses ('U', 'V', or 'W'),
    # where each row is separated by a newline. Used for testing if custom maps are parsed properly
    def __str__(self) -> str:
        return str(list(list(tile.__str__() for tile in row) for row in self.map)).replace("],", "]\n")



class Robot:

    # Constructs a robot given a Grid, environment and starting position (always top left of environment)
    def __init__(self, grid, env: Environment, pos: Tile):
        self.grid = grid
        self.env = env
        self.pos = pos
        self.x = 0
        self.y = 0
        self.grid.add_visited(pos)

    # This is the function you will implement to determine your robot's movement.
    def nextMove(self):
        """
        This function should return the next move direction as a string.
        Allowed directions are: MOVE_UP, MOVE_RIGHT, MOVE_DOWN, MOVE_LEFT, STAY_STILL.
        """
        # TODO: Implement the movement algorithm
        # return random.choice(list(DIRECTIONS.keys()))  # Random move for starter
        above = self.pos.get_above()
        below = self.pos.get_below()
        right = self.pos.get_right()
        left = self.pos.get_left()

        # Sample algorithm (to be removed)
        if(below and below.get_status() != WALL and below.get_status() == UNVISITED):
            return MOVE_DOWN
        elif (right and right.get_status() != WALL and right.get_status() == UNVISITED):
            return MOVE_RIGHT
        elif (above and above.get_status() != WALL and above.get_status() == UNVISITED):
            return MOVE_UP
        elif (left and left.get_status() != WALL and left.get_status() == UNVISITED):
            return MOVE_LEFT
        else:
            return random.choice(list(DIRECTIONS.keys()))

    # Moves the robot in the grid based on your nextMove() function. DO NOT use or edit this function!
    def move(self):
        direction = self.nextMove()
        dx, dy = DIRECTIONS[direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(self.env.map) and 0 <= new_y < len(self.env.map[0]) and \
                                    (self.env.map[new_x][new_y]).get_status() != WALL:
            self.x = new_x
            self.y = new_y
            self.pos = self.env.map[new_x][new_y]
            self.grid.add_visited(self.pos)
        
        if VISUALIZE:
            self.grid.update()

class Grid:
    def __init__(self, master, env: Environment):
        self.master = master
        self.env = env
        self.move = 0
        self.wall_count = 0
        self.visited = set()
        self.pre_visited = 0
        self.robot = Robot(self, self.env, self.env.map[0][0]) # sets starting point in top left corner
        self.initialize_sets()

        if VISUALIZE:
            self.canvas = tk.Canvas(master, width=len(env.map[0])*TILE_SIZE,
                                    height=len(env.map)*TILE_SIZE)
            self.canvas.pack()
            self.update()
    
    # To be used by Robot's move() function to keep track of visited tiles. Student should not use this.
    def add_visited(self, tile):
        self.visited.add(tile)
        self.env.visitTile(tile)

    def initialize_sets(self):
        for row in self.env.map:
            for tile in row:
                if (tile.get_status() == VISITED):
                    self.add_visited(tile)
                    self.pre_visited += 1
                elif (tile.get_status() == WALL):
                    self.wall_count += 1
    
    # resets grid for multiple simulations
    def reset_grid(self):
        self.env.reset_map()
        self.move = 0
        self.visited = set()
        self.pre_visited = 0
        self.wall_count = 0
        self.robot = Robot(self, self.env, self.env.map[0][0])
        self.initialize_sets()

    def update(self):
        self.canvas.delete('all')
        for y in range(len(self.env.map)):
            for x in range(len(self.env.map[0])):
                tile = self.env.map[y][x]
                color = '#55AEF1' # color taken from Zebra's site
                if tile.get_status() == WALL:
                    color = 'black'
                elif tile == self.robot.pos:
                    color = 'red'
                elif tile.get_status() == VISITED:
                    color = 'white'
                self.canvas.create_rectangle(x*TILE_SIZE, y*TILE_SIZE,
                                             (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
                                             fill=color)
    
    # Returns the robot's final stats in a tuple, indexed as follows:
    #
    # 0: number of tiles visited
    # 1: number of possible tiles to visit (i.e., total tiles - walls - tiles that were already visited)
    # 2: Robot's score, calculated as the percent of tiles visited
    def collect_stats(self):
        visit_count = self.visited.__len__() - self.pre_visited
        possible_count = len(self.env.map) * len(self.env.map[0]) - self.wall_count - self.pre_visited
        percent_visited = visit_count / possible_count
        return (visit_count, possible_count, percent_visited)

    def end_screen(self):
        # Count results to see if student passed
        stats = self.collect_stats()
        display_text = f"You have reached {stats[0]} out of {stats[1]} possible tiles.\nYour score: {stats[2] * 100:.2f}%"
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.create_rectangle(0, 0, width, height, fill='black', stipple='gray50')
        self.canvas.create_text(width/2, height/2, text=display_text, fill='white', font=('Helvetica', int(width/30), 'bold'), anchor='s')

    # recursively loops until the robot runs out of moves
    def run(self):
        self.robot.move()
        if(self.move >= MOVES):
            if VISUALIZE:
                self.end_screen()
            return
        self.move += 1
        
        if VISUALIZE:
            self.master.after(DELAY, self.run) # add delay for visualization
        else:
            self.run() # no delay


def main() -> list:

    env = Environment()
    root = tk.Tk()
    grid = Grid(root, env)
    avg_stats = [0, 0, 0] # Average to be calculated after all simulations are complete
                          # (disregard if VISUALIZE == True)

    if VISUALIZE:
        root.title("TileRunner Challenge")
        root.after(500, grid.run)
        root.mainloop()
    else:
        # skip visuals and run a quick simulation for the given number of ITERATIONS
        for i in range(ITERATIONS):
            grid.reset_grid()
            grid.run()
            stats = grid.collect_stats()
            if PRINT_RESULTS:
                print(f"Round {i + 1} results: {stats[0]} tiles visited out of {stats[1]} possible tiles. Score: {stats[2]:.2f}")
            for j in range(3): avg_stats[j] += stats[j]

        for i in range(3): avg_stats[i] /= ITERATIONS
        if PRINT_RESULTS:
            print(f"\nAverage results: {avg_stats[0]:.2f} tiles visited out of {avg_stats[1]:.2f} possible tiles. Score: {avg_stats[2]:.2f}")
    
    return avg_stats # for use by autograder


if __name__ == '__main__':
    main() # let it ripppp
