# documentation stuff
import tkinter as tk
from tkinter import NORMAL, messagebox
import random

# Toggles visualization of robot. Set this to false to disable the
# visual simulation.
VISUALIZE = True

# This is the file of the map to be used. You can change this to
# use any map you want. Feel free to test your robot on custom maps!
MAP_FILE = "MAP_01.txt"

# options for window size
SMALL_WINDOW = 0
NORMAL_WINDOW = 1
BIG_WINDOW = 2

# Set the simulation's window size to either BIG_WINDOW, NORMAL_WINDOW
# or SMALL_WINDOW. Default is NORMAL_WINDOW.
WINDOW_SIZE = NORMAL_WINDOW

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

class Robot:

  def __init__(self):
    self.currentPos = None # will be assigned by environment

  def getCurrentPos(self):
    return self.currentPos

  def setCurrentPos(self, pos:Tile):
    self.currentPos = pos

  # STUDENT WILL IMPLEMENT THIS FUNCTION
  def nextMove(self, environment):

    # complete implementation below

    return STAY_STILL


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

    #

  def visitTile(self, tile: Tile):
    tile.set_status(VISITED)

class VisualInterface:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.tiles = []

        for r in range(rows):
            row_tiles = []
            for c in range(cols):
                tile = tk.Label(root, text="", width=2, height=1, relief="solid")
                tile.tk_setPalette(background="white")
                tile.grid(row=r, column=c)
                row_tiles.append(tile)
            self.tiles.append(row_tiles)

    def updateTileStatus(self, row, col, status):
        self.tiles[row][col].configure(text=status)



def main():
  # with open(MAP_FILE, "r") as mapFile:
  #   # add code here to work with the file
  #   lines = mapFile.readlines()

  # mapArray = [list(line)[:-1] for line in lines]
  # print(mapArray)
  # env = Environment()
  # print(env.map[1][2].get_status())
  robot = Robot()
  env = Environment()
  visualizer = VisualInterface(tk.Tk(), len(env.map), len(env.map[0]))




main()
