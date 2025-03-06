import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Perry the platypus")


# FONT
FONT = {
    "ARIAL": pygame.font.Font(None, 40), # Font mặc định, size 40
    "MARIO_BIG": pygame.font.Font("TypefaceMarioWorldPixelFilledRegular-rgVMx.ttf", 25),
    "MARIO_SMALL": pygame.font.Font("TypefaceMarioWorldPixelFilledRegular-rgVMx.ttf", 15)
}

# COLOR
COLOR = {
    "WHITE": (255,255,255),
    "BLACK": (0,0,0),
    "RED": (255,0,0),
    "GREEN": (0, 255, 0),
    "ORANGE": (237, 145, 33),
    "GOLD": (255, 215, 0),
    "BEIGE": (245, 245, 220),
    "BRONZE": (205, 127, 50),
    "BROWN": (153, 51, 0),
    "CYAN": (0, 255, 255),
    "EMERALD": (80, 200, 120),
    "JUNGLE_GREEN": (41, 171, 135),
    "FOREST_GREEN": (34, 139, 34),
    "LIME_GREEN": (50, 205, 50),
    "MIDNIGHT_GREEN": (0, 73, 83),
    "AQUAMARINE": (0, 255, 191),
    "AZURE": (0, 127, 255),
    "BABY_BLUE": (137, 207, 240),
    "BLUE": (0, 0, 255),
    "DEEP_SKY_BLUE": (0, 191, 255),
    "LIGHT_SKY_BLUE": (135, 206, 250),
    "ICE_BLUE": (153, 255, 255),
    "LAPIS_LAZULI": (38, 97, 156),
    "MIDNIGHT_BLUE": (25, 25, 112),
    "ROYAL_BLUE": (0, 35, 102)
}

# Các hàm linh tinh
def draw_text(text, font = FONT["MARIO_SMALL"], color = COLOR["BLACK"], x = WIDTH // 2, y = HEIGHT // 2):
    """Vẽ chữ lên màn hình"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def is_A_to_the_left_of_B(x_a, x_b):
    if x_a < x_b:
        return True
    return False

# Các hàm tương tác giữa các đối tượng
def touched(block_1_hitbox, block_2_hitbox):
    if block_1_hitbox.colliderect(block_2_hitbox):
        return True
    return False

# CLASS: BACKGROUND
class image:
    def __init__(self, image_path, x = 0, y = 0, width = WIDTH, height = HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def print_image(self):
        screen.blit(self.image, (self.x, self.y))

class background:
    def __init__(self):
        self.velocity_x = -1

        self.background_static = image("background-2-sky.PNG") # PHẦN BACKGROUND ĐỨNG YÊN
        self.background_roto_1 = image("background-2-buildings.png") # PHẦN BACKGROUND CHUYỂN ĐỘNG LOOP
        self.background_roto_2 = image("background-2-buildings.png", WIDTH) # PHẦN BACKGROUND CHUYỂN ĐỘNG LOOP

        self.background_roto_list = [self.background_roto_1, self.background_roto_2]
        
    def print_image(self):
        self.background_static.print_image()
        for frame in self.background_roto_list:
            frame.print_image()

    def animation(self):
        for frame in self.background_roto_list:
            frame.x += self.velocity_x
            if frame.x + frame.width <= 0:
                frame.x = WIDTH

# Class: Flappy bird
class character:
    def __init__(self, image_normal, image_start_sprinting, image_end_sprinting):
        self.animation_frame = [image_normal, image_start_sprinting, image_end_sprinting]
        self.width = 50
        self.height = 50
        self.x = (WIDTH - self.width*4) // 2
        self.y = (HEIGHT - self.height) // 2
        self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load(image_normal)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
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
    def die_animation(self):
        self.velocity_y = -10

    def is_out_of_map(self):
        if self.y < 0 or self.y + self.height > HEIGHT:
            return True
        return False 

    def waiting_animation(self):
        if self.y > HEIGHT // 2:
            self.jumping()

# Class : các cái ống cống
class obstacle:
    def __init__(self, x = WIDTH):
        # chỉ số chung
        self.velocity_x = -5
        self.distance_gap = 150
        self.is_scored = False # Đã được tính điểm hay chưa

        # chỉ số của ống cống trên (ống gốc) 
        self.x_top = x
        self.y_top = 0
        self.width_top = 60
        self.height_top = random.randint(100,300)
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)

        # chỉ số của ống cống dưới (ống phụ thuộc trên)
        self.x_bottom = x
        self.y_bottom = self.height_top + self.distance_gap
        self.width_bottom = 60
        self.height_bottom = HEIGHT - self.y_bottom
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def print_image(self, screen):
        pygame.draw.rect(screen, COLOR["FOREST_GREEN"], self.pipe_top_rect)
        pygame.draw.rect(screen, COLOR["FOREST_GREEN"], self.pipe_bottom_rect)
    
    def moving(self):
        self.x_top += self.velocity_x
        self.x_bottom += self.velocity_x
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def reset(self, x_reset):
        # Chỉ số chung
        self.is_scored = False

        # chỉ số của ống cống trên (ống gốc) 
        self.x_top = x_reset
        self.y_top = 0
        self.width_top = 60
        self.height_top = random.randint(100,300)
        self.pipe_top_rect = pygame.Rect(self.x_top, self.y_top, self.width_top, self.height_top)

        # chỉ số của ống cống dưới (ống phụ thuộc trên)
        self.x_bottom = x_reset
        self.y_bottom = self.height_top + self.distance_gap
        self.width_bottom = 60
        self.height_bottom = HEIGHT - self.y_bottom
        self.pipe_bottom_rect = pygame.Rect(self.x_bottom, self.y_bottom, self.width_bottom, self.height_bottom)

    def is_out_of_range(self):
        # Check nếu ra ngoài 
        if self.x_top + self.width_top <= 0:
            return True
        return False

# TRẠNG THÁI ĐANG CHƠI
def game_playing(): 
    global score
    BACKGROUND.animation()
    BACKGROUND.print_image() # IN BACKGROUND

    draw_text(str(score), FONT["MARIO_BIG"], COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 100) # IN ĐIỂM

    # CHECK CON CHIM CÓ RA NGOÀI MAP KHÔNG?
    if flappy_bird.is_out_of_map():
        flappy_bird.die_animation()
        return "game_over"

    # THAO TÁC VỚI CÁC ỐNG CỐNG
    for obstacle in current_obstacle_list:
        obstacle.moving() # DI CHUYỂN ỐNG

        if obstacle.is_out_of_range(): # RESET VỊ TRÍ CỦA OBSTACLE
            obstacle.reset(x_reset)

        if touched(obstacle.pipe_top_rect, flappy_bird.hitbox) or touched(obstacle.pipe_bottom_rect, flappy_bird.hitbox): # CHECK VA CHẠM
            flappy_bird.die_animation()
            return "game_over"
        
        if is_A_to_the_left_of_B(obstacle.x_top, flappy_bird.x) and not obstacle.is_scored: # CHECK ĐIỂM
            score +=1
            obstacle.is_scored = True

        obstacle.print_image(screen) # IN ỐNG CỐNG

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return ""
        elif event.type == pygame.MOUSEBUTTONDOWN:
            flappy_bird.jumping()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ""

            # CÁC THAO TÁC VỀ NHÂN VẬT
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                flappy_bird.jumping()
            elif event.key == pygame.K_DOWN:
                flappy_bird.velocity_y = 100

    flappy_bird.print_image(screen)
    flappy_bird.moving()

    pygame.display.flip()
    pygame.time.Clock().tick(30) # FPS = 30

    return "playing"


# TRẠNG THÁI MENU
def game_menu():
    BACKGROUND.animation()
    BACKGROUND.print_image()
    
    # RESET CÁC OBSTACLE CHO LƯỢT CHƠI TIẾP THEO
    current_obstacle_list.clear()
    for i in range(number_of_obstacle):
        current_obstacle_list.append(obstacle(WIDTH * 1.5 + (obstacle().width_top + distance_between_obstacles) * i))


    # SET ĐIỂM
    global score
    score = 0

    # ANIMATION CON CHIM Ở MENU
    flappy_bird.print_image(screen)
    flappy_bird.waiting_animation()
    flappy_bird.moving()
    
    # CHỮ MENU
    draw_text("FLAPPY BIRD", FONT["MARIO_BIG"], COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("PRESS SPACE TO PLAY", FONT["MARIO_SMALL"], COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 + 100)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                flappy_bird.jumping()
                return "playing"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""

                # CÁC THAO TÁC VỀ NHÂN VẬT
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    flappy_bird.jumping()
                    return "playing"
                elif event.key == pygame.K_DOWN:
                    flappy_bird.velocity_y = 100
                    return "playing"

    pygame.display.flip() # Cập nhật màn hình
    pygame.time.Clock().tick(30) # FPS = 30

    return "menu"


# TRẠNG THÁI GAME OVER
def game_over():
    BACKGROUND.print_image()

    for obstacle in current_obstacle_list:
        obstacle.print_image(screen)

    # CẬP NHẬT BEST SCORE
    global best_score
    best_score = max(score, best_score)

    draw_text("GAME OVER", FONT["MARIO_BIG"],  COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("PRESS R TO PLAY AGAIN", FONT["MARIO_SMALL"],  COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 + 100)
    draw_text(f"SCORE", FONT["MARIO_SMALL"], COLOR["JUNGLE_GREEN"], WIDTH // 2, HEIGHT // 2 - 30)
    draw_text(f"{score}", FONT["MARIO_SMALL"],  COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2)
    draw_text(f"BEST SCORE", FONT["MARIO_SMALL"],  COLOR["JUNGLE_GREEN"], WIDTH // 2, HEIGHT // 2 + 30)
    draw_text(f"{best_score}", FONT["MARIO_SMALL"],  COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 + 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return ""
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return ""
            elif event.key == pygame.K_r:
                return "menu"

    flappy_bird.print_image(screen)
    flappy_bird.moving()

    pygame.display.flip()
    pygame.time.Clock().tick(30) # FPS = 30

    return "game_over"


# CÁC TRẠNG THÁI CỦA GAME
states = {
    "menu": game_menu,
    "playing": game_playing,
    "game_over": game_over
}

# THỰC THI GAME
# TẠO BACKGROUND
BACKGROUND = background()

# Tạo nhân vật
flappy_bird = character("Perry-1.png", "Perry-2.png", "Perry-3.png")

# Tạo obstacles
current_obstacle_list = []
distance_between_obstacles = 200 # Khoảng cách giữa các vật
number_of_obstacle = 3 # Số lượng vật cản tối đa có thể xuất hiện trên màn hình - 1
x_reset = distance_between_obstacles * number_of_obstacle + (number_of_obstacle - 1) * obstacle().width_top  # Vị trí của vật cần xuất hiện sau reset

# SCORES
score = 0
best_score = 0

current_state = "menu"
while current_state:
    current_state = states[current_state]()

pygame.quit()

