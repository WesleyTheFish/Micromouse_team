from rich.console import Console
from rich.style import Style

def draw_test_at_coordinates():
    console = Console()

    console.clear()

    text_style = Style(color="red")

    console.print("Hello, [bold blue]World[/bold blue]!", style=text_style)

def dup_test():
    # index out of bounds if the last element is a duplicate(issue should never happen)
    path = [(22,22),(0,0),(1,1),(2,2),(1,1),(0,0),(23,34),(3,3),(8,8),(3,3),(4,4)]
    branches = []


    for cord in range(1,len(path),1):
        for check in range(cord):
            if path[cord] == path[check] and path[cord+1] != path[check-1]:
                branches.append((check, cord))

    branches.reverse()

    for branch in branches:
        first,last = branch
        for _ in range(first, last, 1):
            path.remove(path[first])

    print(path)

x = [1,2,3,4,5,6,7,8,9,10]
for x in x[0:3]:
    if x > 2:
        print(x)


# draw_test_at_coordinates()