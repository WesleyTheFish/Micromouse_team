from mouse import Mouse
from maze import Maze
from colorama import Fore
import random

"""5 X 5 maze"""
# MAZE_SIZE = 5
# start=(0,0)
# finish=[(4,4)]

"""16 X 16 competition maze(random start)"""
MAZE_SIZE = 16
# start= random.choice([(0,0),(0,MAZE_SIZE-1),(MAZE_SIZE-1,0),(MAZE_SIZE-1,MAZE_SIZE-1)])
start=(0,15)
finish=[(7,7),(8,7),(7,8),(8,8)]

# create the answer key maze
maze = Maze(finish, size=MAZE_SIZE, key=True)

# creates mouse
mouse = Mouse(start, finish, size=MAZE_SIZE, maze_key=maze)

path = mouse.solve_maze()



print(Fore.GREEN + "done!")
print(f"Mouse position: {Fore.WHITE}{mouse.position}")
print(f"{Fore.GREEN}Mouse path {len(path)} steps: {Fore.WHITE}{path}")

# print the maze with the path the mouse took
print(f"{Fore.GREEN}Mouse path:{Fore.WHITE}")
maze.print_maze(path, done=True)