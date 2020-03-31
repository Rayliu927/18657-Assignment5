 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# size of screen should be 1000 and block size should be 10
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 10
# population size = 1000
M = 2000
# inital infection rate = 0.1%
X = 0.3
# mobility = 50%
Pm = 0.5
# death probability = 2%
Pd = 0.8
# infection duration = 7 periods
K = 100
# S% of population stationary: 0 -> 1
S = 0.9

block_list = []
# position:block
block_position = dict()
infected_block = []
healthy_block = []
dead_block = []
mobile_block = []
 
 
class Block:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        # status: infected, healthy
        self.status = None
        # after infected, periods is set to 0
        self.periods = -1
        # current direction: l, r, u, d, ul, ur, dl, dr 
        self.direction = None

def make_block(status):
    """
    Function to make a new block.
    """
    block = Block()
    # Starting position of the block.
    # Take into account the block size so we don't spawn on the edge.
    block.x = random.randrange(BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE)
    block.y = random.randrange(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE)
    block.status = status
    if status == "infected":
        block.periods = 0
 
    return block

def make_block_mobile(block):
    """
    Function to make a block mobile.
    """
    directions = {(1, 1): "dr", (1, 0): "r", (1, -1): "ur", (0, 1): "d",(0, -1): "u",(-1, -1): "ul", 
    (-1, 0): "l", (-1, 1): "dl"}

    x = 0
    y = 0
    while x == 0 and y == 0:
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
    # Speed and direction of block: -1, 0, 1
    block.change_x = x
    block.change_y = y
    # block.change_x = 10
    # block.change_y = 10
    block.direction = directions[(x, y)]

def infect(block):
    if block.status != "infected":
        return
    for x in range(block.x-5, block.x + 5):
        for y in range(block.y-5, block.y+5):
            if (x, y) in block_position:
                hit_block = block_position[(x, y)]
                if hit_block.status == "healthy":
                    hit_block.status = "infected"
                    hit_block.periods = 0

def eliminate_options(block):
    options = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # top left corner
    if block.x < 0 and block.y < 0:
        options.remove((-1, 0))
        options.remove((0, -1))
        options.remove((-1, -1))
    # top right corner
    elif block.x > SCREEN_WIDTH - BLOCK_SIZE and block.y < 0:
        options.remove((1, 0))
        options.remove((0, -1))
        options.remove((1, -1))
    # botton left corner
    elif block.x < 0 and block.y > SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, -1))
        options.remove((-1, 1))
        options.remove((-1, 1))
    #  botton right corner
    elif block.x > SCREEN_WIDTH - BLOCK_SIZE and block.y > SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, -1))
        options.remove((1, 0))
        options.remove((1, 1))
    # top
    elif block.y < 0:
        options.remove((0, -1))
    # bottom
    elif block.y > SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, 1))
    # left 
    elif block.x < 0:
        options.remove((-1, 1))
    # right
    else:
        options.remove((1, 0))

    return options


def mobile(block):
    """
    Function to make a block bounce if encounter a obstacle
    """
    original_x, original_y = block.x, block.y
    options = eliminate_options(block)
    block.x += block.change_x
    block.y += block.change_y
    infect(block)

    if (block.x, block.y) in block_position or block.y > SCREEN_HEIGHT - BLOCK_SIZE or block.y < 0 or block.x > SCREEN_WIDTH - BLOCK_SIZE or block.x < 0:

        while len(options) > 0:
            block.x = original_x
            block.y = original_y

            new_direction = random.choice(options)
            options.remove(new_direction)

            block.x += new_direction[0]
            block.y += new_direction[1]
            infect(block)

            if (block.x, block.y) not in block_position and block.x > 0 and block.y > 0 and block.x <= SCREEN_WIDTH - BLOCK_SIZE and block.y <= SCREEN_HEIGHT - BLOCK_SIZE :
                block.change_x = new_direction[0] 
                block.change_y = new_direction[1]
                break

    # update the block position hashmap
    del block_position[(original_x, original_y)]
    block_position[(block.x, block.y)] = block

    # # Bounce the block if needed
    # if block.y > SCREEN_HEIGHT - BLOCK_SIZE or block.y < 0:
    #     block.change_y *= -1
    # if block.x > SCREEN_WIDTH - BLOCK_SIZE or block.x < 0:
    #     block.change_x *= -1

def die(block):
    """
    Function to erase a block
    """
    block.status = "dead"
    block_list.remove(block)

 
def main():
    """
    This is our main program.
    """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("covid-19 simulation")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    num_infected = int(M * X)
    num_healthy = M - num_infected

    # make inital infected block
    for i in range(num_infected):
        block = make_block("infected")
        block_list.append(block)
        block_position[(block.x, block.y)] = block

    # make inital healthy block
    for i in range(num_healthy):
        block = make_block("healthy")
        block_list.append(block)
        block_position[(block.x, block.y)] = block

    num_stationary = int(M * S)
    num_mobile = M - num_stationary

    index_block = [i for i in range(len(block_list))]
    index_mobile_block = []
    # randomly choose the mobile block
    for i in range(num_mobile):
        index = random.randint(0, len(index_block)-1)
        index_mobile_block.append(index_block[index])
        del index_block[index]

    # make the chosen block mobile
    for i in index_mobile_block:
        make_block_mobile(block_list[i])
        mobile_block.append(block_list[i])
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # elif event.type == pygame.KEYDOWN:
            #     # Space bar! Spawn a new ball.
            #     if event.key == pygame.K_SPACE:
            #         block = make_block()
            #         block_list.append(block)
 
        # --- Logic
        for block in mobile_block:
            # Move the block's center
            mobile(block)
            # original_x = block.x
            # original_y = block.y
            # block.x += block.change_x
            # block.y += block.change_y
 
            # change_direction(block)
 
        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
 
        # Draw the balls
        for block in block_list:
            if block.status == "infected":
                block.periods += 1
                if block.periods == K:
                    # the block is either dead or cured
                    poss = random.uniform(0, 1)
                    if poss < Pd:
                        die(block)
                        continue
                    else:
                        block.status = "cured"
                pygame.draw.rect(screen, RED, (block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
            elif block.status == "cured":
                pygame.draw.rect(screen, GREEN, (block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(10)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()