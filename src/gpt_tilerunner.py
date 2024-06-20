import random
import tkinter as tk

# Constants
GRID_SIZE = 10  # 10x10 grid
TILE_SIZE = 50  # Size of each tile in pixels

# Directions
DIRECTIONS = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
    'none': (0, 0)
}

class Robot:
    def __init__(self, grid):
        self.grid = grid
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

        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and \
                                    (new_x, new_y) not in self.grid.walls:
            self.x = new_x
            self.y = new_y
            self.visited.add((self.x, self.y))
        self.grid.update()

class Grid:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=GRID_SIZE*TILE_SIZE,
                                height=GRID_SIZE*TILE_SIZE)
        self.canvas.pack()
        self.walls = set()
        self.robot = Robot(self)
        self.create_walls()
        self.update()

    def create_walls(self):
        # Randomly create walls
        for _ in range(15):
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            self.walls.add((x, y))

    def update(self):
        self.canvas.delete('all')
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
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
                

    def run(self):
        self.robot.move()
        self.master.after(500, self.run)

def main():
    root = tk.Tk()
    root.title("Robot Grid Navigation")
    grid = Grid(root)
    root.after(500, grid.run)
    root.mainloop()

if __name__ == "__main__":
    main()