import pygame

# Khởi tạo Pygame
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Perry the platypus")

# Load hình ảnh ống cống và nhân vật
pipe_image = pygame.image.load("top_pipe.png").convert_alpha()
player_image = pygame.image.load("Perry-1.png").convert_alpha()

# Tạo mask từ hình ảnh
pipe_mask = pygame.mask.from_surface(pipe_image)
player_mask = pygame.mask.from_surface(player_image)

# Tạo Rect từ hình ảnh để lấy vị trí
pipe_rect = pipe_image.get_rect(topleft=(100, 150))
player_rect = player_image.get_rect(topleft=(150, 200))

# Tính offset giữa nhân vật và ống cống
offset = (player_rect.x - pipe_rect.x, player_rect.y - pipe_rect.y)

# Kiểm tra va chạm dựa trên mask
collision = pipe_mask.overlap(player_mask, offset)

if collision:
    print("Va chạm!")
else:
    print("Không va chạm!")
