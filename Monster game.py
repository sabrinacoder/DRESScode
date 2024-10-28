import pygame
import sys
import random
import math

# Initialise Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAVITY = 0.8
PLAYER_JUMP_STRENGTH = -15
PLAYER_SPEED = 5
MONSTER_SPEED = 2
COBWEB_SPEED = 5
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Halloween Warrior vs Monster Horde")

# Load Halloween-themed background image
bg_image = pygame.image.load('halloween_background.jpg')
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Font for displaying score and messages
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 50)

# Timer variables
start_time = pygame.time.get_ticks()  # Get initial time in milliseconds

# Warrior class
class Warrior(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 70), pygame.SRCALPHA)
        self.draw_warrior()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 150
        self.vel_y = 0
        self.on_ground = False

    def draw_warrior(self):
        pygame.draw.rect(self.image, BLUE, (10, 0, 30, 20))  # Helmet
        pygame.draw.rect(self.image, BLACK, (20, 5, 10, 10))  # Visor
        pygame.draw.rect(self.image, BLUE, (5, 20, 40, 40))  # Armor
        pygame.draw.line(self.image, BLACK, (45, 40), (50, 70), 3)  # Sword
        pygame.draw.circle(self.image, BLACK, (45, 40), 4)  # Sword hilt

    def update(self, platforms):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = PLAYER_JUMP_STRENGTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True

# Monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.color = color
        self.draw_monster()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.shoot_timer = random.randint(60, 180)
        self.bounce_offset = random.randint(0, 20)

    def draw_monster(self):
        pygame.draw.ellipse(self.image, self.color, (5, 5, 40, 40))  # Body
        pygame.draw.circle(self.image, WHITE, (25, 20), 10)  # Eye
        pygame.draw.circle(self.image, BLACK, (25, 20), 5)  # Pupil
        pygame.draw.polygon(self.image, BLACK, [(15, 35), (25, 45), (35, 35)])  # Teeth

    def update(self):
        self.rect.x += self.direction * MONSTER_SPEED
        self.rect.y += int(5 * math.sin(self.bounce_offset))  # Vertical bounce using math.sin
        self.bounce_offset += 0.1
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_cobweb()
            self.shoot_timer = random.randint(60, 180)

    def shoot_cobweb(self):
        cobweb = Cobweb(self.rect.centerx, self.rect.bottom, -1 if self.direction < 0 else 1)
        cobwebs.add(cobweb)
        all_sprites.add(cobweb)

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Projectile class for the warrior's shots
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += 10 * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Cobweb class for the monsters' shots
class Cobweb(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.x += COBWEB_SPEED * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Restart function to reset game state
def restart_game():
    global warrior, monsters, all_sprites, projectiles, cobwebs, score, game_over, win_message, start_time, elapsed_time
    all_sprites.empty()
    monsters.empty()
    projectiles.empty()
    cobwebs.empty()
    warrior = Warrior()
    all_sprites.add(warrior)
    monster1 = Monster(400, SCREEN_HEIGHT - 80, RED)
    monster2 = Monster(200, SCREEN_HEIGHT - 80, ORANGE)
    monster3 = Monster(600, SCREEN_HEIGHT - 80, PURPLE)
    monsters.add(monster1, monster2, monster3)
    all_sprites.add(monster1, monster2, monster3)
    all_sprites.add(platform1, platform2, platform3, ground)
    score = 0
    start_time = pygame.time.get_ticks()  # Reset start time
    elapsed_time = 0  # Reset elapsed time
    game_over = False
    win_message = ""
    

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
monsters = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
cobwebs = pygame.sprite.Group()

# Create platforms
platform1 = Platform(100, 500, 200, 20)
platform2 = Platform(350, 400, 200, 20)
platform3 = Platform(600, 300, 150, 20)
ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
platforms.add(platform1, platform2, platform3, ground)
all_sprites.add(platform1, platform2, platform3, ground)

# Create player (Warrior) and initial monsters
warrior = Warrior()
monster1 = Monster(400, SCREEN_HEIGHT - 80, RED)
monster2 = Monster(200, SCREEN_HEIGHT - 80, ORANGE)
monster3 = Monster(600, SCREEN_HEIGHT - 80, PURPLE)
monsters.add(monster1, monster2, monster3)
all_sprites.add(warrior, monster1, monster2, monster3)

# Score and game state
score = 0
game_over = False
win_message = ""

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and not game_over:
                direction = 1 if warrior.rect.centerx < monster1.rect.centerx else -1
                projectile = Projectile(warrior.rect.centerx, warrior.rect.centery, direction)
                projectiles.add(projectile)
                all_sprites.add(projectile)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if "Restart" button is clicked
                if SCREEN_WIDTH // 2 - 50 <= mouse_x <= SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 3 + 60 <= mouse_y <= SCREEN_HEIGHT // 3 + 110:
                    restart_game()

    if not game_over:
        # Update game objects
        warrior.update(platforms)
        monsters.update()
        projectiles.update()
        cobwebs.update()

        # Check for collisions between projectiles and monsters
        for monster in monsters:
            if pygame.sprite.spritecollide(monster, projectiles, True):
                score += 1
                monster.kill()

        # Check if all monsters are defeated
        if len(monsters) == 0:
            game_over = True
            win_message = "All monsters have been defeated, You win!"
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Freeze elapsed time

        # Check if any cobweb hits the warrior
        if pygame.sprite.spritecollideany(warrior, cobwebs) or pygame.sprite.spritecollideany(warrior, monsters):
            game_over = True
            win_message = "You have been caught by the monsters. GAME OVER!"
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Freeze elapsed time

    # Draw everything
    screen.blit(bg_image, (0, 0))
    all_sprites.draw(screen)

    # Display score
    #score_text = font.render(f"Score: {score}", True, WHITE)
    #screen.blit(score_text, (10, 10))

    # Display score and timer
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # Calculate time in seconds
    timer_text = font.render(f"Time: {elapsed_time}", True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 100, 10))

    # Display win or game over message if game is over
    if game_over:
        end_text = font.render(win_message, True, WHITE)
        screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 3))
        # Draw "Restart" button
        pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 3 + 60, 140, 50))
        restart_text = button_font.render("Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 3 + 70))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()



