from maze import Maze
from wall import Wall
from cell import Cell

class Mouse:
    def __init__(self, start, finish, maze_key, size=5):
        self.start:list = [start]
        self.position = start
        self.dirct_facing = "east"
        self.finish:list = finish
        self.maze = Maze(finish, size=size,key=False)
        self.maze_key:Maze = maze_key
        self.size = size

    
    def solve_maze(self):
        """through trial and error the mouse explores the maze and returns the shortest path to the finish"""
        path_there = []
        path_back = []

        # runs through the maze twice, once to the finish and once back to the start
        for destination in (self.finish, self.start):

            # changes maze's finish to the start for the return trip
            if destination == self.start:
                self.maze.finish = self.start

            while self.position not in destination:

                # update surrounding wall status
                self.update_walls()

                # update weights of all cells
                self.maze.wipe_weights()
                
                # updates weights of cells(method starts at each finishing square)
                for cord in destination:
                    self.maze.update_weights(self.maze.cells[cord],None)

                self.maze.print_maze(self.position)

                # move mouse to next best Cell
                direction = self.find_next_move()
                self.move(direction)

                # logs the path the mouse took
                if destination == self.finish:
                    path_there.append(self.position)
                else:
                    path_back.append(self.position)

        self.smooth_path(path_there)
        self.smooth_path(path_back)

        # returns the shortest path
        if len(path_back) < len(path_there):
            path_back.reverse()
            return path_back
        else:
            return path_there
    
    def smooth_path(self, path):
        """removes any unnecessary turns in the path"""
        branches = []

        # index out of bounds if the last element is a duplicate(issue should never happen)
        for cord in range(1,len(path),1):
            for check in range(cord):
                if path[cord] == path[check] and path[cord+1] != path[check-1]:
                    branches.append((check, cord))

        branches.reverse()

        for branch in branches:
            first,last = branch
            for _ in range(first, last, 1):
                path.remove(path[first])

    def update_walls(self):
        """mouse looks around and updates it's maze with the wall data surrounding it"""
        # sets value of wall in maze equal to the counterpart in the maze_key
        cur_cell = self.maze.cells[self.position]
        key_cell = self.maze_key.cells[self.position]

        cur_cell.left.update_wall(key_cell.left.is_blocked)
        cur_cell.right.update_wall(key_cell.right.is_blocked)
        cur_cell.top.update_wall(key_cell.top.is_blocked)
        cur_cell.bottom.update_wall(key_cell.bottom.is_blocked)

    def find_next_move(self):
        """takes current position and returns the direction you need to go to get to the next Cell of smallest weight"""
        next_cell = None
        least_num_moves = self.size**2+1

        # list of all surrounding cells possible to get to 
        possible_cells = []
        cell,y = self.position
        if not self.maze.cells[self.position].left.is_blocked: possible_cells.append(self.maze.cells[cell-1,y])
        if not self.maze.cells[self.position].right.is_blocked: possible_cells.append(self.maze.cells[cell+1,y])
        if not self.maze.cells[self.position].top.is_blocked: possible_cells.append(self.maze.cells[cell,y-1])
        if not self.maze.cells[self.position].bottom.is_blocked: possible_cells.append(self.maze.cells[cell,y+1])

        """This is where optimization could happen balancing number of turns to distance traveled"""
        for cell in possible_cells:
            if cell.weight == least_num_moves:
                if self.dirct_facing == self.direct_to_cell(cell):
                    next_cell = cell
                    least_num_moves = cell.weight
            elif cell.weight < least_num_moves:
                least_num_moves = cell.weight
                next_cell = cell

        return self.direct_to_cell(next_cell)
    
    def move(self, direction):
        """Moves the mouse in given direction(makes sure direction is valid)"""
        # checks if the wall is up in the direction the mouse is moving
        if direction == "east":
            assert self.maze.cells[self.position].right.is_blocked == False
        elif direction == "west":
            assert self.maze.cells[self.position].left.is_blocked == False
        elif direction == "north":
            assert self.maze.cells[self.position].top.is_blocked == False
        elif direction == "south":
            assert self.maze.cells[self.position].bottom.is_blocked == False
        else:
            raise ValueError("Invalid direction")

        # moves the mouse
        self.dirct_facing = direction
        if direction == "north":
            self.position = (self.position[0], self.position[1]-1)
        elif direction == "south":
            self.position = (self.position[0], self.position[1]+1)
        elif direction == "east":
            self.position = (self.position[0]+1, self.position[1])
        elif direction == "west":
            self.position = (self.position[0]-1, self.position[1])
        
        # throws error if mouse moves out of bounds of the maze
        if 0 > self.position[0] or self.position[0] > self.maze.size-1 or 0 > self.position[1] or self.position[1] > self.maze.size-1:
            raise ValueError("Mouse has moved out of bounds")
              
    def direct_to_cell(self,destination:Cell):
        """given a desired cell to travel to, returns the direction you would need to travel in to get to it"""
        x,y = destination.address
        a,b = self.position
        
        # cells aligned on y-axis
        if a == x:
            if b > y:
                return "north"
            else:
                return "south"
        else:
            if a > x:
                return "west"
            else:
                return "east"
            