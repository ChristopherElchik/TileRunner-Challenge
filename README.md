# TileRunner-Challenge
Tile Runner challenge for Zebra Robotics

This challenge is meant to serve as an introduction to AI for students who are learning python. The students are given an environment and a 'robot', where the goal is to program the robot to traverse any given environment and cover as many tiles as possible. This introduces students to agent-environment interactions, as well as the challenges of pathfinding and algorithms in AI.

## Provided Files

### tilerunner.py

This file contains a comprehensive guide for students to program their robots for the tilerunner challenge. It includes all the starter code for setting up the robot's environment, with instructions for the students to create their algorithm in the nextMove() function of the Robot class. We encourage students to create their own test cases for their robots, as we included a map parser within tilerunner.py to interpret any given map (stored as a .txt file), which is very simple/intuitive to create. See the start of tilerunner.py for the full description.

### grader.py

This file is for teaching staff to determine the score of a student's robot by running it on all 20 test environments. Students are scored by averaging their performance of 100 iterations over each of the 20 test environments. This score (0 <= score <= 1) is multiplied by 250,000 points, where students can score a maximum of 250,000 points for this assignment.

### maps/*

All files in the maps folder are example maps that the students can use to test their robots. Maps 1-20 will be used to score the robot's performance. Note that the students will be given maps 1-10, where maps 11-20 will be hidden test cases to incentivize adaptable algorithms over hard-coded movements.
