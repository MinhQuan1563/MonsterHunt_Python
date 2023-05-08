import pygame, random
from constants import display_surface, SCREEN_WIDTH, SCREEN_HEIGHT

class MyMonsters(pygame.sprite.Sprite):
    def __init__(self, x, y, image, monster_type):
        super().__init__()

        """Tạo ảnh monster theo tham số image bất kì truyền vào và set tọa độ cho chúng"""
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # (type) Loại quái được xác định bằng các số nguyên: 
        # 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow
        self.type = monster_type

        # Tạo tọa độ và vận tốc ngẫu nhiên
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.veloc = random.randint(1, 5)

    def update(self):
        """Cập nhật các tọa độ của quái vật theo vận tốc"""
        self.rect.x += self.dx * self.veloc
        self.rect.y += self.dy * self.veloc

        # Giới hạn di chuyển của quái vật ở các cạnh của màn hình
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 100 or self.rect.bottom >= SCREEN_HEIGHT - 100:
            self.dy *= -1

