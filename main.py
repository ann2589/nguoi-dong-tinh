import pygame
import cv2
import numpy as np

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Tải video bằng OpenCV
video = cv2.VideoCapture("transition_effect.mp4")

running = True
while running:
    ret, frame = video.read()
    
    if not ret:  # Nếu video kết thúc, thoát vòng lặp
        break
    
    # Chuyển đổi frame từ BGR (OpenCV) sang RGB (Pygame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)  # Xoay lại ảnh nếu cần
    frame = pygame.surfarray.make_surface(frame)

    # Vẽ frame lên màn hình
    screen.blit(pygame.transform.scale(frame, (WIDTH, HEIGHT)), (0, 0))
    
    pygame.display.update()

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

video.release()
pygame.quit()
