import colorama
from colorama import Fore, Back, Style
from wall import Wall


class Cell:
    def __init__(self, address, left:Wall, right:Wall, top:Wall, bottom:Wall, weight):
        self.weight = weight
        self.address = address

        # Surrounding Walls
        self.left:Wall = left
        self.right:Wall = right
        self.top:Wall = top
        self.bottom:Wall = bottom

    def update_weight(self, num):
        """changes weight of Cell to given value"""
        self.weight = num

    def print_cell(self):
        """Returns weight of cell centered in 4 total spaces(not in color cause it was being weird)"""
        return "{:^4}".format(self.weight)