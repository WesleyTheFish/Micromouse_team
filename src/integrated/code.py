from mouse import Mouse


"""16 X 16 competition maze(random start)"""
MAZE_SIZE = 16
start=(0,0)
finish=[(7,7),(8,7),(7,8),(8,8)]

mouse = Mouse(start, finish, size=MAZE_SIZE)

mouse.solve_maze()

