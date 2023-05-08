import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class MyHunter(pygame.sprite.Sprite):
    def __init__(self):
        """Khởi tạo nhân vật hunter"""
        super().__init__()

        self.image = pygame.image.load("images/hunter.png")
        self.rect = self.image.get_rect()   # get_rect() là để lấy ra khối ảnh đó và xử lý nó
        self.rect.centerx = SCREEN_WIDTH//2 # Tọa độ trục hoành
        self.rect.bottom = SCREEN_HEIGHT    # Tọa độ trục tung

        self.lives = 5 # Số mạng của nhân vật
        self.safes = 3 # Số lần được trở về vùng an toàn
        self.veloc = 8 # Tốc độ di chuyển của hunter

        # Âm thanh nhân vật
        self.kill_sound = pygame.mixer.Sound("sounds/kill.wav")
        self.die_sound = pygame.mixer.Sound("sounds/die.wav")
        self.safe_sound = pygame.mixer.Sound("sounds/safe.wav")

    def update(self):
        """Cập nhật các chuyển động của nhân vật"""
        keys = pygame.key.get_pressed()

        # Bắt sự kiện ấn phím và giới hạn tọa độ của nhân vật
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.veloc
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.veloc
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.veloc
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 100:
            self.rect.y += self.veloc

    def safe(self):
        """Kiểm tra vùng an toàn của nhân vật"""
        if self.safes > 0:
            self.safes -= 1
            self.safe_sound.play()
            self.rect.bottom = SCREEN_HEIGHT

    def reset(self):
        """Reset lại vị trí của nhân vật về ban đầu"""
        self.rect.centerx = SCREEN_WIDTH//2
        self.rect.bottom = SCREEN_HEIGHT





