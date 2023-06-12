import random
from colorama import init, Fore

game_level = 2
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXXXXX      E   XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "XP  B    XX  XXX        XX",
    "XXXXXX  XX  XXX T      XX",
    "XXXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX        XXXX  XXXXX",
    "X  XXX  XXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X T E            XXXXXXXX",
    "XXXXXXXXXXXX     XXXXXETX",
    "XXXXXXXXXXXXXXX  XXXXX  X",
    "XXX  XXXXXXXXXX         X",
    "XXX                     X",
    "XX          EXXXXXXXXXXXX",
    "XXXXXXXXXX  XXXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX   XXXXX        B      X",
    "XX   XXXXXXXXXXXXX  XXXXX",
    "XX    XXXXXXXXXXXX  XXXXX",
    "XXT          XXXX       X",
    "XXXE       B            TX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Iterate through each character in the list and replace spaces with 'S'
level_1 = ["".join(['S' if char == ' ' else char for char in line]) for line in level_1]


def generate_random_maze(layout, level):
    width = len(layout[0]) + 7 * (level - 1)
    height = len(layout) + 1 * (level - 1)
    maze = [['X' for _ in range(width)] for _ in range(height)]
    count_b = 0
    count_t = 0
    count_e = 0

    space_coordinates = []

    # Generate vertical alignments of spaces
    for x in range(1, width - 1, random.randint(1, 6)):
        for y in range(1, height - 1):
            if random.random() < 0.5:
                for z in range(1, y):
                        maze[z][x] = 'S'  # Replace ' ' with 'S'
                        space_coordinates.append((z, x))
                        
    # Generate horizontal alignments of spaces
    for y in range(1, height - 1, random.randint(1, 7)):
        for x in range(1, width - 1):
            if random.random() < 0.3:
                for z in range(1, x):
                            maze[y][z] = 'S' 
                            space_coordinates.append((y, z))
   
    while count_b < 3 * level:
        random_y = random.randint(0, height - 1)
        random_x = random.randint(0, width - 1)
        if maze[random_y][random_x] == 'S':  
            maze[random_y][random_x] = 'B'
            space_coordinates.append((random_y, random_x))
            count_b += 1

    while count_e < 3 * level:
        random_y = random.randint(5, height - 1)
        random_x = random.randint(5, width - 1)
        if maze[random_y][random_x] == 'S':  
            maze[random_y][random_x] = 'E'
            space_coordinates.append((random_y, random_x))

            count_e += 1

    while count_t < 5* level:
        random_y = random.randint(0, height - 1)
        random_x = random.randint(0, width - 1)
        if maze[random_y][random_x] == 'S': 
            maze[random_y][random_x] = 'T'
            space_coordinates.append((random_y, random_x))

            count_t += 1

    # Place P at a random location
    # Place 'P' away from 'E'
    p_placed = False
    while not p_placed:
        offset_x = random.randint(-1, 1)
        offset_y = random.randint(-1, 1)
        new_x = random_x + offset_x
        new_y = random_y + offset_y
        random_y = random.randint(0, height - 1)
        random_x = random.randint(0, width - 1)
        if (
            maze[random_y][random_x] == 'S' and  # Replace ' ' with 'S'
            abs(random_x - new_x) > 1 and
            abs(random_y - new_y) > 1
        ):
            maze[random_y][random_x] = 'P'
            p_placed = True

    return maze, space_coordinates


game_levels = 3
maze_list = []
maze_dimensions = []

for level in range(1, game_levels + 1):
    if level == 1:
        maze, space_coordinates = generate_random_maze(level_1, level)
    else:
        maze, space_coordinates = generate_random_maze(level_1, level)
    maze_list.append(maze)
    maze_dimensions.append((len(maze[0]), len(maze)))
    




blank_maze = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]
