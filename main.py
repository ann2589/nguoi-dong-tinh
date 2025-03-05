import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Perry the platypus")

# BACKGROUND
BACKGROUND = pygame.image.load("background-1.PNG")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

# FONT
FONT = {
    "ARIAL": pygame.font.Font(None, 40) # Font mặc định, size 40
}

# COLOR
COLOR = {
    "WHITE": (255,255,255),
    "BLACK": (0,0,0),
    "RED": (255,0,0),
    "GREEN": (0,128,0)
}

# Các hàm linh tinh
def draw_text(text, font = FONT["ARIAL"], color = COLOR["BLACK"], x = WIDTH // 2, y = HEIGHT // 2):
    """Vẽ chữ lên màn hình"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Các hàm tương tác giữa các đối tượng
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
    def die_animation(self):
        self.velocity_y = -10

    def is_out_of_map(self):
        if self.y < 0 or self.y + self.height > HEIGHT:
            return True
        return False 

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
        pygame.draw.rect(screen, COLOR["GREEN"], self.pipe_top_rect)
        pygame.draw.rect(screen, COLOR["GREEN"], self.pipe_bottom_rect)
    
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

    def is_out_of_range(self):
        # Check nếu ra ngoài 
        if self.x_top + self.width_top < 0:
            return True
        return False

# TRẠNG THÁI ĐANG CHƠI
def game_playing():
    screen.blit(BACKGROUND, (0, 0))

    # CHECK CON CHIM CÓ RA NGOÀI MAP KHÔNG?
    if flappy_bird.is_out_of_map():
        flappy_bird.die_animation()
        return "game_over"

    # CHECK CÓ TẠO THÊM BLOCK KHÔNG
    is_needing_obstacle = True if current_obstacle_list[0].is_out_of_range() else False

    # TẠO THÊM ỐNG NẾU CẦN
    if is_needing_obstacle:
        current_obstacle_list[0].reset()

    for obstacle in current_obstacle_list:
        obstacle.moving()
        if touched(obstacle.pipe_top_rect, flappy_bird.hitbox) or touched(obstacle.pipe_bottom_rect, flappy_bird.hitbox):
            flappy_bird.die_animation()
            return "game_over"
        obstacle.print_image(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return ""
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
    screen.blit(BACKGROUND, (0, 0))

    # Tạo nhân vật
    global flappy_bird
    flappy_bird = character("Perry-1.png", "Perry-2.png", "Perry-3.png", 100, HEIGHT // 2, 50, 50)

    # Tạo obstacles
    # global obstacle_list 
    # obstacle_list = [obstacle(), obstacle(), obstacle()]
    global current_obstacle_list
    current_obstacle_list = [obstacle()]

    flappy_bird.print_image(screen)
    
    draw_text("FLAPPY BIRD", FONT["ARIAL"], COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("PRESS SPACE TO PLAY", FONT["ARIAL"], COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 + 100)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ""
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
    screen.blit(BACKGROUND, (0, 0))

    for obstacle in current_obstacle_list:
        obstacle.print_image(screen)

    draw_text("GAME OVER", FONT["ARIAL"],  COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 - 100)
    draw_text("PRESS R TO PLAY AGAIN", FONT["ARIAL"],  COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 + 100)

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
current_state = "menu"
while current_state:
    current_state = states[current_state]()

pygame.quit()

