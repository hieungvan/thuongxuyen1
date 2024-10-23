import pygame
import sys
import random

# Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
FPS = 60
JUMP_STRENGTH = 15
OBSTACLE_COUNT = 1  # Number of obstacle types
OBSTACLE_GAP = 300  # Gap between obstacles

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dinosaur Jump Game')

# Load images
dino_image = pygame.image.load('buoi7/chim1.jpg')  # Load dinosaur image
dino_image = pygame.transform.scale(dino_image, (60, 60))  # Resize dinosaur
BG = pygame.image.load('buoi7/bg1.jpg')  # Background image
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))

# Load obstacle images (cacti)
cactus_image = pygame.image.load('buoi7/tao.jpg')  # Load cactus image
cactus_image = pygame.transform.scale(cactus_image, (40, 60))  # Resize cactus

# Create the font
font = pygame.font.SysFont('Arial', 30)

# Game variables
score = 0
lives = 3
dino_x = 50
dino_y = WINDOWHEIGHT - 60  # Ground level
is_jumping = False
jump_count = JUMP_STRENGTH

# Initialize clock
fpsClock = pygame.time.Clock()

# Generate random obstacles
obstacles = []


def generate_obstacle():
    obstacle_x = WINDOWWIDTH + random.randint(0, 100)
    obstacle_y = WINDOWHEIGHT - 60  # Ground level
    return (cactus_image, cactus_image.get_rect(topleft=(obstacle_x, obstacle_y)))


# Initialize first obstacles
for _ in range(3):  # Create initial obstacles
    obstacles.append(generate_obstacle())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                is_jumping = False  # Allow jumping only once when space is pressed

    # Background
    window.blit(BG, (0, 0))

    # Draw the dinosaur
    window.blit(dino_image, (dino_x, dino_y))

    # Jumping mechanics
    if is_jumping:
        if jump_count >= -JUMP_STRENGTH:
            neg = 1 if jump_count >= 0 else -1
            dino_y -= (jump_count ** 2) * 0.5 * neg  # Jumping arc
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = JUMP_STRENGTH

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle_image, obstacle_rect = obstacle
        obstacle_rect.x -= 5  # Move the obstacle left

        # Draw each obstacle
        window.blit(obstacle_image, obstacle_rect.topleft)

        # Check for collision
        if dino_image.get_rect(topleft=(dino_x, dino_y)).colliderect(obstacle_rect):
            lives -= 1
            obstacles.remove(obstacle)  # Remove the obstacle
            obstacles.append(generate_obstacle())  # Add a new obstacle
            if lives <= 0:
                game_over_text = font.render('Game Over', True, (255, 0, 0))
                window.blit(game_over_text, (WINDOWWIDTH //
                            2 - 100, WINDOWHEIGHT // 2))
                pygame.display.update()
                pygame.time.delay(2000)  # Show game over for 2 seconds
                pygame.quit()
                sys.exit()

        # Reset the obstacle if it goes off-screen
        if obstacle_rect.x < -obstacle_rect.width:
            obstacles.remove(obstacle)
            obstacles.append(generate_obstacle())  # Add a new obstacle

    # Update score
    score += 1

    # Display score and lives
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 40))

    pygame.display.update()  # Refresh display
    fpsClock.tick(FPS)  # Maintain frame rate
 