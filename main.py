import pygame
import random

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy bird")

# Màu sắc
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,128,0)

# Chướng ngại vật
class obstacle:
    def __init__(self, image_path, x, y, width, height):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hit_box = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity_x = -10

    def checking_if_out_of_range(self): # Check nếu ra khỏi màn hình
        if self.x + self.width  < 0:
            self.x = WIDTH
            return True # True nếu out
        return False # False nếu in

    def moving(self): # Di chuyển
        self.x += self.velocity_x

    def checking_if_killed(self, character_hit_box): # Kiểm tra xem vật có chạm vào ai không
        if self.hit_box.colliderect(character_hit_box):
            print("Game over!")
            return True
        return False
    
    def print_image(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Ống cống
class pipe(obstacle):
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)


# Nhân vật con chim
class character:
    def __init__(self, image_path_normal, image_path_faster, image_path_fastest, x, y, width, height):
        self.image = pygame.image.load(image_path_normal)
        self.image = pygame.transform.scale(self.image,(width,height))
        self.animation_frame = [image_path_normal, image_path_faster, image_path_fastest]
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x, self.y, width, height)
        self.velocity_x = 0 # tốc độ di chuyển theo trục Ox
        self.velocity_y = 0 # tốc độ di chuyển theo trục Oy
        self.gravity = 1 # gia tốc trọng trường
        self.jump_power = -16 # vận tốc v[0] ban đầu lúc bật nhảy

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

    def jumping(self):
        self.velocity_y = self.jump_power

flappy_bird = character("Perry-1.png","Perry-2.png","Perry-3.png", 50, HEIGHT//2, 64, 64)
# obstacle1 = obstacle("J97-realistic.png", WIDTH, HEIGHT - 400, 300, 400)
# obstacle2 = obstacle("NTH-realistic.png", WIDTH, HEIGHT - 600, 450, 600)
# obstacle3 = obstacle("BD.png", WIDTH, HEIGHT - 200, 120, 200)
# obstacle4 = obstacle("DoPhuQui-realistic.png", WIDTH, HEIGHT - 300, 250, 300)
obstacle_list = []

current_obstacle_list = []
running = True
lack_of_obstacle = False
while running:
    screen.fill(WHITE) # Nền trắng
    flappy_bird.moving() # cập nhật vị trí của con chim
    flappy_bird.print_image(screen) # xuất ảnh của con chim

    lack_of_obstacle = True if current_obstacle_list[0].checking_if_out_of_range() else False # Check nếu ra khỏi tầm

    if lack_of_obstacle: # Nếu ít obstacle
        current_obstacle_list.pop(0) # Xoá obstacle đã out of range
        current_obstacle_list.append(random.choice(obstacle_list)) # Thêm obstacle mới vào game
    
    for obstacle in current_obstacle_list: 
        obstacle.moving() # Ống nước di chuyển
        obstacle.print_image(screen) # In ống nước ra màn hình
        obstacle.checking_if_killed(flappy_bird.hit_box) # 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                flappy_bird.jumping()

    pygame.display.flip()
    pygame.time.Clock().tick(30) # FPS = 30

pygame.quit()