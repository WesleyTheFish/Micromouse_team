from cell import Cell
from wall import Wall
from colorama import Fore, Back

class Maze:
    def __init__(self, finish:list, size=5, key=False):
        """Creates empty maze for mouse"""
        self.size = size
        self.finish:list = finish
        
        # creates dictionary of Walls
        self.walls = {}
        # vertical walls
        for i in range(0, size*2+1, 2):
            for j in range(size):
                self.walls[(i,j)] = Wall((i, j), False)
        # horizontal walls
        for i in range(1, size*2, 2):
            for j in range(size+1):
                self.walls[(i,j)] = Wall((i, j), True)
       
        # creates dictionary of Cells
        self.cells = {}
        for i in range(size):
            for j in range(size):
                self.cells[(i,j)] = Cell((i,j),self.walls[(i*2,j)], self.walls[(i*2+2,j)], self.walls[(i*2+1,j)], self.walls[(i*2+1,j+1)],weight=size**2+1)
                # raises wall of boarder cells
                if i == 0: self.cells[(i,j)].left.update_wall(True) 
                if i == size-1: self.cells[(i,j)].right.update_wall(True)
                if j == 0: self.cells[(i,j)].top.update_wall(True)
                if j == size-1: self.cells[(i,j)].bottom.update_wall(True)
        
        # sets finish line to weight 0        
        for cell in self.finish:
            self.cells[cell].update_weight(0)

        # edits empty maze to become answer key
        if key:
            self.create_maze_key(size)

    def create_maze_key(self,size):
        """creates actual maze(Never Changes) size = 5 or 16"""
        if size == 5:
            self.cells[(0,0)].bottom.update_wall(True)
            self.cells[(1,0)].bottom.update_wall(True)
            self.cells[(2,1)].left.update_wall(True)
            self.cells[(3,0)].bottom.update_wall(True)
            self.cells[(4,1)].bottom.update_wall(True)
            self.cells[(4,1)].left.update_wall(True)
            self.cells[(2,1)].right.update_wall(True)
            self.cells[(2,2)].right.update_wall(True)
            self.cells[(1,2)].bottom.update_wall(True)
            self.cells[(0,3)].bottom.update_wall(True)
            self.cells[(2,2)].bottom.update_wall(True)
            self.cells[(1,2)].top.update_wall(True)
            self.cells[(1,4)].top.update_wall(True)
            self.cells[(3,4)].top.update_wall(True)
            self.cells[(4,4)].top.update_wall(True)
        elif size == 16:
            self.cells[(0,0)].bottom.update_wall(True)
            self.cells[(1,0)].bottom.update_wall(True)
            self.cells[(2,0)].bottom.update_wall(True)
            self.cells[(3,0)].bottom.update_wall(True)
            self.cells[(4,0)].bottom.update_wall(True)
            self.cells[(5,0)].bottom.update_wall(True)
            self.cells[(7,0)].bottom.update_wall(True)
            self.cells[(8,0)].bottom.update_wall(True)
            self.cells[(10,0)].bottom.update_wall(True)
            self.cells[(12,0)].bottom.update_wall(True)
            self.cells[(13,0)].bottom.update_wall(True)
            self.cells[(6,1)].right.update_wall(True)
            self.cells[(8,1)].right.update_wall(True)
            self.cells[(10,1)].right.update_wall(True)
            self.cells[(11,1)].right.update_wall(True)
            self.cells[(12,1)].right.update_wall(True)
            self.cells[(13,1)].right.update_wall(True)
            self.cells[(14,1)].right.update_wall(True)
            self.cells[(2,2)].top.update_wall(True)
            self.cells[(3,2)].top.update_wall(True)
            self.cells[(4,2)].top.update_wall(True)
            self.cells[(6,2)].top.update_wall(True)
            self.cells[(9,2)].top.update_wall(True)
            self.cells[(10,2)].top.update_wall(True)
            self.cells[(0,2)].right.update_wall(True)
            self.cells[(1,2)].right.update_wall(True)
            self.cells[(3,2)].right.update_wall(True)
            self.cells[(4,2)].right.update_wall(True)
            self.cells[(6,2)].right.update_wall(True)
            self.cells[(7,2)].right.update_wall(True)
            self.cells[(8,2)].right.update_wall(True)
            self.cells[(10,2)].right.update_wall(True)
            self.cells[(12,2)].right.update_wall(True)
            self.cells[(14,2)].right.update_wall(True)
            self.cells[(5,3)].top.update_wall(True)
            self.cells[(6,3)].top.update_wall(True)
            self.cells[(11,3)].top.update_wall(True)
            self.cells[(12,3)].top.update_wall(True)
            self.cells[(13,3)].top.update_wall(True)
            self.cells[(14,3)].top.update_wall(True)
            self.cells[(0,3)].right.update_wall(True)
            self.cells[(1,3)].right.update_wall(True)
            self.cells[(2,3)].right.update_wall(True)
            self.cells[(3,3)].right.update_wall(True)
            self.cells[(5,3)].right.update_wall(True)
            self.cells[(7,3)].right.update_wall(True)
            self.cells[(8,3)].right.update_wall(True)
            self.cells[(9,3)].right.update_wall(True)
            self.cells[(10,3)].right.update_wall(True)
            self.cells[(13,3)].right.update_wall(True)
            self.cells[(6,4)].top.update_wall(True)
            self.cells[(7,4)].top.update_wall(True)
            self.cells[(12,4)].top.update_wall(True)
            self.cells[(2,4)].right.update_wall(True)
            self.cells[(3,4)].right.update_wall(True)
            self.cells[(4,4)].right.update_wall(True)
            self.cells[(8,4)].right.update_wall(True)
            self.cells[(9,4)].right.update_wall(True)
            self.cells[(11,4)].right.update_wall(True)
            self.cells[(13,4)].right.update_wall(True)
            self.cells[(14,4)].right.update_wall(True)
            self.cells[(1,5)].top.update_wall(True)
            self.cells[(2,5)].top.update_wall(True)
            self.cells[(5,5)].top.update_wall(True)
            self.cells[(6,5)].top.update_wall(True)
            self.cells[(7,5)].top.update_wall(True)
            self.cells[(10,5)].top.update_wall(True)
            self.cells[(11,5)].top.update_wall(True)
            self.cells[(13,5)].top.update_wall(True)
            self.cells[(1,5)].right.update_wall(True)
            self.cells[(2,5)].right.update_wall(True)
            self.cells[(7,5)].right.update_wall(True)
            self.cells[(9,5)].right.update_wall(True)
            self.cells[(11,5)].right.update_wall(True)
            self.cells[(14,5)].right.update_wall(True)
            self.cells[(4,6)].top.update_wall(True)
            self.cells[(5,6)].top.update_wall(True)
            self.cells[(6,6)].top.update_wall(True)
            self.cells[(8,6)].top.update_wall(True)
            self.cells[(9,6)].top.update_wall(True)
            self.cells[(11,6)].top.update_wall(True)
            self.cells[(12,6)].top.update_wall(True)
            self.cells[(13,6)].top.update_wall(True)
            self.cells[(15,6)].top.update_wall(True)
            self.cells[(0,6)].right.update_wall(True)
            self.cells[(2,6)].right.update_wall(True)
            self.cells[(3,6)].right.update_wall(True)
            self.cells[(5,6)].right.update_wall(True)
            self.cells[(9,6)].right.update_wall(True)
            self.cells[(13,6)].right.update_wall(True)
            self.cells[(1,7)].top.update_wall(True)
            self.cells[(2,7)].top.update_wall(True)
            self.cells[(7,7)].top.update_wall(True)
            self.cells[(8,7)].top.update_wall(True)
            self.cells[(10,7)].top.update_wall(True)
            self.cells[(11,7)].top.update_wall(True)
            self.cells[(0,7)].right.update_wall(True)
            self.cells[(2,7)].right.update_wall(True)
            self.cells[(3,7)].right.update_wall(True)
            self.cells[(4,7)].right.update_wall(True)
            self.cells[(5,7)].right.update_wall(True)
            self.cells[(6,7)].right.update_wall(True)
            self.cells[(8,7)].right.update_wall(True)
            self.cells[(9,7)].right.update_wall(True)
            self.cells[(12,7)].right.update_wall(True)
            self.cells[(13,7)].right.update_wall(True)
            self.cells[(14,7)].right.update_wall(True)
            self.cells[(11,8)].top.update_wall(True)
            self.cells[(12,8)].top.update_wall(True)
            self.cells[(1,8)].right.update_wall(True)
            self.cells[(2,8)].right.update_wall(True)
            self.cells[(3,8)].right.update_wall(True)
            self.cells[(4,8)].right.update_wall(True)
            self.cells[(5,8)].right.update_wall(True)
            self.cells[(6,8)].right.update_wall(True)
            self.cells[(8,8)].right.update_wall(True)
            self.cells[(9,8)].right.update_wall(True)
            self.cells[(11,8)].right.update_wall(True)
            self.cells[(14,8)].right.update_wall(True)
            self.cells[(1,9)].top.update_wall(True)
            self.cells[(2,9)].top.update_wall(True)
            self.cells[(7,9)].top.update_wall(True)
            self.cells[(10,9)].top.update_wall(True)
            self.cells[(11,9)].top.update_wall(True)
            self.cells[(13,9)].top.update_wall(True)
            self.cells[(14,9)].top.update_wall(True)
            self.cells[(0,9)].right.update_wall(True)
            self.cells[(2,9)].right.update_wall(True)
            self.cells[(5,9)].right.update_wall(True)
            self.cells[(6,9)].right.update_wall(True)
            self.cells[(9,9)].right.update_wall(True)
            self.cells[(11,9)].right.update_wall(True)
            self.cells[(12,9)].right.update_wall(True)
            self.cells[(3,10)].top.update_wall(True)
            self.cells[(4,10)].top.update_wall(True)
            self.cells[(5,10)].top.update_wall(True)
            self.cells[(6,10)].top.update_wall(True)
            self.cells[(8,10)].top.update_wall(True)
            self.cells[(9,10)].top.update_wall(True)
            self.cells[(11,10)].top.update_wall(True)
            self.cells[(12,10)].top.update_wall(True)
            self.cells[(0,10)].right.update_wall(True)
            self.cells[(1,10)].right.update_wall(True)
            self.cells[(9,10)].right.update_wall(True)
            self.cells[(12,10)].right.update_wall(True)
            self.cells[(13,10)].right.update_wall(True)
            self.cells[(14,10)].right.update_wall(True)
            self.cells[(2,11)].top.update_wall(True)
            self.cells[(3,11)].top.update_wall(True)
            self.cells[(4,11)].top.update_wall(True)
            self.cells[(5,11)].top.update_wall(True)
            self.cells[(7,11)].top.update_wall(True)
            self.cells[(8,11)].top.update_wall(True)
            self.cells[(9,11)].top.update_wall(True)
            self.cells[(10,11)].top.update_wall(True)
            self.cells[(11,11)].top.update_wall(True)
            self.cells[(0,11)].right.update_wall(True)
            self.cells[(5,11)].right.update_wall(True)
            self.cells[(6,11)].right.update_wall(True)
            self.cells[(11,11)].right.update_wall(True)
            self.cells[(12,11)].right.update_wall(True)
            self.cells[(13,11)].right.update_wall(True)
            self.cells[(14,11)].right.update_wall(True)
            self.cells[(1,12)].top.update_wall(True)
            self.cells[(2,12)].top.update_wall(True)
            self.cells[(3,12)].top.update_wall(True)
            self.cells[(4,12)].top.update_wall(True)
            self.cells[(7,12)].top.update_wall(True)
            self.cells[(8,12)].top.update_wall(True)
            self.cells[(9,12)].top.update_wall(True)
            self.cells[(0,12)].right.update_wall(True)
            self.cells[(2,12)].right.update_wall(True)
            self.cells[(4,12)].right.update_wall(True)
            self.cells[(5,12)].right.update_wall(True)
            self.cells[(9,12)].right.update_wall(True)
            self.cells[(10,12)].right.update_wall(True)
            self.cells[(11,12)].right.update_wall(True)
            self.cells[(2,13)].top.update_wall(True)
            self.cells[(3,13)].top.update_wall(True)
            self.cells[(6,13)].top.update_wall(True)
            self.cells[(7,13)].top.update_wall(True)
            self.cells[(8,13)].top.update_wall(True)
            self.cells[(9,13)].top.update_wall(True)
            self.cells[(13,13)].top.update_wall(True)
            self.cells[(14,13)].top.update_wall(True)
            self.cells[(15,13)].top.update_wall(True)
            self.cells[(4,13)].right.update_wall(True)
            self.cells[(5,13)].right.update_wall(True)
            self.cells[(7,13)].right.update_wall(True)
            self.cells[(9,13)].right.update_wall(True)
            self.cells[(10,13)].right.update_wall(True)
            self.cells[(0,14)].top.update_wall(True)
            self.cells[(1,14)].top.update_wall(True)
            self.cells[(3,14)].top.update_wall(True)
            self.cells[(12,14)].top.update_wall(True)
            self.cells[(14,14)].top.update_wall(True)
            self.cells[(15,14)].top.update_wall(True)
            self.cells[(1,14)].right.update_wall(True)
            self.cells[(4,14)].right.update_wall(True)
            self.cells[(6,14)].right.update_wall(True)
            self.cells[(8,14)].right.update_wall(True)
            self.cells[(10,14)].right.update_wall(True)
            self.cells[(13,14)].right.update_wall(True)
            self.cells[(1,15)].top.update_wall(True)
            self.cells[(2,15)].top.update_wall(True)
            self.cells[(3,15)].top.update_wall(True)
            self.cells[(5,15)].top.update_wall(True)
            self.cells[(6,15)].top.update_wall(True)
            self.cells[(7,15)].top.update_wall(True)
            self.cells[(8,15)].top.update_wall(True)
            self.cells[(9,15)].top.update_wall(True)
            self.cells[(10,15)].top.update_wall(True)
            self.cells[(12,15)].top.update_wall(True)
            self.cells[(13,15)].top.update_wall(True)
            self.cells[(14,15)].top.update_wall(True)

    def update_weights(self, root:Cell, current:Cell):
        """updates all weights of the maze"""

        if current:
            # set weight of cur cell to one higher than the cell it came from
            current.update_weight(root.weight+1)

        # if current is None, then the function is being called for the first time
        current = current or root
        x,y = current.address

        if not current.left.is_blocked:
            dest:Cell = self.cells[(x-1,y)]
            if current.weight+1 < dest.weight:
                self.update_weights(current, dest)
        if not current.right.is_blocked:
            dest:Cell = self.cells[(x+1,y)]
            if current.weight+1 < dest.weight:
                self.update_weights(current, dest)
        if not current.top.is_blocked:
            dest:Cell = self.cells[(x,y-1)]
            if current.weight+1 < dest.weight:
                self.update_weights(current, dest)
        if not current.bottom.is_blocked:
            dest:Cell = self.cells[(x,y+1)]
            if current.weight+1 < dest.weight:
                self.update_weights(current, dest)
        return None
    
    def wipe_weights(self):
        """resets all weights of the maze"""
        for i in self.cells:
            self.cells[i].update_weight(self.size**2+1)
        for i in self.finish:
            self.cells[i].weight = 0

    def print_maze(self, highlight, done=False):
        """either prints the maze with weights and color-coded walls or the maze with the path the mouse took"""
        
        color = Back.RESET
        # runs through each row
        for j in range(self.size):
            top_row = ""
            middle_row = ""
            # runs through each cell in the row
            for i in range(self.size):
                top_row +=  " " + self.cells[(i,j)].top.print_wall()

                # sets color of finish cell and current location cell
                if (i,j) in self.finish:
                    color = Back.YELLOW
                elif done:
                    if (i,j) in highlight:
                        color = Back.CYAN
                elif not done:
                    if highlight == (i,j):
                        color = Back.CYAN
                else:
                    color = Back.RESET

                middle_row += Back.RESET + self.cells[(i,j)].left.print_wall()

                # prints either the weight of the cell or a * if the path is being printed
                if done:
                    middle_row += Fore.WHITE + color + "{:^4}".format("*")
                else:
                    middle_row += Fore.WHITE + color + self.cells[(i,j)].print_cell()

                color = Back.RESET
            
            # prints the last wall of the row(edge case of loop)
            middle_row += Back.RESET + self.cells[(self.size-1,j)].right.print_wall()
            print(top_row)
            print(middle_row)

        # prints the last row of the maze(edge case of loop)
        for i in range(self.size):
            print(" " + self.cells[(i,self.size-1)].bottom.print_wall(), end="")
        print()
