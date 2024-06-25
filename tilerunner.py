# MAIN FILE FOR STUDENTS
import random
import tkinter as tk


# Toggles visualization of robot. Set this to false to disable the
# visual simulation. 
VISUALIZE = True

# This is the file of the map to be used. You can change this to
# use any map you want. Feel free to test your robot on custom maps!
#
# Note: Your robot will ALWAYS start in the top left corner.
MAP_FILE = "MAP_01.txt"

# Size of each tile in pixels (Feel free to adjust to fit your screen)
TILE_SIZE = 50

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

# Directions
DIRECTIONS = {
    MOVE_UP: (-1, 0),
    MOVE_DOWN: (1, 0),
    MOVE_LEFT: (0, -1),
    MOVE_RIGHT: (0, 1),
    STAY_STILL: (0, 0)
}

# Number of moves the user can make until the program cuts off
ITERATIONS = 250

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

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_row(self):
        return self.row

    def set_row(self, row: int):
        self.row = row

    def get_col(self):
        return self.col

    def set_col(self, col: int):
        self.col = col

    def get_above(self):
        return self.above

    def set_above(self, above):
        self.above = above

    def get_below(self):
        return self.below

    def set_below(self, below):
        self.below = below

    def get_left(self):
        return self.left

    def set_left(self, left):
        self.left = left

    def get_right(self):
        return self.right

    def set_right(self, right):
        self.right = right
    
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

    def visitTile(self, tile: Tile):
        tile.set_status(VISITED)
    
    # Formats each row of the environment as a comma-separated list of tile-statuses ('U', 'V', or 'W'),
    # where each row is separated by a newline. Used for testing if custom maps are parsed properly
    def __str__(self) -> str:
        return str(list(list(tile.__str__() for tile in row) for row in self.map)).replace("],", "]\n")



class Robot:
    def __init__(self, grid, env: Environment, pos: Tile):
        self.grid = grid
        self.env = env
        self.pos = pos
        self.x = 0
        self.y = 0
        self.grid.add_visited(pos)

    def nextMove(self):
        """
        This function should return the next move direction as a string.
        Allowed directions are: MOVE_UP, MOVE_RIGHT, MOVE_DOWN, MOVE_LEFT, STAY_STILL.
        """
        # TODO: Implement the movement algorithm
        return random.choice(list(DIRECTIONS.keys()))  # Random move for starter

    def move(self):
        direction = self.nextMove()
        dx, dy = DIRECTIONS[direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(self.env.map[0]) and 0 <= new_y < len(self.env.map) and \
                                    (self.env.map[new_y][new_x]).get_status() != WALL:
            self.x = new_x
            self.y = new_y
            self.pos = self.env.map[new_y][new_x]
            self.grid.add_visited(self.pos)
        self.grid.update()

class Grid:
    def __init__(self, master, env: Environment):
        self.master = master
        self.env = env
        self.iteration = 0
        self.canvas = tk.Canvas(master, width=len(env.map[0])*TILE_SIZE,
                                height=len(env.map)*TILE_SIZE)
        self.canvas.pack()
        self.wall_count = 0
        self.visited = set()
        self.robot = Robot(self, self.env, self.env.map[0][0]) # sets starting point in top left corner
        self.initialize_sets()
        self.update()
    
    # To be used by Robot to add visited tiles
    def add_visited(self, tile):
        self.visited.add(tile)
        self.env.visitTile(tile)

    def initialize_sets(self):
        for row in self.env.map:
            for tile in row:
                if (tile.get_status() == VISITED):
                    self.add_visited(tile)
                elif (tile.get_status() == WALL):
                    self.wall_count += 1

    def update(self):
        self.canvas.delete('all')
        for y in range(len(self.env.map)):
            for x in range(len(self.env.map[0])):
                tile = self.env.map[y][x]
                color = '#55AEF1'
                if tile.get_status() == WALL:
                    color = 'white'
                elif tile == self.robot.pos:
                    color = 'red'
                elif tile.get_status() == VISITED:
                    color = 'black'
                self.canvas.create_rectangle(x*TILE_SIZE, y*TILE_SIZE,
                                             (x+1)*TILE_SIZE, (y+1)*TILE_SIZE,
                                             fill=color)
    
    # Returns the robot's final stats in a tuple, indexed as follows:
    #
    # 0: number of tiles visited
    # 1: number of possible tiles to visit (i.e., total tiles - walls)
    # 2: Robot's score, calculated as the percent of tiles visited
    def collect_stats(self):
        visit_count = self.visited.__len__()
        possible_count = len(self.env.map) * len(self.env.map[0]) - self.wall_count
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

    def run(self):
        self.robot.move()
        if(self.iteration >= ITERATIONS):
            self.end_screen()
            return
        self.iteration += 1
        self.master.after(20, self.run)


def main():
    env = Environment()
    root = tk.Tk()
    root.title("TileRunner Challenge")
    grid = Grid(root, env)
    root.after(500, grid.run)
    root.mainloop()
    

if __name__ == '__main__':
    main()
