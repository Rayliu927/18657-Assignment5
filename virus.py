import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# TODO: use the right scale of initial value
# TODO: vary S, run the experiment and draw plots
# size of screen should be 1000 and block size should be 10
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
BLOCK_SIZE = 1
# population size = 1000
M = 1000
# inital infection rate = 1%
X = 0.01
# mobility = 50%
Pm = 0.5
# death probability = 10%
Pd = 0.1
# infection duration = 9 periods
K = 9
# S% of population stationary: 0 -> 1
S = 0

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
        # infected periods: after infected, periods is set to 0
        self.periods = -1
        # current direction: l, r, u, d, ul, ur, dl, dr 
        self.direction = None
        # time of the block
        self.time = 0

def make_block(status):
    """
    Function to make a new block.
    """
    block = Block()
    # Starting position of the block.
    # Take into account the block size so we don't spawn on the edge.
    x = random.randrange(BLOCK_SIZE/2, SCREEN_WIDTH - BLOCK_SIZE/2)
    y = random.randrange(BLOCK_SIZE/2, SCREEN_HEIGHT - BLOCK_SIZE/2)
    while (x, y) in block_position:
    	x = random.randrange(BLOCK_SIZE/2, SCREEN_WIDTH - BLOCK_SIZE/2)
    	y = random.randrange(BLOCK_SIZE/2, SCREEN_HEIGHT - BLOCK_SIZE/2)

    block.x = x
    block.y = y
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
    block.direction = directions[(x, y)]

def infect(block):
	num_infected = 0
	if block.status == "cured":
		return num_infected
	for x in range(block.x - BLOCK_SIZE, block.x + BLOCK_SIZE):
	    for y in range(block.y - BLOCK_SIZE, block.y + BLOCK_SIZE):
	        if (x, y) in block_position:
	            hit_block = block_position[(x, y)]
	            if block.status == "infected" and hit_block.status == "infected":
	                continue
	            elif block.status == "infected" and hit_block.status == "healthy":
	                if block.time == hit_block.time or (hit_block.change_x == 0 and hit_block.change_y == 0):
	                    hit_block.status = "infected"
	                    hit_block.periods = 0
	                    num_infected += 1
	            elif block.status == "healthy" and hit_block.status == "infected":
	                if block.time == hit_block.time or (hit_block.change_x == 0 and hit_block.change_y == 0):
	                    block.status = "infected"
	                    block.periods = 0
	                    num_infected += 1
	return num_infected

def eliminate_options(block):
    options = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # top left corner
    if block.x <= 0 and block.y <= 0:
        options.remove((-1, 0))
        options.remove((0, -1))
        options.remove((-1, -1))
    # top right corner
    elif block.x >= SCREEN_WIDTH - BLOCK_SIZE and block.y <= 0:
        options.remove((1, 0))
        options.remove((0, -1))
        options.remove((1, -1))
    # botton left corner
    elif block.x <= 0 and block.y >= SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, 1))
        options.remove((-1, 1))
        options.remove((-1, 0))
    #  botton right corner
    elif block.x >= SCREEN_WIDTH - BLOCK_SIZE and block.y >= SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, 1))
        options.remove((1, 0))
        options.remove((1, 1))
    # top
    elif block.y <= 0:
        options.remove((0, -1))
    # bottom
    elif block.y >= SCREEN_HEIGHT - BLOCK_SIZE:
        options.remove((0, 1))
    # left 
    elif block.x <= 0:
        options.remove((-1, 0))
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
    num_infected = infect(block)

    if (block.x, block.y) in block_position or block.y >= SCREEN_HEIGHT - BLOCK_SIZE or block.y <= 0 or block.x >= SCREEN_WIDTH - BLOCK_SIZE or block.x <= 0:

        while len(options) > 0:
            block.x = original_x
            block.y = original_y

            new_direction = random.choice(options)
            options.remove(new_direction)

            block.x += new_direction[0]
            block.y += new_direction[1]
            num_infected += infect(block)

            if (block.x, block.y) not in block_position and block.x >= 0 and block.y >= 0 and block.x <= SCREEN_WIDTH - BLOCK_SIZE and block.y <= SCREEN_HEIGHT - BLOCK_SIZE :
                block.change_x = new_direction[0] 
                block.change_y = new_direction[1]
                break

    # update the block position hashmap
    if (original_x, original_y) in block_position:
	    del block_position[(original_x, original_y)]
	    block_position[(block.x, block.y)] = block
	# the number of blocks are infected
    return num_infected

# update the status of the block and remove it from board
def die(block):
    """
    Function to erase a block
    """
    block.status = "dead"
    block_list.remove(block)


def writeResult(total_death, total_infection, maximum_infection, maximum_periods, stop_periods):
	f = open('total_death.txt', 'a')
	f.write(str(total_death))
	f.write("\n")
	f.close()

	f1 = open('total_infection.txt', 'a')
	f1.write(str(total_infection))
	f1.write("\n")
	f1.close()

	f2 = open('maximum_infection.txt', 'a')
	f2.write(str(maximum_infection) + ", " + str(maximum_periods))
	f2.write("\n")
	f2.close()

	f3 = open('stop_periods.txt', 'a')
	f3.write(str(stop_periods))
	f3.write("\n")
	f3.close()

def main(T_periods):
    """
    This is our main program.
    """
    pygame.init()
    # initial result
    total_death = 0
    total_infection = 0
    maximum_infection = 0
    maximum_periods = 0
    current_infection = 0
    periods = 0

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
    # update result
    total_infection = num_infected
    maximum_infection = num_infected
    current_infection = num_infected

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
    while T_periods > periods:
    	periods += 1
    	if done:
    		break
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            	# end the program
            	done = True
          
        # --- Logic
        for block in mobile_block:
        	block.time += 1
        	poss = random.uniform(0, 1)
        	if poss > Pm:
        		continue
            # Move the block's center
	        infected = mobile(block)
	        if infected > 0:
	        	current_infection += infected
	        	total_infection += infected
 		
 		if current_infection > maximum_infection:
 			# print("max", periods, current_infection, maximum_infection)
 			maximum_infection = max(current_infection, maximum_infection)
 			maximum_periods = max(periods, maximum_periods)

        # --- Drawing
        # Set the screen background
        screen.fill(WHITE)
 
        # Draw the blocks
        for block in block_list:
            if block.status == "infected":
                block.periods += 1
                if block.periods == K:
                	current_infection -= 1
                	# print("aa", current_infection)
                	# the block is either dead or cured
                	poss = random.uniform(0, 1)
	                if poss < Pd:
	                    die(block)
	                    total_death += 1
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
        # clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # if there is no one infected now, end the simulation
        if current_infection == 0:
        	done = True
 
    # Close everything down
    pygame.quit()
    del block_list[:]
    block_position.clear()
    del mobile_block[:]
    return total_death, total_infection, maximum_infection, maximum_periods, periods
 
if __name__ == "__main__":
	# T_periods is the maximum duration of simulation
	T_periods = 500
	# number of simulation
	num_simulation = 20
	print("total_death", "total_infection", "maximum_infection", "maximum_periods", "stop_periods")
	for i in range(num_simulation):
		total_death, total_infection, maximum_infection, maximum_periods, stop_periods = main(T_periods)
		print(total_death, total_infection, maximum_infection, maximum_periods, stop_periods)
		writeResult(total_death, total_infection, maximum_infection, maximum_periods, stop_periods)





