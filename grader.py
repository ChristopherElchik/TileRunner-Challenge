import random
import tkinter as tk
import copy
import tilerunner as tr

# Number of maps to grade (All numbers from 1 to NUM_MAPS will be substituted into 'MAP_XX.txt')
NUM_MAPS = 10

# map setter
def set_map(mapName:str):
    tr.MAP_FILE = mapName


def main():
    # force no visualization
    tr.VISUALIZE = False

    # Only print grader's results1
    tr.PRINT_RESULTS = False
    tr.ITERATIONS = 100
    tr.MOVES = 200

    # keep track of average score against every map
    avg_score = 0

    for map_num in range(1, NUM_MAPS + 1):

        map_name = f"MAP_{map_num:2}.txt".replace(' ', '0')
        set_map(map_name)
        stats = tr.main()
        print(f"Average performance on {map_name}: {stats[0]:.2f} tiles reached out of {stats[1]:.2f} possible tiles. Score: {stats[2]*100:.2f}")
        avg_score += stats[2]
    avg_score /= NUM_MAPS

    print(f"Student's average score: {avg_score:.2f}")
    print(f"Number of points earned for the challenge: {avg_score * 250000:.0f}")


if __name__ == '__main__':
    main()