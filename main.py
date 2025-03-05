import pygame
import random

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Perry the platypus")

# BACKGROUND
BACKGROUND = pygame.image.load("background-1.PNG")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

# FONT
ARIAL = pygame.font.Font(None, 40) # Font mặc định, size 40

# Màu sắc
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,128,0)

# Các hàm tương tác
def touched(block_1_hitbox, block_2_hitbox):
    if block_1_hitbox.colliderect(block_2_hitbox):
        return True
    return False

# Flappy bird
class character:
    def __init__(self, image_normal, image_start_sprinting, image_end_sprinting, x, y, width, height):
        self.image = pygame.image.load(image_normal)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.animation_frame = [image_normal, image_start_sprinting, image_end_sprinting]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_box = pygame.Rect(self.x, self.y, width, height)
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.jump_power = -12 # v[0]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def print_image(self, screen):
        if self.velocity_y < -8:
            self.image = pygame.image.load(self.animation_frame[2])
        elif self.velocity_y < 0:
            self.image = pygame.image.load(self.animation_frame[1])
        else:
            self.image = pygame.image.load(self.animation_frame[0])

        screen.blit(self.image,(self.x,self.y))

    def moving(self): # Di chuyển (cập nhật vị trí)
        self.velocity_y = min(self.velocity_y + self.gravity, 10) # trọng lực ảnh hưởng đến tốc độ di chuyển theo trục Oy
        self.x += self.velocity_x # di chuyển theo chiều Ox
        self.y += self.velocity_y # di chuyển theo chiều Oy
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def jumping(self):
        self.velocity_y = self.jump_power

    # Cắt cảnh game over
    def cutscene_gameover(self):
        global cutscene_is_playing
        cutscene_is_playing = True
        self.velocity_y = -10
        

# Class : các cái ống cống
class obstacle:
    def __init__(self):
        # chỉ số chung
        self.velocity_x = -10 
        self.distance_gap = 150 

        # chỉ số của ống cống trên (ống gốc) 
        self.x_top = WIDTH
        self.y_top = 0
        self.width_top = 50
        self.height_top = random.randint(100,300)
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)

        # chỉ số của ống cống dưới (ống phụ thuộc trên)
        self.x_bottom = WIDTH
        self.y_bottom = self.height_top + self.distance_gap
        self.width_bottom = 50
        self.height_bottom = HEIGHT - self.y_bottom
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def print_image(self, screen):
        pygame.draw.rect(screen, GREEN, self.pipe_top_rect)
        pygame.draw.rect(screen, GREEN, self.pipe_bottom_rect)
    
    def moving(self):
        self.x_top += self.velocity_x
        self.x_bottom += self.velocity_x
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def reset(self):
        # chỉ số của ống cống trên (ống gốc) 
        self.x_top = WIDTH
        self.y_top = 0
        self.width_top = 50
        self.height_top = random.randint(100,300)
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)

        # chỉ số của ống cống dưới (ống phụ thuộc trên)
        self.x_bottom = WIDTH
        self.y_bottom = self.height_top + self.distance_gap
        self.width_bottom = 50
        self.height_bottom = HEIGHT - self.y_bottom
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def out_of_range(self):
        # Check nếu ra ngoài 
        if self.x_top + self.width_top < 0:
            return True
        return False

#  Tạo nhân vật
flappy_bird = character("Perry-1.png", "Perry-2.png", "Perry-3.png", 100, 100, 50, 50)

# Tạo block
obstacle_list = [obstacle(), obstacle(), obstacle()]
current_obstacle_list = [obstacle_list[0]]

# Thực thi game
running = True
cutscene_is_playing = False
lack_of_obstacle = False
while(running):
    screen.blit(BACKGROUND, (0, 0))

    lack_of_obstacle = True if current_obstacle_list[0].out_of_range() else False

    if lack_of_obstacle:
        current_obstacle_list[0].reset()
        current_obstacle_list.pop(0)
        current_obstacle_list.append(random.choice(obstacle_list))

    for obstacle in current_obstacle_list:
        if not cutscene_is_playing:
            obstacle.moving()
            if touched(obstacle.pipe_top_rect, flappy_bird.hitbox) or touched(obstacle.pipe_bottom_rect, flappy_bird.hitbox):
                flappy_bird.cutscene_gameover()
        obstacle.print_image(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # CÁC THAO TÁC VỀ NHÂN VẬT
            if cutscene_is_playing:
                continue
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                flappy_bird.jumping()
            elif event.key == pygame.K_DOWN:
                flappy_bird.velocity_y = 100

    flappy_bird.print_image(screen)
    flappy_bird.moving()

    pygame.display.flip()
    pygame.time.Clock().tick(30) # FPS = 30

pygame.quit()

