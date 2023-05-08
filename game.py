import pygame, random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, display_surface
from monster import MyMonsters

FPS = 60
# Class Game dùng để điều khiển các thao tác trong hệ thống
class Game:
    def __init__(self, hunter, monster_group):
        # Khởi tạo các giá trị trong Game
        self.score = 0 # Điểm số
        self.round = 0 # Số vòng chơi
        self.time = 0 # Thời gian chơi được
        self.frame = 0 # Tốc độ khung hình

        self.hunter = hunter
        self.monster_group = monster_group

        # Tạo sound khi chuyển level
        self.next_sound = pygame.mixer.Sound("sounds/next_level.wav")

        # Tạo font chữ
        self.font = pygame.font.Font("fonts/arial.ttf", 24)

        # Tạo các loại monster
        blue_monster = pygame.image.load("images/blue_monster.png")
        green_monster = pygame.image.load("images/green_monster.png")
        purple_monster = pygame.image.load("images/purple_monster.png")
        yellow_monster = pygame.image.load("images/yellow_monster.png")

        # Tạo monster từ các loại khi random
        self.monster_images = [blue_monster, green_monster, purple_monster, yellow_monster]
        self.monster_random = random.randint(0, 3)
        self.monster_image = self.monster_images[self.monster_random]

        # Set tọa độ monster khi mới vô
        self.monster_rect = self.monster_image.get_rect()
        self.monster_rect.centerx = SCREEN_WIDTH//2
        self.monster_rect.top = 30

    def update(self):
        """Cập nhật lại các đối tượng trong Game"""
        self.frame += 1
        if self.frame == FPS:
            self.time += 1
            self.frame = 0

        # Check for collisions
        self.check_collisions()
    
    def draw(self):
        """Hàm dùng đễ vẽ các đối tượng lên màn hình game"""
        # Tạo màu sắc
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # Thêm màu quái vật vào danh sách trong đó chỉ mục của màu khớp với monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # Set text
        catch_text = self.font.render("Mục Tiêu", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = SCREEN_WIDTH//2
        catch_rect.top = 3

        score_text = self.font.render("Điểm Số: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Số Mạng: " + str(self.hunter.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Vòng: " + str(self.round), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Thời Gian: " + str(self.time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (SCREEN_WIDTH - 10, 5)

        safe_text = self.font.render("Số Lượt Về: " + str(self.hunter.safes), True, WHITE)
        safe_rect = safe_text.get_rect()
        safe_rect.topright = (SCREEN_WIDTH - 10, 35)

        # Gán các text cho các khối rect chứa nó
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(safe_text, safe_rect)
        display_surface.blit(self.monster_image, self.monster_rect)

        """Vẽ khối viền chứa mục tiêu và khuôn cho các quái vật di chuyển: 
            + Đối số 1: chứa màn hình mà đối tượng cần hiển thị
            + Đối số 2: Màu sắc khối viền
            + Đối số 3: Vị trí hiển thị khối viền
            + Đối số 4: Độ dày khung viền"""
        pygame.draw.rect(display_surface, colors[self.monster_random], (SCREEN_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.monster_random], (0, 100, SCREEN_WIDTH, SCREEN_HEIGHT - 200), 4)
 
    def check_collisions(self):
        """Kiểm tra va chạm giữa hunter và các con quái vật"""
        # Dùng hàm spritecollideany() để kiểm tra va chạm
        collided_monster = pygame.sprite.spritecollideany(self.hunter, self.monster_group)

        # Nếu có va chạm sẽ thực hiện các lệnh dưới đây
        if collided_monster:
            # Nếu va chạm đúng con quái được chỉ định
            if collided_monster.type == self.monster_random:
                self.score += 100 * self.round
                # Xóa con quái bị va chạm ra khỏi monster_group
                collided_monster.remove(self.monster_group)
                if self.monster_group:  # Nếu vòng chơi còn quái vật thì sẽ tiếp tục chơi
                    self.hunter.kill_sound.play()
                    self.chose_new_target()
                else: # Nếu không (tức đã hoàn thành vòng chơi)
                    self.hunter.reset()
                    self.start_new_round()
            # Nếu va chạm sai
            else:
                self.hunter.die_sound.play()
                self.hunter.lives -= 1
                # Kiểm tra số mạng còn đủ để tiếp tục không
                if self.hunter.lives <= 0:
                    self.pause_game("Tổng Điểm: " + str(self.score), "Vui lòng nhấn 'Enter' chơi lại")
                    self.reset_game()
                self.hunter.reset()

    def start_new_round(self):
        """Bắt đầu vòng chơi mới"""
        # Cung cấp phần thưởng điểm dựa trên tốc độ kết thúc vòng đấu
        self.score += int(10000 * self.round / (1 + self.time))

        # Reset các giá trị sau đây
        self.time = 0
        self.frame = 0
        self.round += 1
        self.hunter.safes += 1
        self.hunter.lives += 1

        # Xóa mọi quái vật còn lại khi reset game
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add các monster vào monster_group
        for _ in range(self.round):
            self.monster_group.add(
                MyMonsters(random.randint(0, SCREEN_WIDTH - 64), 
                           random.randint(100, SCREEN_HEIGHT - 164), 
                           self.monster_images[0], 
                           0))
            self.monster_group.add(
                MyMonsters(random.randint(0, SCREEN_WIDTH - 64), 
                           random.randint(100, SCREEN_HEIGHT - 164), 
                           self.monster_images[1], 
                           1))
            self.monster_group.add(
                MyMonsters(random.randint(0, SCREEN_WIDTH - 64), 
                           random.randint(100, SCREEN_HEIGHT - 164), 
                           self.monster_images[2], 
                           2))
            self.monster_group.add(
                MyMonsters(random.randint(0, SCREEN_WIDTH - 64), 
                           random.randint(100, SCREEN_HEIGHT - 164), 
                           self.monster_images[3], 
                           3))

        # Chọn một mục tiêu mới
        self.chose_new_target()

        self.next_sound.play()

    def chose_new_target(self):
        """Chọn 1 mục tiêu mới cho hunter tấn công"""
        target_monster = random.choice(self.monster_group.sprites())
        self.monster_random = target_monster.type
        self.monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        """Dừng game"""
        global running

        # Set màu sắc
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Tạo text khi dừng chương trình game
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        # Tạo sub text khi dừng chương trình game
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 32)

        # Hiển thị text khi dừng màn hình
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Thao tác các nút khi dừng màn hình
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        """Reset lại game"""
        self.score = 0
        self.round = 0

        self.hunter.lives = 5
        self.hunter.safes = 2
        self.hunter.reset()

        self.start_new_round()