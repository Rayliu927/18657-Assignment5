 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BLOCK_SIZE = 25
 
 
class Block:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
 
 
def make_block():
    """
    Function to make a new, random ball.
    """
    block = Block()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    block.x = random.randrange(BLOCK_SIZE, SCREEN_WIDTH - BLOCK_SIZE)
    block.y = random.randrange(BLOCK_SIZE, SCREEN_HEIGHT - BLOCK_SIZE)
 
    # Speed and direction of rectangle
    block.change_x = random.randrange(-2, 3)
    block.change_y = random.randrange(-2, 3)
 
    return block
 
 
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
 
    block_list = []
 
    block = make_block()
    block_list.append(block)
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    block = make_block()
                    block_list.append(block)
 
        # --- Logic
        for block in block_list:
            # Move the ball's center
            block.x += block.change_x
            block.y += block.change_y
 
            # Bounce the ball if needed
            if block.y > SCREEN_HEIGHT - BLOCK_SIZE or block.y < BLOCK_SIZE:
                block.change_y *= -1
            if block.x > SCREEN_WIDTH - BLOCK_SIZE or block.x < BLOCK_SIZE:
                block.change_x *= -1
 
        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)
 
        # Draw the balls
        for block in block_list:
            pygame.draw.rect(screen, RED, (block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main()