import time
from classes import Space, Treasure, Box, Pen
from levels import maze_list
from static import *
from utility import *


difficulty = 1


def start_game(game_level):
    # Get the dimensions of the maze
    maze_dimensions = [(len(maze[0]), len(maze)) for maze in maze_list]

    # Calculate the maximum dimensions of the maze
    max_width = max(dimensions[0] for dimensions in maze_dimensions)
    max_height = max(dimensions[1] for dimensions in maze_dimensions)

    # Calculate the width and height of the screen
    grid_block_size = 30  # Adjust the block size as desired
    screen_width = max_width * grid_block_size
    screen_height = max_height * grid_block_size + 90

    # Create the turtle screen with the adjusted dimensions
    wn = turtle.Screen()
    wn.title('Speedscapes: Portal Jump')
    wn.bgcolor("light pink")
    wn.setup(width=screen_width, height=screen_height)
    wn.tracer(35)

    trigger_assign_gif(wn)

    # game status
    levelsList = []
    walls = []
    treasures = []
    boxes = []
    enemies = []
    space = []

    class Player(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.safe_teleport_distance = 1
            self.speed(10)
            self.new_y_cor = None
            self.new_x_cor = None
            self.portal_x = None
            self.portal_y = None
            self.check = None
            self.penup()
            self.speed(0)
            self.lives = 10
            self.name = 'Player'
            self.shape("player/right.gif")
            self.gold = 0
            self.current_move = "right"
            self.powerup = 5
            self.is_being_attacked = False
            self.hideturtle()
            self.portal = Portal()

        def move_up(self):
            self.current_move = "up"
            new_x_cor = self.xcor()
            new_y_cor = self.ycor() + grid_block_size
            if check_wall_collision(new_x_cor, new_y_cor, walls):
                self.goto(new_x_cor, new_y_cor)
                self.shape("player/up.gif")
                player_position_bidirectional_destination = (
                    new_x_cor, new_y_cor)

        def move_down(self):
            self.current_move = "down"
            new_x_cor = self.xcor()
            new_y_cor = self.ycor() - grid_block_size
            check = check_wall_collision(new_x_cor, new_y_cor, walls)
            if check:
                self.goto(self.xcor(), self.ycor() - grid_block_size)
                self.shape("player/down.gif")
                player_position_bidirectional_destination = (
                    new_x_cor, new_y_cor)

        def move_left(self):
            self.current_move = "left"
            new_x_cor = self.xcor() - grid_block_size
            new_y_cor = self.ycor()
            check = check_wall_collision(new_x_cor, new_y_cor, walls)
            if check:
                self.goto(new_x_cor, new_y_cor)
                self.shape("player/left.gif")
                player_position_bidirectional_destination = (
                    new_x_cor, new_y_cor)

        def move_right(self):
            self.current_move = "right"
            new_x_cor = self.xcor() + grid_block_size
            new_y_cor = self.ycor()
            check = check_wall_collision(new_x_cor, new_y_cor, walls)
            if check:
                self.goto(new_x_cor, new_y_cor)
                self.shape("player/right.gif")
                player_position_bidirectional_destination = (
                    new_x_cor, new_y_cor)

        def teleport(self):
            
            if self.current_move == "right":
                self.new_x_cor = self.xcor() + (grid_block_size * self.safe_teleport_distance)
                self.new_y_cor = self.ycor()
            elif self.current_move == "left":
                self.new_x_cor = self.xcor() - (grid_block_size * self.safe_teleport_distance)
                self.new_y_cor = self.ycor()
            elif self.current_move == "up":
                self.new_x_cor = self.xcor()
                self.new_y_cor = self.ycor() + (grid_block_size * self.safe_teleport_distance)
            elif self.current_move == "down":
                self.new_x_cor = self.xcor()
                self.new_y_cor = self.ycor() - (grid_block_size * self.safe_teleport_distance)
            self.is_safe_teleport(self.new_x_cor, self.new_y_cor)

        def is_attacked(self):
            self.is_being_attacked = True

        def is_safe_teleport(self, x, y):
            if check_wall_collision(x, y, walls):
                if self.is_being_attacked and (x, y) not in current_enemy_location:
                    self.safe_teleport_distance += 5  # Increment the safe teleport distance
                    self.portal_x = x
                    self.portal_y = y
                    self.portal.set_position(x, y)
                    self.switch_teleport()
                elif not any((x, y) in enemy_location for enemy_location in current_enemy_location):
                    self.portal_x = x
                    self.portal_y = y
                    self.portal.set_position(x, y)
                    self.safe_teleport_distance = 1
            else:
                self.safe_teleport_distance += 1
                self.teleport()
            player_position_bidirectional_destination = (x, y)

        def switch_teleport(self):
            self.setposition(self.portal_x, self.portal_y)
            self.portal.hide()
            self.is_being_attacked = False
            self.safe_teleport_distance = 1

        def hide(self):
            self.hideturtle()

        def return_player_ycor(self):
            return self.ycor()

        def return_player_xcor(self):
            return self.xcor()

    # classes
    class Portal(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.x = None
            self.y = None
            self.penup()
            self.speed(0)
            self.shape("misc/portal.gif")
            self.hideturtle()

        def set_position(self, x, y):
            self.goto(x, y)
            self.showturtle()

        def hide(self):
            self.hideturtle()

    class Enemy(turtle.Turtle):
        def __init__(self, x, y):
            turtle.Turtle.__init__(self)
            self.speed(0)
            self.color('#362020')
            self.movement = grid_block_size/2
            self.penup()
            self.gold = 50
            self.name = 'Enemy'
            self.shape(f"enemy/level{game_level}/right.gif")
            self.setposition(x, y)
            self.direction = set_direction()
            self.x = x
            self.y = y
            

        def change_direction(self):
            if self.direction == 'up':
                dx = 0
                dy = grid_block_size
            elif self.direction == 'down':
                dx = 0
                dy = -grid_block_size
            elif self.direction == 'left':
                dx = -grid_block_size
                dy = 0
                self.shape(f"enemy/level{game_level}/left.gif")
            elif self.direction == 'right':
                dx = grid_block_size
                dy = 0
                self.shape(f"enemy/level{game_level}/right.gif")
            move_to_x = self.xcor() + dx
            move_to_y = self.ycor() + dy
            if self.path:
                next_node = self.path.pop(0)
                self.goto(next_node[0], next_node[1])
                self.update_direction(next_node)

            else:
                if self.distance(player) < (difficulty * 1000):
                    if player.xcor() < self.xcor():
                        self.direction = 'left'

                    elif player.xcor() > self.xcor():
                        self.direction = 'right'

                    elif player.ycor() < self.ycor():
                        self.direction = 'down'

                    elif player.ycor() > self.ycor():
                        self.direction = 'up'
                check = check_wall_collision(move_to_x, move_to_y, walls)
                if check:
                    self.goto(move_to_x, move_to_y)
                else:
                    self.direction = set_direction()

            wn.update()
            wn.ontimer(self.change_direction, t=random.randint(100, 300))

        def hide(self):
            self.hideturtle()

        def return_enemy_ycor(self):
            return self.ycor()

        def return_enemy_xcor(self):
            return self.xcor()

        def update_direction(self, next_node):
            player_node = (next_node[0], next_node[1])
            self_node = (self.xcor(), self.ycor())
            if player_node[0] < self_node[0]:
                self.direction = 'left'
            elif player_node[0] > self_node[0]:
                self.direction = 'right'
            elif player_node[1] < self_node[1]:
                self.direction = 'down'
            elif player_node[1] > self_node[1]:
                self.direction = 'up'

        def update_shape(self):
            if self.direction == 'up':
                self.shape(f"enemy/level{game_level}/right.gif")
            elif self.direction == 'down':
                self.shape(f"enemy/level{game_level}/left.gif")
            elif self.direction == 'left':
                self.shape(f"enemy/level{game_level}/left.gif")
            elif self.direction == 'right':
                self.shape(f"enemy/level{game_level}/right.gif")

        def walk_randomly(self):
            directions = ['up', 'down', 'left', 'right']
            random_direction = random.choice(directions)
            dx, dy = 0, 0
            if random_direction == 'up':
                dy = self.movement
            elif random_direction == 'down':
                dy = -self.movement
            elif random_direction == 'left':
                dx = -self.movement
            elif random_direction == 'right':
                dx = self.movement
            move_to_x = self.xcor() + dx
            move_to_y = self.ycor() + dy
            check = check_wall_collision(move_to_x, move_to_y, walls)
            if check:
                self.goto(move_to_x, move_to_y)
            self.direction = random_direction
            self.update_shape()

        def bidirectional_search(self, player):
            start_node = (self.xcor(), self.ycor())
            goal_node = (player.xcor(), player.ycor())

            # Create two separate queues for forward and backward search
            forward_queue = deque()
            backward_queue = deque()

            # Create two separate sets for visited nodes for forward and backward search
            forward_visited = set()
            backward_visited = set()

            # Initialize the queues and visited sets
            forward_queue.append(start_node)
            forward_visited.add(start_node)

            backward_queue.append(goal_node)
            backward_visited.add(goal_node)

            # Store the parent of each visited node in forward search
            forward_parent = {start_node: None}
            # Store the parent of each visited node in backward search
            backward_parent = {goal_node: None}

            while forward_queue and backward_queue:
                # Perform forward search
                forward_node = forward_queue.popleft()
                # Check if the forward search intersects with the backward search
                if forward_node in backward_visited:
                    # Path found! Implement the code to move the enemy sprite along the path.
                    print("Path found!")
                    print(f"{goal_node} - Goal Node")
                    print(f"{forward_node} - Forward Node")
                    player_node = goal_node
                    self_node = (self.xcor(), self.ycor())
                    if player_node[0] < self_node[0]:
                        self.direction = 'left'
                    elif player_node[0] > self_node[0]:
                        self.direction = 'right'
                    elif player_node[1] < self_node[1]:
                        self.direction = 'down'
                    elif player_node[1] > self_node[1]:
                        self.direction = 'up'
                    check = check_wall_collision(
                        player_node[0], player_node[1], walls)
                    if check:
                        forward_parent = {}
                        backward_parent = {}
                        path = get_path(start_node, forward_node,
                                        forward_parent, backward_parent)
                        self.path = path

                        for node in path:
                            print(f"{node} - Walk Node")
                            self.goto(node[0], node[1])
                            wn.update()
                            # Add a delay between each step for smooth movement
                            time.sleep(0.1)
                    else:
                        self.direction = set_direction()

                    # Clear the forward and backward queues and visited sets
                    forward_queue.clear()
                    backward_queue.clear()
                    forward_visited.clear()
                    backward_visited.clear()
                    return

                # Add neighboring nodes to the forward queue if they are not visited
                for neighbor in get_neighbors(forward_node):
                    if neighbor not in forward_visited:
                        forward_queue.append(neighbor)
                        forward_visited.add(neighbor)
                        # Update the parent-child relationship
                        forward_parent[neighbor] = forward_node

                # Perform backward search
                backward_node = backward_queue.popleft()
                # Check if the backward search intersects with the forward search
                if backward_node in forward_visited:
                    # Path found! Implement the code to move the enemy sprite along the path.
                    print("Path found!")
                    print(f"{goal_node} - Goal Node")
                    print(f"{forward_node} - Forward Node")
                    player_node = goal_node
                    self_node = (self.xcor(), self.ycor())
                    if player_node[0] < self_node[0]:
                        self.direction = 'left'
                    elif player_node[0] > self_node[0]:
                        self.direction = 'right'
                    elif player_node[1] < self_node[1]:
                        self.direction = 'down'
                    elif player_node[1] > self_node[1]:
                        self.direction = 'up'
                    check = check_wall_collision(
                        player_node[0], player_node[1], walls)
                    if check:
                        forward_parent = {}
                        backward_parent = {}
                        path = get_path(backward_node, goal_node,
                                        forward_parent, backward_parent)
                        self.path = path

                        for node in path:
                            self.goto(node[0], node[1])
                            wn.update()
                            # Add a delay between each step for smooth movement
                            time.sleep(0.2)
                    else:
                        self.direction = set_direction()

                    return

                # Add neighboring nodes to the backward queue if they are not visited
                for neighbor in get_neighbors(backward_node):
                    if neighbor not in backward_visited:
                        backward_queue.append(neighbor)
                        backward_visited.add(neighbor)
                        # Update the parent-child relationship
                        backward_parent[neighbor] = backward_node

    def check_wall_collision(next_x, next_y, walls):
        wall_size = grid_block_size
        for wall in walls:
            wall_x, wall_y = wall
            if (
                next_x >= wall_x and
                next_x < wall_x + wall_size and
                next_y >= wall_y and
                next_y < wall_y + wall_size
            ):
                return False  # Collision detected with wall
        return True  # No collision with walls

    def get_neighbors(node):
        x, y = node
        neighbors = []

        # Check upward neighbor
        if check_wall_collision(x, y + grid_block_size, walls):
            neighbors.append((x, y + grid_block_size))

        # Check downward neighbor
        if check_wall_collision(x, y - grid_block_size, walls):
            neighbors.append((x, y - grid_block_size))

        # Check left neighbor
        if check_wall_collision(x - grid_block_size, y, walls):
            neighbors.append((x - grid_block_size, y))

        # Check right neighbor
        if check_wall_collision(x + grid_block_size, y, walls):
            neighbors.append((x + grid_block_size, y))

        return neighbors

    # levels
    levelsList.append(maze_list)

    def hide_text():
        turtle.clear()
        
    def hearts_functions(lives):
        image = "misc/box.gif"  # Use the image file path directly
        turtle.hideturtle()
        turtle.addshape(image)  # Register the shape with turtle
        turtle.penup()
        
        
        # Draw hearts based on the heart life count
        for i in range(lives):
            turtle.shape(image)
            turtle.goto(-500 + i * 40, 420)
            turtle.stamp()
        
        turtle.goto(0, max_height // 5)  # Set y-coordinate to the top
        
    def collision_check(sprite1, sprite2, block_sprite_size):
        global difficulty

        if sprite2.distance(sprite1) < block_sprite_size:
            if sprite2.name == 'Treasure':
                sprite1.gold += sprite2.gold
                coin_sound.play()
                sprite2.hide()
                treasures.remove(sprite2)
                font = ("Arial", 25, "bold")
                # Additional code for treasure collision...
                turtle.write("Hunt Mode", align="center", font=font)
                turtle.ontimer(hide_text, 1000) 
            elif sprite2.name == 'Box':
                sprite2.hide()
                boxes.remove(sprite2)
                heart_sound.play()
                sprite1.lives += 1
                font = ("Arial", 25, "bold")
                turtle.write("Add +life", align="center", font=font)
                turtle.ontimer(hide_text, 1000)  
                # Additional code for box collision...
                hearts_functions(sprite1.lives)
            elif sprite2.name == 'Enemy':
                if sprite1.lives == 0:
                    hurt_sound.play()
                    hurt_sound.set_volume(0)
                    sprite1.hide()
                    font = ("Arial", 28, "bold")
                    turtle.write("Game Over!", align="center", font=font)
                    lose_sound.play()
                    lose_sound.stop()
                else:
                    hurt_sound.play()
                    sprite1.lives -= 1
                    sprite1.is_attacked()
                    sprite1.teleport()
                    hearts_functions(sprite1.lives)
                    font = ("Arial", 25, "bold")
                    turtle.write("Hit!", align="center", font=font)
                    turtle.ontimer(hide_text, 1000)  # Hide text after 1 second (1000 milliseconds)

    def get_path(start_node, end_node, forward_parent, backward_parent):
        path = []

        path.append(start_node)

        current_node = start_node
        while current_node != end_node:
            if current_node not in forward_parent:
                break
            current_node = forward_parent[current_node]
            path.append(current_node)

        backward_path = []
        current_node = end_node
        while current_node != start_node:
            if current_node not in backward_parent:
                break
            backward_path.append(current_node)
            current_node = backward_parent[current_node]

        path.extend(reversed(backward_path))

        return path
    
    # For the Floors!
    max_floor_w = screen_width + 70
    max_floor_h = screen_height + 70

    def setup_maze(level, maze_dimensions):
        wn.tracer(300)
        maze_width, maze_height = maze_dimensions
        # formula for finding the coordinates within the maze
        for maze_y in range(len(level)):
            for maze_x in range(len(level[maze_y])):
                character = level[maze_y][maze_x]
                # formula for finding the coordinates within the screen
                screen_x = -(maze_width * grid_block_size) / \
                    2 + (maze_x * grid_block_size)
                screen_y = (maze_height * grid_block_size) / \
                    2 - (maze_y * grid_block_size)
                if character == 'S':
                    space.goto(screen_x, screen_y)
                    # append this is the coordinates we will need for the bidirectional
                    screen_space_coordinates.append((screen_x, screen_y))

                if character == 'X':
                    pen.goto(screen_x, screen_y)
                    choice_random_string = random.choice(
                        ["wall1", "wall2", "wall3", "wall4"])
                    pen.shape(
                        f"walls/level{game_level}/{choice_random_string}.gif")
                    pen.stamp()
                    walls.append((screen_x, screen_y))
                if character == 'T':
                    treasure_instance = Treasure(screen_x, screen_y)
                    treasures.append(treasure_instance)
                    # append this is the coordinates we will need for the bidirectional. This is the space location of the treasure.
                    screen_space_coordinates.append(
                        (treasure_instance.xcor(), treasure_instance.ycor()))
                if character == 'B':
                    boxes.append(Box(screen_x, screen_y))
                    # append this is the coordinates we will need for the bidirectional. This is the space location of the powerups.
                    screen_space_coordinates.append((screen_x, screen_y))
                if character == 'P':
                    player.setposition(screen_x, screen_y)
                    # append this is the coordinates we will need for the bidirectional. This is the space location of the player.
                    screen_space_coordinates.append((screen_x, screen_y))
                    player.showturtle()
                if character == 'E':
                    enemies.append(Enemy(screen_x, screen_y))
                    # append this is the coordinates we will need for the bidirectional. This is the space location of the Enemy.
                    screen_space_coordinates.append((screen_x, screen_y))

    maze_dimensions_list = [(len(maze[game_level-1]), len(maze))
                            for maze in maze_list]

    def check_wall_collision(next_x, next_y, walls):
        wall_size = grid_block_size
        for wall in walls:
            wall_x, wall_y = wall
            if (
                next_x >= wall_x and
                next_x < wall_x + wall_size and
                next_y >= wall_y and
                next_y < wall_y + wall_size
            ):
                return False  # Collision detected with wall
        return True  # No collision with walls

    # CHANGE LEVELS



    maze_dimensions = maze_dimensions_list[game_level-1]
    trigger_floor_gif(game_level, max_floor_w, max_floor_h)
    pen = Pen()
    space = Space()
    player = Player()
    setup_maze(maze_list[game_level-1], maze_dimensions)
    player_move(player, wn=wn)
    start_enemies_moving(500, enemies, wn, player)
    hearts_functions(player.lives)

    while True:
        if len(treasures) == 0:
            print("Winner!")
            win_sound.play()
            game_level+=1
            if game_level > 3:
                game_level = 1  # Reset game level to 1 if it exceeds 3
            start_game(game_level)
        for treasure in treasures:
            collision_check(player, treasure, grid_block_size)
        for box in boxes:
            collision_check(player, box, grid_block_size)
        for i, enemy in enumerate(enemies):
            collision_check(player, enemy, grid_block_size)
            # Get the current position of the enemystart_enemies_moving
            enemy_position = (enemy.xcor(), enemy.ycor())
            if len(current_enemy_location) <= i:
                # Append the position if it's the first time
                current_enemy_location.append(enemy_position)
            else:
                # Update the previous position with the new one
                current_enemy_location[i] = (enemy_position)
            random_string = random.choice(["action2", "action1", "action3"])
            enemy.shape(f"enemy/level{game_level}/{random_string}.gif")
            if enemy.direction == "right":
                enemy.shape(f"enemy/level{game_level}/right.gif")
            if enemy.direction == "left":
                enemy.shape(f"enemy/level{game_level}/left.gif")
        hearts_functions(player.lives)
        wn.update()

def new_level(value):
    pygame.mixer.init()
    pygame.mixer.music.load('bgmusic/main.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    start_game(value)
