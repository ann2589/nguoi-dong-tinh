import pygame
import random
import os

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Perry the platypus")

# LIÊN KẾT FILE / FOLDER
base_dir = os.path.dirname(__file__) # Lấy đường dẫn đến thư mục chứa script này

# Sound
soundtrack_1 = os.path.join(base_dir, "assets", "sounds", "soundtracks", "soundtrack-1.mp3")
scoring_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "score.mp3"))
jumping_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "jump.mp3"))
game_over_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "game over", "splat.mp3"))
collecting_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "ufo", "ufo-1.mp3"))

# Character 1 - perry ufo
char_perry_ufo_normal_frame = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-1.png")
char_perry_ufo_is_jumping_frame = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-2.png")
char_perry_ufo_start_jumping_frame = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-3.png")
char_perry_ufo_is_collecting_frame = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-4.png")

# Grounds
ground_frame = os.path.join(base_dir, "assets", "grounds", "ground.png")

# Obstacles
pipe_bottom_frame = os.path.join(base_dir, "assets", "obstacles", "pipe_bottom.png")
pipe_top_frame = os.path.join(base_dir, "assets", "obstacles", "pipe_top.png")

# Backgrounds
background_stato_frame = os.path.join(base_dir, "assets", "backgrounds", "background-2-sky.png")
background_roto_frame = os.path.join(base_dir, "assets", "backgrounds", "background-2-buildings.png")

# fonts
mario_font = os.path.join(base_dir, "assets", "fonts", "TypefaceMarioWorldPixelFilledRegular-rgVMx.ttf")

FONT = {
    "ARIAL": pygame.font.Font(None, 40), # Font mặc định, size 40
    "MARIO_BIG": pygame.font.Font(mario_font, 25),
    "MARIO_SMALL": pygame.font.Font(mario_font, 15)
}

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

class obj: # MỘT VẬT THỂ TRONG GAME
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        self.x = x # Các thông số của obj
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        
        self.image = pygame.image.load(image_path).convert_alpha() # Ảnh của obj
        self.width = self.image.get_width() if width == 0 else width # Nếu có kích thước tuỳ chỉnh thì theo, không thì kích thước như file ban đầu
        self.height = self.image.get_height() if height == 0 else height  # Nếu có kích thước tuỳ chỉnh thì theo, không thì kích thước như file ban đầu
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def print_image(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def is_out_of_the_map(self, right = True, left = True, bottom = True, top = True): # CHECK CÓ RA KHỎI HOÀN TOÀN MAP KHÔNG
        if left and self.x + self.width <= 0:
            return True
        elif right and self.x >= WIDTH:
            return True
        elif top and self.y + self.height <= 0:
            return True
        elif bottom and self.y >= HEIGHT:
            return True
        return False

    def is_collided_with_the_map(self, right = True, left = True, bottom = True, top = True): # CHECK CÓ VA CHẠM RÌA MAP HAY KHÔNG 
        if left and self.x <= 0:
            return True
        elif right and self.x + self.width >= WIDTH:
            return True
        elif top and self.y <= 0:
            return True
        elif bottom and self.y + self.height >= HEIGHT:
            return True
        return False
    
    def move(self): # DI CHUYỂN
        self.x += self.velocity_x * game_speed # di chuyển theo chiều Ox
        self.y += self.velocity_y * game_speed # di chuyển theo chiều Oy

class frontground(obj): # FRONTGROUND: LÀ VẬT MÀ CHIM CÓ THỂ TƯƠNG TÁC VA CHẠM (CẦN TẠO MASK)
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)
        self.hitbox = pygame.mask.from_surface(self.image)
        
class character(frontground): # NHẬT VẬT: FLAPPY BIRD
    def __init__(self, normal_frame, start_jumping_frame, is_jumping_frame, is_collecting_frame, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(normal_frame, x, y, width, height, velocity_x, velocity_y)
        self.gravity = 1 # gia tốc trọng trường
        self.jump_power = -12 # v[0]
        self.normal_frame = normal_frame
        self.start_jumping_frame = start_jumping_frame
        self.is_jumping_frame = is_jumping_frame
        self.is_collecting_frame = is_collecting_frame # Frame lúc hút bò

    def jump(self): # THAO TÁC NHẢY
        pygame.mixer.Sound.play(jumping_sound)
        self.velocity_y = self.jump_power

    def die(self): # ANIMATION CỦA CON CHIM KHI GAME OVER
        
        self.jump()

    def act_at_menu(self): # ANIMATION CỦA CON CHIM KHI Ở MENU
        if self.y > HEIGHT // 2:
            self.jump()

    def update_frame(self, is_collecting = False): # CẬP NHẬT FRAME THEO TỐC ĐỘ
        if is_collecting:
            self.image = pygame.image.load(self.is_collecting_frame)
        elif self.velocity_y < self.jump_power // 2:
            self.image = pygame.image.load(self.start_jumping_frame)
        elif self.velocity_y < 0:
            self.image = pygame.image.load(self.is_jumping_frame)
        else:
            self.image = pygame.image.load(self.normal_frame)

    def update_velocity(self): # UPDATE VẬN TỐC THEO GRAVITY
        self.velocity_y += self.gravity

    def reset_position(self):
        self.x = character_x
        self.y = character_y

    def move(self, is_collecting = False):
        self.update_velocity()
        self.update_frame(is_collecting)
        super().move()

class coins(frontground): # NHỮNG VẬT CHARACTER CÓ THỂ THU THẬP: BÒ
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

class obstacle(frontground): # CHƯỚNG NGẠI VẬT: ỐNG CỐNG
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0, give_score = False):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

        self.give_score = give_score # obstacle này khi vượt qua có cộng điểm hay không / chỉ định đây là cống trên hay dưới: True = trên, False = dưới
        self.is_scored = False # Đã được tính điểm hay chưa

        self.reset(x, y) # khởi tạo vị trí (x,y) của ống trên và dưới

    def reset(self, x, y): # Khởi tạo chỉ số vị trí và bật chế độ tính điểm của các ống cống
        self.is_scored = False if self.give_score else True
        self.x = x # vị trí reset của ống cống
        self.y = y # Gen random độ cao thấp của ống cống

class ground(frontground): # MẶT ĐẤT
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

    def reset(self):
        self.x += self.width * 2 # x2 để nó ở ngay sau ảnh ground số 2

class background(obj): # BACKGROUND: LÀ VẬT MÀ CHIM KHÔNG THỂ TƯƠNG TÁC (KHÔNG CẦN TẠO MASK)
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

    def reset(self): # Khởi tạo lại vị trí
        self.x += self.width * 2 # x2 để xuất hiện ngay sau frame ảnh thứ 2

def random_obstacle_height():
    y_top = random.uniform(- (obstacle_height - 0.15 * HEIGHT), - (obstacle_height - 0.45 * HEIGHT)) # ống cống trên dài từ 15% - 45% màn
    y_bottom = y_top + obstacle_height + distance_gap # ống cống dưới cách ống trên một khoảng = distance_gap
    return (y_top, y_bottom)

def update_game_speed(): # Cập nhật tốc độ game theo số điểm hiện tại (tỉ lệ thuận)
    global game_speed
    game_speed = game_speed_accel * score + min_game_speed
    game_speed = min(game_speed, max_game_speed)

def draw_text(text, font = FONT["MARIO_SMALL"], color = COLOR["BLACK"], x = WIDTH // 2, y = HEIGHT // 2): # VẼ CHỮ
    """Vẽ chữ lên màn hình"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def is_A_to_the_left_of_B(x_a, x_b): # KIỂM TRA A CÓ BÊN TRÁI B KHÔNG
    if x_a < x_b:
        return True
    return False

def is_collided(obj_a, obj_b): # KIỂM TRA VA CHẠM GIỮA 2 OBJ (MASK CỦA ẢNH)
    offset = (obj_a.x - obj_b.x, obj_a.y - obj_b.y) # Lấy vị trí tương đối của player so với ống cống

    return obj_b.hitbox.overlap(obj_a.hitbox, offset) is not None # True = có va chạm

def init_character(normal_frame, start_jumping_frame, is_jumping_frame, is_collecting_frame):
    return character(normal_frame, start_jumping_frame, is_jumping_frame, is_collecting_frame, character_x, character_y, character_width, character_height)
    
def init_ground_list(my_list): # TẠO FRAME LIST CỦA MẶT ĐẤT
    my_list.clear()
    
    ground1 = ground(ground_frame, 0, HEIGHT - 100, WIDTH, 100, -5, 0) # ground frame 1
    ground2 = ground(ground_frame, WIDTH, HEIGHT - 100, WIDTH, 100, -5, 0) # ground frame 2
    my_list.append(ground1)
    my_list.append(ground2)

def init_obstacle_list(my_list): # TẠO DANH SÁCH CHƯỚNG NGẠI VẬT: ỐNG CỐNG
    my_list.clear()

    for i in range(number_of_obstacle): # tạo danh sách obstacle
        (y_top, y_bottom) = random_obstacle_height()
        my_list.insert(0, obstacle(pipe_top_frame, WIDTH * 1.5 + (obstacle_width + distance_between_obstacles) * i, y_top, obstacle_width, obstacle_height, obstacle_velocity_x, 0, True))
        my_list.insert(0, obstacle(pipe_bottom_frame, WIDTH * 1.5 + (obstacle_width + distance_between_obstacles) * i, y_bottom, obstacle_width, obstacle_height, obstacle_velocity_x, 0, False))

def init_frontground_list(ground_list, obstacle_list):
    init_ground_list(ground_list)
    init_obstacle_list(obstacle_list)

def init_background_list(my_list): # TẠO DANH SÁCH FRAME PHẦN BACKGROUND
    background_stato = background(background_stato_frame, 0, 0, WIDTH, HEIGHT, 0, 0) # Phần background đứng yên
    background_roto1 = background(background_roto_frame, 0, 0, WIDTH, HEIGHT - 100, -1, 0) # Phần background loop frame 1
    background_roto2 = background(background_roto_frame, WIDTH, 0, WIDTH, HEIGHT - 100, -1, 0) # Phần background loop frame 2
    my_list[:] = [background_stato, background_roto1, background_roto2]

def game_playing_hard():
    
    pygame.mixer.music.play()
    
    while True:
        global score, is_collecting # liên kết score => cập nhật best_score
        update_game_speed() # Tặng tốc game dần theo score

        for frame in background_list: # IN BACKGROUND
            frame.move()
            frame.print_image(screen)
            
            if frame.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                frame.reset()

        y_top, y_bottom = 0, 0
        for frame in obstacle_list: # IN OBSTACLE
            frame.move()
            frame.print_image(screen)
            
            if frame.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                if frame.give_score: # Nếu ống trên
                    frame.reset(x_reset_for_obstacle, y_top) # vị trí ống trên
                else:
                    (y_top, y_bottom) = random_obstacle_height() # thì random chiều cao cho cặp ống trên dưới mới này
                    frame.reset(x_reset_for_obstacle, y_bottom) # vị trí ống dưới

            if is_collided(current_character, frame): # Game over nếu có va chạm
                current_character.die()
                return "game_over"

            if not frame.is_scored and is_A_to_the_left_of_B(frame.x, current_character.x): # CẬP NHẬT ĐIỂM
                score += 1
                frame.is_scored = True

        for frame in ground_list: # IN GROUND
            frame.move()
            frame.print_image(screen)
            
            if frame.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                frame.reset()

            if is_collided(current_character, frame): # Game over nếu có va chạm
                current_character.die()
                return "game_over"

        if current_character.is_collided_with_the_map(False, False, True, True): # CHECK GAME OVER KHI CHIM BAY NGOÀI MAP
            current_character.die()
            return "game_over"

        current_character.move(is_collecting) # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        draw_text(str(score), FONT["MARIO_BIG"], COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 100) # IN ĐIỂM

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif not is_collecting and event.type == pygame.MOUSEBUTTONDOWN:
                current_character.jump()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif not is_collecting and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    current_character.jump()
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    pygame.mixer.Sound.play(collecting_sound)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

    return "game_playing_hard"

def game_menu():
    while True:
        global is_collecting
        for frame in background_list: # IN BACKGROUND
            frame.move() 
            frame.print_image(screen)
            
            if frame.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                frame.reset()

        for frame in ground_list: # IN GROUND
            frame.move()
            frame.print_image(screen)
            
            if frame.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                frame.reset()

        if current_character.is_out_of_the_map(): # RESET VỊ TRÍ CHIM
            current_character.y = HEIGHT // 2

        current_character.move() # Cập nhật vị trí
        current_character.act_at_menu() # animation ở menu
        current_character.print_image(screen) # IN CHARACTER

        draw_text("FLAPPY BIRD", FONT["MARIO_BIG"], COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 - 100) # IN CHỮ Ở MENU
        draw_text("PRESS SPACE TO PLAY", FONT["MARIO_SMALL"], COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 + 100)

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_character.jump()
                return "game_playing_hard"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    current_character.jump()
                    return "game_playing_hard"
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    return "game_playing_hard"

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False
                    return "game_playing_hard"

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

    return "game_menu"

def game_over():
    pygame.mixer.Sound.play(game_over_sound)
    pygame.mixer.music.fadeout(5)

    while True:
        global best_score, score, game_speed, current_character # liên kết score => cập nhật best_score; game_speed
        best_score = max(score, best_score)

        for frame in background_list: # IN BACKGROUND
            frame.print_image(screen)

        for frame in obstacle_list: # IN OBSTACLE
            frame.print_image(screen)

        for frame in ground_list: # IN GROUND
            frame.print_image(screen)

        current_character.move() # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        pygame.draw.rect(screen, COLOR["BABY_BLUE"], (20, 100, 380 - 20, 500 - 100)) # IN CHỮ
        draw_text("GAME OVER", FONT["MARIO_BIG"],  COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("PRESS C TO PLAY AGAIN", FONT["MARIO_SMALL"],  COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 + 100)
        draw_text(f"SCORE", FONT["MARIO_SMALL"], COLOR["JUNGLE_GREEN"], WIDTH // 2, HEIGHT // 2 - 45)
        draw_text(f"{score}", FONT["MARIO_SMALL"],  COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 15)
        draw_text(f"BEST SCORE", FONT["MARIO_SMALL"],  COLOR["JUNGLE_GREEN"], WIDTH // 2, HEIGHT // 2 + 15)
        draw_text(f"{best_score}", FONT["MARIO_SMALL"],  COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 + 45)

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""

                if event.key == pygame.K_c: # Trở về menu
                    init_frontground_list(ground_list, obstacle_list) # Khởi tạo lại các frame
                    init_background_list(background_list)
                    score = 0 # reset score
                    game_speed = min_game_speed
                    current_character.reset_position()
                    return "game_menu"

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

    return "game_over"

'''DƯỚI ĐÂY LÀ CÁC THÔNG SỐ CÓ THỂ ĐƯỢC TUỲ CHỈNH SAO CHO PHÙ HỢP VỚI NGƯỜI CHƠI'''

# TẠO NHẠC NỀN
pygame.mixer.music.load(soundtrack_1)

# THÔNG SỐ NHÂN VẬT
character_width = 50
character_height = 50
character_x = (WIDTH - 200) // 2
character_y = (HEIGHT - 50) // 2

# TẠO NHÂN VẬT
current_character = init_character(char_perry_ufo_normal_frame, char_perry_ufo_start_jumping_frame, char_perry_ufo_is_jumping_frame, char_perry_ufo_is_collecting_frame)
is_collecting = False

# THÔNG SỐ CỦA OBSTACLE
distance_gap = 150 # Khoảng cách giữa 2 ống cống trên dưới
obstacle_width = 60
obstacle_height = 500 
obstacle_velocity_x = -5 # TỐC ĐỘ DI CHUYỂN CỦA ỐNG CỐNG
distance_between_obstacles = 200 # Khoảng cách giữa 2 chướng ngại vật
number_of_obstacle = 3 # Số lượng vật cản tối đa có thể xuất hiện trên màn hình = number_of_obstacle - 1
x_reset_for_obstacle = distance_between_obstacles * number_of_obstacle + (number_of_obstacle - 1) * obstacle_width  # VỊ TRÍ hoành độ của ống cống spawn lại sau khi bay ra khỏi màn hình

# TẠO DANH SÁCH FRAME PHẦN FRONTGROUND GỒM: OBSTACLE & GROUND
obstacle_list = [] # Tạo danh sách frame của obstacle
ground_list = [] # Tạo danh sách frame của ground
init_frontground_list(ground_list, obstacle_list)

# TẠO DANH SÁCH FRAME PHẦN BACKGROUND
background_list = []
init_background_list(background_list)

# TỐC ĐỘ GAME
game_speed = 1 # khởi đầu là 1x
score_at_max_game_speed = 100 # Điểm dừng tăng tiến tốc độ game
min_game_speed = 1 # Tốc độ game ban đầu
max_game_speed = 2 # Tốc độ game tối đa
game_speed_accel = (max_game_speed - min_game_speed) / score_at_max_game_speed # gia tốc của tốc độ game => gia tốc của vận tốc theo hoành độ

# SCORES
score = 0
best_score = 0

# CÁC TRẠNG THÁI CỦA GAME
states = {
    "game_menu": game_menu,
    "game_playing_hard": game_playing_hard,
    # "game_playing_normal": game_playing_normal,
    # "game_playing_easy": game_playing_easy,
    "game_over": game_over
}

# VÒNG LẶP CHÍNH CỦA GAME
current_state = "game_menu"
while current_state:
    current_state = states[current_state]()

pygame.quit()
