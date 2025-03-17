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
cow_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "cows", "bokhongluoi-1.mp3"))
plane_sound = pygame.mixer.Sound(os.path.join(base_dir, "assets", "sounds", "planes", "planecrashdiectai.mp3"))

# Character 1 - perry ufo
char_perry_ufo_normal_image = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-1.png")
char_perry_ufo_is_jumping_image = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-2.png")
char_perry_ufo_start_jumping_image = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-3.png")
char_perry_ufo_is_collecting_image = os.path.join(base_dir, "assets", "characters", "perry_ufo", "perry-4.png")

# Character 2 - perry plane
char_perry_plane_normal_image = os.path.join(base_dir, "assets", "characters", "perry_plane", "perry-plane-1.png")

# Grounds
ground_image = os.path.join(base_dir, "assets", "grounds", "ground.png")

# Obstacles
pipe_bottom_image = os.path.join(base_dir, "assets", "obstacles", "pipe-bottom.png")
pipe_top_image = os.path.join(base_dir, "assets", "obstacles", "pipe-top.png")
twin_towers_image = os.path.join(base_dir, "assets", "obstacles", "twin-towers-1.png")

# Coins
coin_image_1 = os.path.join(base_dir, "assets", "coins", "cow-1.png")

# Backgrounds
background_stato_image = os.path.join(base_dir, "assets", "backgrounds", "background-2-sky.png")
background_roto_image = os.path.join(base_dir, "assets", "backgrounds", "background-2-buildings.png")

# fonts
mario_font = os.path.join(base_dir, "assets", "fonts", "TypefaceMarioWorldPixelFilledRegular-rgVMx.ttf")

# random files
sexy_girl_image = os.path.join(base_dir, "assets", "easter eggs", "sexy.png")

RANDOM_HINT = [
    "Press down-but to have a long dic-",
    "Right mouse for a long dic-",
    "Score 69 for a sexy",
    "Score 119 for a surprise",
    "Press 2 for 200 points",
    "score 20 = faster game speed"
]

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
        elif bottom and self.y >= HEIGHT - ground_height:
            return True
        return False

    def is_collided_with_the_map(self, right = True, left = True, bottom = True, top = True): # CHECK CÓ VA CHẠM RÌA MAP HAY KHÔNG 
        if left and self.x <= 0:
            return True
        elif right and self.x + self.width >= WIDTH:
            return True
        elif top and self.y <= 0:
            return True
        elif bottom and self.y + self.height >= HEIGHT - ground_height:
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
    def __init__(self, normal_image, start_jumping_image, is_jumping_image, is_collecting_image, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(normal_image, x, y, width, height, velocity_x, velocity_y)
        self.gravity = 1 # gia tốc trọng trường
        self.jump_power = -12 # v[0]
        self.normal_image = normal_image
        self.start_jumping_image = start_jumping_image
        self.is_jumping_image = is_jumping_image
        self.is_collecting_image = is_collecting_image # image lúc hút bò
        self.collecting_range = pygame.mask.from_surface(pygame.image.load(self.is_collecting_image))

    def jump(self): # THAO TÁC NHẢY
        pygame.mixer.Sound.play(jumping_sound)
        self.velocity_y = self.jump_power

    def die(self): # ANIMATION CỦA CON CHIM KHI GAME OVER
        self.jump()

    def act_at_menu(self): # ANIMATION CỦA CON CHIM KHI Ở MENU
        if self.y > HEIGHT // 2:
            self.jump()

    def update_image(self, is_collecting = False): # CẬP NHẬT image THEO TỐC ĐỘ
        if is_collecting:
            self.image = pygame.image.load(self.is_collecting_image)
        elif self.velocity_y < self.jump_power // 2:
            self.image = pygame.image.load(self.start_jumping_image)
            self.image = pygame.transform.rotate(self.image, 0)
        elif self.velocity_y < 0:
            self.image = pygame.image.load(self.is_jumping_image)
            self.image = pygame.transform.rotate(self.image, 0)
        else:
            self.image = pygame.image.load(self.normal_image)
            self.image = pygame.transform.rotate(self.image, 0)

    def update_velocity(self): # UPDATE VẬN TỐC THEO GRAVITY
        self.velocity_y += self.gravity

    def reset_position(self):
        self.x = character_x
        self.y = character_y

    def move(self, is_collecting = False):
        self.update_velocity()
        self.update_image(is_collecting)
        super().move()

class coin(frontground): # NHỮNG VẬT CHARACTER CÓ THỂ THU THẬP: BÒ
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)
        self.is_scored = False

    def reset_position(self, x, y):
        self.is_scored = False
        self.x = x
        self.y = y

class obstacle(frontground): # CHƯỚNG NGẠI VẬT: ỐNG CỐNG
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0, give_score = False):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

        self.give_score = give_score # obstacle này khi vượt qua có cộng điểm hay không / chỉ định đây là cống trên hay dưới: True = trên, False = dưới
        self.is_scored = False # Đã được tính điểm hay chưa

        self.reset_position(x, y) # khởi tạo vị trí (x,y) của ống trên và dưới

    def reset_position(self, x, y): # Khởi tạo chỉ số vị trí và bật chế độ tính điểm của các ống cống
        self.is_scored = False if self.give_score else True
        self.x = x # vị trí reset của ống cống
        self.y = y # Gen random độ cao thấp của ống cống

class ground(frontground): # MẶT ĐẤT
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

    def reset_position(self):
        self.x += self.width * 2 # x2 để nó ở ngay sau ảnh ground số 2

class background(obj): # BACKGROUND: LÀ VẬT MÀ CHIM KHÔNG THỂ TƯƠNG TÁC (KHÔNG CẦN TẠO MASK)
    def __init__(self, image_path, x = 0, y = 0, width = 0, height = 0, velocity_x = 0, velocity_y = 0):
        super().__init__(image_path, x, y, width, height, velocity_x, velocity_y)

    def reset_position(self): # Khởi tạo lại vị trí
        self.x += self.width * 2 # x2 để xuất hiện ngay sau image ảnh thứ 2

def random_obstacle_height():
    y_top = random.uniform(- (obstacle_height - 0.15 * HEIGHT), - (obstacle_height - 0.45 * HEIGHT)) # ống cống trên dài từ 15% - 45% màn
    y_bottom = y_top + obstacle_height + distance_gap # ống cống dưới cách ống trên một khoảng = distance_gap
    return (y_top, y_bottom)

def random_coin_position(): # Vị trí random của coin giữa 2 obstacles
    x_position_cap = distance_between_obstacles - coin_width # Vị trí coin.x tối đa  
    return random.uniform(0.2 * x_position_cap, 0.8 * x_position_cap)

def update_game_speed(game_speed): # Cập nhật tốc độ game theo số điểm hiện tại (tỉ lệ thuận)
    game_speed = game_speed_accel * score + min_game_speed
    game_speed = min(game_speed, max_game_speed)

def draw_text(text = "Hello, world!", font = FONT["MARIO_SMALL"], color = COLOR["BLACK"], x = WIDTH // 2, y = HEIGHT // 2): # VẼ CHỮ
    """Vẽ chữ lên màn hình"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def is_A_to_the_left_of_B(x_a, x_b): # KIỂM TRA A CÓ BÊN TRÁI B KHÔNG
    if x_a < x_b:
        return True
    return False

def is_collided(a_x, a_y, a_hitbox, b_x, b_y, b_hitbox): # KIỂM TRA VA CHẠM GIỮA 2 OBJ (MASK CỦA ẢNH)
    offset = (a_x - b_x, a_y - b_y) # Lấy vị trí tương đối của player so với ống cống
    return b_hitbox.overlap(a_hitbox, offset) is not None # True = có va chạm

def init_character(normal_image, start_jumping_image, is_jumping_image, is_collecting_image):
    return character(normal_image, start_jumping_image, is_jumping_image, is_collecting_image, character_x, character_y, character_width, character_height)
    
def init_ground_list(my_list): # TẠO image LIST CỦA MẶT ĐẤT
    my_list.clear()
    
    ground1 = ground(ground_image, 0, HEIGHT - ground_height, ground_width, ground_height, ground_velocity_x) # ground image 1
    ground2 = ground(ground_image, ground_width, HEIGHT - ground_height, ground_width, ground_height, ground_velocity_x) # ground image 2
    my_list.append(ground1)
    my_list.append(ground2)

def init_obstacle_list(my_list): # TẠO DANH SÁCH CHƯỚNG NGẠI VẬT: ỐNG CỐNG
    my_list.clear()

    for i in range(number_of_obstacle): # tạo danh sách obstacle
        (y_top, y_bottom) = random_obstacle_height()
        my_list.insert(0, obstacle(pipe_top_image, x_first_spawn + (obstacle_width + distance_between_obstacles) * i, y_top, obstacle_width, obstacle_height, obstacle_velocity_x, 0, True))
        my_list.insert(0, obstacle(pipe_bottom_image, x_first_spawn + (obstacle_width + distance_between_obstacles) * i, y_bottom, obstacle_width, obstacle_height, obstacle_velocity_x, 0, False))

def init_coin_list(my_list):# TẠO DANH SÁCH COIN: Bò
    my_list.clear()
    
    for i in range(number_of_coin): # tạo danh sách coin
        coin_x = random_coin_position() + x_first_spawn + obstacle_width + (obstacle_width + distance_between_obstacles) * i
        my_list.insert(0, coin(coin_image_1, coin_x, coin_y_when_it_resets_position, coin_width, coin_height, coin_velocity_x))

def init_background_list(my_list): # TẠO DANH SÁCH image PHẦN BACKGROUND
    my_list.clear()
    
    background_stato = background(background_stato_image, 0, 0, WIDTH, HEIGHT, 0, 0) # Phần background đứng yên
    background_roto1 = background(background_roto_image, 0, 0, WIDTH, HEIGHT - ground_height, background_velocity_x) # Phần background loop image 1
    background_roto2 = background(background_roto_image, WIDTH, 0, WIDTH, HEIGHT - ground_height, background_velocity_x) # Phần background loop image 2
    my_list[:] = [background_stato, background_roto1, background_roto2]

def init_obj(ground_list = False, obstacle_list = False, coin_list = False, background_list = False):
    if type(ground_list) == list:
        init_ground_list(ground_list)
    if type(obstacle_list) == list: 
        init_obstacle_list(obstacle_list)
    if type(coin_list) == list:
        init_coin_list(coin_list)
    if type(background_list) == list:
        init_background_list(background_list)

def game_playing_easy():
    global score, is_collecting # liên kết score => cập nhật best_score
    y_top, y_bottom = 0, 0
    pygame.mixer.music.play()
    
    while True:
        for background in background_list: # IN BACKGROUND
            background.move()
            background.print_image(screen)
            
            if background.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                background.reset_position()

        for obstacle in obstacle_list: # IN OBSTACLE
            obstacle.move()
            obstacle.print_image(screen)
            
            if obstacle.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                if obstacle.give_score: # Nếu ống trên
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_top) # vị trí ống trên
                else:
                    (y_top, y_bottom) = random_obstacle_height() # thì random chiều cao cho cặp ống trên dưới mới này
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_bottom) # vị trí ống dưới

            if is_collided(current_character.x, current_character.y, current_character.hitbox, obstacle.x, obstacle.y, obstacle.hitbox): # Game over nếu có va chạm
                current_character.die()
                return "game_over"

            if not obstacle.is_scored and is_A_to_the_left_of_B(obstacle.x, current_character.x): # CẬP NHẬT ĐIỂM
                pygame.mixer.Sound.play(scoring_sound)
                score += 1
                obstacle.is_scored = True

        for ground in ground_list: # IN GROUND
            ground.move()
            ground.print_image(screen)
            
            if ground.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                ground.reset_position()

        if current_character.is_collided_with_the_map(False, False, True, True): # CHECK GAME OVER KHI CHIM BAY NGOÀI MAP
            current_character.die()
            return "game_over"

        current_character.move(is_collecting) # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        draw_text(str(score), FONT["MARIO_BIG"], COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 100) # IN ĐIỂM

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # chuột trái
                    is_collecting = False
                    current_character.jump()
                elif event.button == 3: # chuột phải
                    is_collecting = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    is_collecting = False
                    current_character.jump()
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    pygame.mixer.Sound.play(collecting_sound)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    is_collecting = False

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

def game_playing_normal():
    global score, is_collecting # liên kết score => cập nhật best_score
    y_top, y_bottom = 0, 0
    pygame.mixer.music.play()
    
    while True:
        update_game_speed(game_speed) # Tặng tốc game dần theo score

        for background in background_list: # IN BACKGROUND
            background.move()
            background.print_image(screen)
            
            if background.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                background.reset_position()

        for obstacle in obstacle_list: # IN OBSTACLE
            obstacle.move()
            obstacle.print_image(screen)
            
            if obstacle.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                if obstacle.give_score: # Nếu ống trên
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_top) # vị trí ống trên
                else:
                    (y_top, y_bottom) = random_obstacle_height() # thì random chiều cao cho cặp ống trên dưới mới này
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_bottom) # vị trí ống dưới

            if is_collided(current_character.x, current_character.y, current_character.hitbox, obstacle.x, obstacle.y, obstacle.hitbox): # Game over nếu có va chạm
                current_character.die()
                return "game_over"

            if not obstacle.is_scored and is_A_to_the_left_of_B(obstacle.x, current_character.x): # CẬP NHẬT ĐIỂM
                pygame.mixer.Sound.play(scoring_sound)
                score += 1
                obstacle.is_scored = True

        for ground in ground_list: # IN GROUND
            ground.move()
            ground.print_image(screen)
            
            if ground.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                ground.reset_position()

        if current_character.is_collided_with_the_map(False, False, True, True): # CHECK GAME OVER KHI CHIM BAY NGOÀI MAP
            current_character.die()
            return "game_over"

        current_character.move(is_collecting) # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        draw_text(str(score), FONT["MARIO_BIG"], COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 100) # IN ĐIỂM

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # chuột trái
                    is_collecting = False
                    current_character.jump()
                elif event.button == 3: # chuột phải
                    is_collecting = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    is_collecting = False
                    current_character.jump()
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    pygame.mixer.Sound.play(collecting_sound)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    is_collecting = False

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

def game_playing_hard():
    global number_of_coin, score, is_collecting, is_lack_of_coin # liên kết score => cập nhật best_score
    y_top, y_bottom = 0, 0
    pygame.mixer.music.play()
    
    while True:
        update_game_speed(game_speed) # Tặng tốc game dần theo score

        for background in background_list: # IN BACKGROUND
            background.move()
            background.print_image(screen)
            
            if background.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                background.reset_position()

        for obstacle in obstacle_list: # IN OBSTACLE
            obstacle.move()
            obstacle.print_image(screen)
            
            if obstacle.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                if is_lack_of_coin:
                    coin_x = random_coin_position() + obstacle_x_when_it_resets_position + obstacle_width
                    is_lack_of_coin = False
                    the_coin_that_need_to_be_reset_position.reset_position(coin_x, coin_y_when_it_resets_position)
                if obstacle.give_score: # Nếu ống trên
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_top) # vị trí ống trên
                else:
                    (y_top, y_bottom) = random_obstacle_height() # thì random chiều cao cho cặp ống trên dưới mới này
                    obstacle.reset_position(obstacle_x_when_it_resets_position, y_bottom) # vị trí ống dưới

            if is_collided(current_character.x, current_character.y, current_character.hitbox, obstacle.x, obstacle.y, obstacle.hitbox): # Game over nếu có va chạm
                current_character.die()
                return "game_over"

            if not obstacle.is_scored and is_A_to_the_left_of_B(obstacle.x, current_character.x): # CẬP NHẬT ĐIỂM
                pygame.mixer.Sound.play(scoring_sound)
                score += 1
                obstacle.is_scored = True

        for ground in ground_list: # IN GROUND
            ground.move()
            ground.print_image(screen)
            
            if ground.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                ground.reset_position()

        if current_character.is_collided_with_the_map(False, False, True, True): # CHECK GAME OVER KHI CHIM BAY NGOÀI MAP
            current_character.die()
            return "game_over"

        current_character.move(is_collecting) # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        for coin in coin_list:
            coin.move()
            coin.print_image(screen)

            if coin.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                is_lack_of_coin = True
                the_coin_that_need_to_be_reset_position = coin
                
            if not coin.is_scored and is_collided(coin.x, coin.y, coin.hitbox, current_character.x, current_character.y, current_character.collecting_range):
                coin.is_scored = True
                the_coin_that_need_to_be_reset_position = coin
                pygame.mixer.Sound.play(cow_sound)
                score += 1

            if is_collided(coin.x, coin.y, coin.hitbox, current_character.x, current_character.y, current_character.hitbox):
                current_character.die()
                return "game_over"

        draw_text(str(score), FONT["MARIO_BIG"], COLOR["ROYAL_BLUE"], WIDTH // 2, HEIGHT // 2 - 100) # IN ĐIỂM

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # chuột trái
                    is_collecting = False
                    current_character.jump()
                elif event.button == 3: # chuột phải
                    is_collecting = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    is_collecting = False
                    current_character.jump()
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    pygame.mixer.Sound.play(collecting_sound)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    is_collecting = False

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

def game_playing_hardcore():
    global number_of_coin, score, is_collecting, is_lack_of_coin # liên kết score => cập nhật best_score

    current_character = init_character(char_perry_plane_normal_image, char_perry_plane_normal_image, char_perry_plane_normal_image, char_perry_plane_normal_image)
    twin_towers = obstacle(twin_towers_image, x_first_spawn, 0, 0, 0, obstacle_velocity_x)

    while True:
        for background in background_list: # IN BACKGROUND
            background.move()
            background.print_image(screen)
            
            if background.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                background.reset_position()

        twin_towers.move()
        twin_towers.print_image(screen)

        if is_collided(current_character.x, current_character.y, current_character.hitbox, twin_towers.x, twin_towers.y, twin_towers.hitbox): # Game over nếu có va chạm
                current_character.die()
                pygame.mixer.Sound.play(plane_sound)
                return "game_over"

        for ground in ground_list: # IN GROUND
            ground.move()
            ground.print_image(screen)
            
            if ground.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                ground.reset_position()

        if current_character.is_collided_with_the_map(False, False, True, True): # CHECK GAME OVER KHI CHIM BAY NGOÀI MAP
            current_character.die()
            return "game_over"

        current_character.print_image(screen) # IN CHARACTER

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                
        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

def game_menu():
    global score, game_speed, is_collecting, is_lack_of_coin, current_game_mode
    is_lack_of_coin = False

    init_obj(ground_list, obstacle_list, coin_list, background_list)
    current_character.reset_position()
    
    hint = random.choice(RANDOM_HINT)

    if current_game_mode == "game_playing_hardcore":
        current_game_mode = "game_playing_easy"
    elif score >= 119:
        return "game_playing_hardcore"
    elif current_game_mode == "game_playing_easy" and score >= 20: # tăng độ khó khi đạt đủ score
        current_game_mode = "game_playing_normal"
        hint = "score 50 for cow girls"
    elif current_game_mode == "game_playing_normal" and score >= 50:
        current_game_mode = "game_playing_hard"

    score = 0 # reset score
    game_speed = min_game_speed

    while True:
        for background in background_list: # IN BACKGROUND
            background.move() 
            background.print_image(screen)
            
            if background.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ra ngoài map
                background.reset_position()

        for ground in ground_list: # IN GROUND
            ground.move()
            ground.print_image(screen)
            
            if ground.is_out_of_the_map(False, True, False, False): # Reset vị trí nếu ngoài map
                ground.reset_position()

        current_character.move() # Cập nhật vị trí
        current_character.act_at_menu() # animation ở menu
        current_character.print_image(screen) # IN CHARACTER

        draw_text("FLAPPY BIRD", FONT["MARIO_BIG"], COLOR["BROWN"], WIDTH // 2, HEIGHT // 2 - 100) # IN CHỮ Ở MENU
        draw_text("PRESS SPACE TO PLAY", FONT["MARIO_SMALL"], COLOR["MIDNIGHT_BLUE"], WIDTH // 2, HEIGHT // 2 + 100)
        draw_text(hint, FONT["MARIO_SMALL"], COLOR["MIDNIGHT_BLUE"], WIDTH // 2, HEIGHT // 2 + 150)

        for event in pygame.event.get(): # CHECK THAO TÁC
            if event.type == pygame.QUIT:
                return ""
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # chuột trái
                    is_collecting = False
                    current_character.jump()
                elif event.button == 3: # chuột phải
                    is_collecting = True
                return current_game_mode

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ""
                elif event.key == pygame.K_1:
                    score = 100
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    is_collecting = False
                    current_character.jump()
                elif event.key == pygame.K_DOWN:
                    is_collecting = True
                    pygame.mixer.Sound.play(collecting_sound)
                return current_game_mode

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    is_collecting = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    is_collecting = False

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

def game_over():
    global best_score, score, game_speed, current_character # liên kết score => cập nhật best_score; game_speed
    best_score = max(score, best_score)

    pygame.mixer.Sound.play(game_over_sound)

    while True:
        for background in background_list: # IN BACKGROUND
            background.print_image(screen)

        for obstacle in obstacle_list: # IN OBSTACLE
            obstacle.print_image(screen)

        for ground in ground_list: # IN GROUND
            ground.print_image(screen)

        current_character.move() # Cập nhật vị trí
        current_character.print_image(screen) # IN CHARACTER

        pygame.draw.rect(screen, COLOR["BABY_BLUE"], (20, 100, 380 - 20, 500 - 100)) # IN CHỮ
        draw_text("GAME OVER", FONT["MARIO_BIG"],  COLOR["BRONZE"], WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("Press space to play again", FONT["MARIO_SMALL"],  COLOR["BLACK"], WIDTH // 2, HEIGHT // 2 + 100)
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

                if event.key == pygame.K_SPACE: # Trở về menu
                    return "game_menu"

        pygame.display.flip() # CẬP NHẬT MÀN HÌNH
        pygame.time.Clock().tick(30) # FPS = 30

'''DƯỚI ĐÂY LÀ CÁC THÔNG SỐ CÓ THỂ ĐƯỢC TUỲ CHỈNH SAO CHO PHÙ HỢP VỚI NGƯỜI CHƠI'''

# TẠO NHẠC NỀN
pygame.mixer.music.load(soundtrack_1)

# THÔNG SỐ NHÂN VẬT
character_width = 50
character_height = 50
character_x = (WIDTH - 200) // 2
character_y = (HEIGHT - 50) // 2

# TẠO NHÂN VẬT
current_character = init_character(char_perry_ufo_normal_image, char_perry_ufo_start_jumping_image, char_perry_ufo_is_jumping_image, char_perry_ufo_is_collecting_image)
is_collecting = False

# THÔNG SỐ CỦA OBSTACLE
x_first_spawn = WIDTH * 1.5
distance_gap = 150 # Khoảng cách giữa 2 ống cống trên dưới
obstacle_width = 60
obstacle_height = 500 
obstacle_velocity_x = -5 # TỐC ĐỘ DI CHUYỂN CỦA ỐNG CỐNG
distance_between_obstacles = 200 # Khoảng cách giữa 2 chướng ngại vật
number_of_obstacle = 2 # Số lượng vật cản tối đa có thể xuất hiện trên màn hình = number_of_obstacle 
obstacle_x_when_it_resets_position = distance_between_obstacles * number_of_obstacle + (number_of_obstacle - 1) * obstacle_width  # VỊ TRÍ hoành độ của ống cống spawn lại sau khi bay ra khỏi màn hình

# THÔNG SỐ MẶT ĐẤT
ground_width = WIDTH
ground_height = 100
ground_velocity_x = obstacle_velocity_x

# THÔNG SỐ COINS: CON BÒ
number_of_coin = 1 # Số lượng coin tối đa có thể xuất hiện trên màn hình = number_of_coin
coin_width = 70
coin_height = coin_width / 39 * 27
coin_y_when_it_resets_position = HEIGHT - coin_height - ground_height # vị trí theo chiều Ox là random và dựa theo obstacle nên không có ở đây
coin_velocity_x = obstacle_velocity_x
is_lack_of_coin = True

# THÔNG SỐ BACKGROUND
background_velocity_x = -1

# TẠO DANH SÁCH image
obstacle_list = []
ground_list = [] 
coin_list = []
background_list = []
init_obj(ground_list, obstacle_list, coin_list, background_list)

# TỐC ĐỘ GAME
game_speed = 1 # khởi đầu là 1x
score_at_max_game_speed = 50 # Điểm dừng tăng tiến tốc độ game
min_game_speed = 1 # Tốc độ game ban đầu
max_game_speed = 3 # Tốc độ game tối đa
game_speed_accel = (max_game_speed - min_game_speed) / score_at_max_game_speed # gia tốc của tốc độ game => gia tốc của vận tốc theo hoành độ

# SCORES
score = 0
best_score = 0

# CÁC TRẠNG THÁI CỦA GAME
states = {
    "game_menu": game_menu,
    "game_playing_hard": game_playing_hard,
    "game_playing_normal": game_playing_normal,
    "game_playing_easy": game_playing_easy,
    "game_playing_hardcore": game_playing_hardcore,
    "game_over": game_over
}

# VÒNG LẶP CHÍNH CỦA GAME
current_state = "game_menu"
current_game_mode = "game_playing_easy"
while current_state:
    current_state = states[current_state]()

pygame.quit()
