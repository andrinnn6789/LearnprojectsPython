import pygame
import random
import time
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y, color, length, width):
        super().__init__()
        self.image = pygame.Surface((length, width), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, [0, 0, length, width])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def move_left(self):
        self.rect.move_ip(-20, 0)

    def move_right(self):
        self.rect.move_ip(20, 0)

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.size = size

    def draw_size(self, surface):
        font_size = int(self.size / 2)
        font = pygame.font.SysFont(None, font_size)
        size_text = font.render(str((1000 - (self.size * 10)) + self.size), True, BLACK)
        text_rect = size_text.get_rect()
        text_rect.center = self.rect.center
        surface.blit(size_text, text_rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, [0, 0, 10, 20])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -1

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:
            self.kill()

pygame.init()
screen_width = 800
screen_height = 600
textbox_width = 400
textbox_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))

gun = Gun(screen_width/2, screen_height - 80, BLACK, 50, 20)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

monsters = []
for i in range(5):
    monster = Monster(random.randint(40, screen_width - 40), screen_height/7, GREEN, random.randint(20, 100))
    monsters.append(monster)
    all_sprites.add(monster)

for sprite in all_sprites:
    sprite.draw_size(screen)

pygame.display.set_caption("Shooter")

# Set up the game clock
clock = pygame.time.Clock()

count = 0

countTime = 50  # Set the countdown timer to 60 seconds
start_time = pygame.time.get_ticks()  # Get the start time
    

# Game loop
while countTime > 0:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                gun.move_left()
            elif event.key == pygame.K_RIGHT:
                gun.move_right()
            elif event.key == pygame.K_SPACE:
                # Shoot bullet
                bullet = Bullet(gun.rect.centerx, gun.rect.top, RED)
                all_sprites.add(bullet)
                bullets.add(bullet)
                count -= 169

    for monster in monsters:
        hits = pygame.sprite.spritecollide(monster, bullets, True)
        if hits:
        # Remove the monster and create a new one
            count = count + (1000 - (monster.size * 10)) + monster.size
            monsters.remove(monster)
            all_sprites.remove(monster)
            monster = Monster(random.randint(40, screen_width - 40), screen_height/6, GREEN, random.randint(20, 100))
            all_sprites.add(monster)
            monsters.append(monster)

        # Move the bullets and remove them if they go off-screen
        all_sprites.update()

        # Draw all the sprites on the screen
        screen.fill(YELLOW)
        screen.blit(gun.image, gun.rect)
        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect)
            if isinstance(sprite, Monster):
                sprite.draw_size(screen)

    # Draw the count number on the screen
    font = pygame.font.SysFont(None, 36)
    count_text = font.render("Score: {}".format(count), True, BLACK)
    screen.blit(count_text, (10, 10))

    # Calculate the elapsed time since the start time
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

    # Calculate the remaining time on the countdown timer
    remaining_time = countTime - elapsed_time

    # Display the remaining time on the countdown timer
    font = pygame.font.SysFont(None, 36)
    count_text = font.render("Time: {}".format(round(countTime/83, 2)), True, BLACK)
    screen.blit(count_text, ((screen_width / 2) - 50, 10))

    # Limit the loop to running at a maximum of 60 frames per second
    clock.tick(200)

    # Decrement the countdown timer by one second per loop iteration
    countTime -= 1

    pygame.display.flip()

# Initialize the Pygame font module
pygame.freetype.init()

# Set up the font for displaying text
font = pygame.freetype.Font(None, 36)

# Create a message box surface
message_box = pygame.Surface((screen_width, screen_height // 3))
message_box.fill((255, 255, 255))  # Fill the surface with white

# Draw text on the message box surface
text_surface, _ = font.render("Your score is {}".format(count), (0, 0, 0))
message_box.blit(text_surface, (10, 10))

# Draw the message box on the Pygame window
screen.blit(message_box, (screen.get_width() // 2 - message_box.get_width() // 2,
                          screen.get_height() // 2 - message_box.get_height() // 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            # Exit the game loop when any key is pressed
            pygame.quit()

    pygame.display.update()