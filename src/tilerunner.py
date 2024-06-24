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

    def visit(self):
        self.status = VISITED

    def __str__(self) -> str:
        return f"Tile at ({self.row}, {self.col})"
  

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


class Robot:
    def __init__(self, grid, env: Environment, pos: Tile):
        self.grid = grid
        self.env = env
        self.pos = pos
        self.x = 0
        self.y = 0
        self.visited = set()
        self.visited.add((self.x, self.y))

    def nextMove(self):
        """
        This function should return the next move direction as a string.
        Allowed directions are: 'up', 'down', 'left', 'right', 'none'.
        """
        # TODO: Implement the movement algorithm
        return random.choice(list(DIRECTIONS.keys()))  # Random move for starter

    def move(self):
        direction = self.nextMove()
        dx, dy = DIRECTIONS[direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(self.env.map[0]) and 0 <= new_y < len(self.env.map) and \
                                    (new_x, new_y) not in self.grid.walls:
            self.x = new_x
            self.y = new_y
            self.visited.add((self.x, self.y))
        self.grid.update()

class Grid:
    def __init__(self, master, env: Environment):
        self.master = master
        self.env = env
        self.canvas = tk.Canvas(master, width=len(env.map[0])*TILE_SIZE,
                                height=len(env.map)*TILE_SIZE)
        self.canvas.pack()
        self.walls = set()
        self.robot = Robot(self, env[0][0]) # sets starting point in top left corner
        self.create_walls()
        self.update()

    def create_walls(self):
        # Randomly create walls
        # for _ in range(15):
        #     x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        #     self.walls.add((x, y))
        pass

    def update(self):
        self.canvas.delete('all')
        for x in range(len(self.env.map[0])):
            for y in range(len(self.env.map)):
                color = 'white'
                if (x, y) in self.walls:
                    color = 'black'
                elif (x, y) == (self.robot.x, self.robot.y):
                    color = 'red'
                elif (x, y) in self.robot.visited:
                    color = 'green'
                self.canvas.create_rectangle(y*TILE_SIZE, x*TILE_SIZE,
                                             (y+1)*TILE_SIZE, (x+1)*TILE_SIZE,
                                             fill=color)


def main():
    root = tk.Tk()
    root.title("TileRunner Challenge")
    env = Environment()
    grid = Grid(root, env)
    root.after(500, grid.run)
    root.mainloop()
    

if __name__ == '__main__':
    main()
