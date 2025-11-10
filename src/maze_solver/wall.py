import colorama
from colorama import Fore, Back, Style

class Wall:
    def __init__(self, address, isHorz):
        self.address = address
        self.is_blocked = False
        self.horz_char = "—"
        self.vert_char = "|"

        # used for correct printing
        self.isHorz = isHorz
  
    def update_wall(self,is_blocked):
        """sets wall to being there"""
        self.is_blocked = is_blocked

    def print_wall(self,width=4):
        """returns characters of the wall(red if it is there and white if not)"""
        self.color = Fore.RED if self.is_blocked else Fore.WHITE

        # if wall is up, print the wall, else print empty space
        if self.is_blocked:
            self.horz_char = "—"
            self.vert_char = "|"
        else:
            self.horz_char = " "
            self.vert_char = " "
            

        return self.color + (self.horz_char*width) if self.isHorz else self.color + self.vert_char