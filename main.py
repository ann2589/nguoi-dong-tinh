import pygame

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hội thoại tự động xuống dòng")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Font chữ
font = pygame.font.Font(None, 32)

# Danh sách hội thoại
dialogues = [
    ("Nhân vật A", "Xin chào, bạn khỏe không? Đây là một câu rất dài để kiểm tra chức năng tự động xuống dòng trong hội thoại."),
    ("Nhân vật B", "Chào bạn! Mình vẫn khỏe, còn bạn thì sao? Mình đang học Pygame và thấy nó rất thú vị."),
    ("Nhân vật A", "Mình cũng vậy! Bạn có muốn làm một trò chơi nhỏ không? Chúng ta có thể thử làm một game platformer đơn giản."),
    ("Nhân vật B", "Nghe có vẻ hay đấy! Bắt đầu từ đâu nhỉ?"),
    ("Nhân vật A", "Đầu tiên, hãy tạo một nhân vật có thể di chuyển bằng các phím mũi tên."),
]

# Chỉ số hội thoại hiện tại
dialogue_index = 0
text_full = dialogues[dialogue_index][1]  # Toàn bộ câu cần hiển thị
char_index = 0  # Chỉ số ký tự hiện tại
current_text = ""

# Tốc độ hiển thị chữ (miligiây trên mỗi ký tự)
TEXT_SPEED = 50  # 50ms mỗi ký tự
DIALOGUE_DELAY = 2000  # 2 giây trước khi chuyển sang câu tiếp theo
last_update = pygame.time.get_ticks()
dialogue_done_time = None  # Biến lưu thời gian hoàn thành hội thoại

# Giới hạn kích thước hộp thoại
TEXT_BOX_WIDTH = 680  # Chiều rộng hộp thoại (để căn chỉnh chữ)
TEXT_BOX_HEIGHT = 120  # Chiều cao hộp thoại tối đa

# Hàm tự động xuống dòng
def wrap_text(text, font, max_width):
    words = text.split()  # Tách từng từ
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)  # Xuống dòng
            current_line = word + " "

    lines.append(current_line)  # Thêm dòng cuối cùng
    return lines

# Hàm hiển thị hộp thoại
def draw_dialogue_box(character, text):
    pygame.draw.rect(screen, GRAY, (50, 400, 700, 150))  # Vẽ hộp thoại
    pygame.draw.rect(screen, WHITE, (50, 400, 700, 150), 3)  # Viền hộp thoại
    
    character_text = font.render(character + ":", True, WHITE)
    screen.blit(character_text, (60, 420))
    
    # Xử lý văn bản xuống dòng
    lines = wrap_text(text, font, TEXT_BOX_WIDTH)
    
    y_offset = 450  # Vị trí hiển thị dòng đầu tiên
    for line in lines:
        line_render = font.render(line, True, WHITE)
        screen.blit(line_render, (60, y_offset))
        y_offset += 30  # Khoảng cách giữa các dòng

# Vòng lặp chính
running = True
while running:
    screen.fill(BLACK)  # Xóa màn hình
    
    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hiệu ứng hiển thị từng ký tự
    current_time = pygame.time.get_ticks()
    if char_index < len(text_full) and current_time - last_update > TEXT_SPEED:
        char_index += 1
        last_update = current_time
        current_text = text_full[:char_index]
    
    # Nếu chữ đã hiển thị hết, bắt đầu đếm thời gian trước khi chuyển tiếp
    if char_index == len(text_full) and dialogue_done_time is None:
        dialogue_done_time = current_time  # Lưu thời gian hoàn tất hội thoại

    # Sau khi hiện xong, chờ một lúc rồi chuyển tiếp hội thoại
    if dialogue_done_time and current_time - dialogue_done_time > DIALOGUE_DELAY:
        if dialogue_index < len(dialogues) - 1:
            dialogue_index += 1
            text_full = dialogues[dialogue_index][1]
            char_index = 0
            current_text = ""
            dialogue_done_time = None  # Reset thời gian hoàn thành
        else:
            running = False  # Nếu hết hội thoại, thoát chương trình

    # Lấy nhân vật và hiển thị hội thoại với tự động xuống dòng
    character = dialogues[dialogue_index][0]
    draw_dialogue_box(character, current_text)

    # Cập nhật màn hình
    pygame.display.flip()

pygame.quit()
