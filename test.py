import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Thêm ống nước")

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Tải hình ảnh con chim
bird = pygame.image.load("pepe_frog.png")
bird = pygame.transform.scale(bird, (50, 50))

# Vị trí con chim
bird_x = 100
bird_y = HEIGHT // 2
velocity_y = 0
gravity = 0.5
jump_power = -8

# Ống nước
pipe_width = 60
pipe_gap = 150  # Khoảng cách giữa ống trên và ống dưới
pipe_x = WIDTH  # Xuất hiện ngoài màn hình
pipe_height_top = random.randint(100, 300)  # Chiều cao ngẫu nhiên
pipe_speed = 3  # Tốc độ di chuyển của ống nước

# Đồng hồ FPS
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    # Hiển thị con chim
    screen.blit(bird, (bird_x, bird_y))

    # Cập nhật trọng lực
    velocity_y += gravity
    bird_y += velocity_y

    # Vẽ ống nước
    pygame.draw.rect(screen, GREEN, (pipe_x, 0, pipe_width, pipe_height_top))  # Ống trên
    pygame.draw.rect(screen, GREEN, (pipe_x, pipe_height_top + pipe_gap, pipe_width, HEIGHT - pipe_height_top - pipe_gap))  # Ống dưới

    # Di chuyển ống nước
    pipe_x -= pipe_speed

    # Khi ống nước đi khỏi màn hình, tạo lại ở bên phải với chiều cao mới
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_height_top = random.randint(100, 300)

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity_y = jump_power

    pygame.display.update()
    clock.tick(30)  # Giữ FPS ổn định ở 30

pygame.quit()
