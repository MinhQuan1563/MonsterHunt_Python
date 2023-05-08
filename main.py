import pygame
from constants import display_surface
from hunter import MyHunter
from monster import MyMonsters
from game import Game

pygame.init()
FPS = 60

# Tạo background image và vị trí background đó xuất hiện
background_image = pygame.image.load("images/background.jpg")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

# Gọi đối tượng hunter và tạo hunter_group để lưu trữ
hunter_group = pygame.sprite.Group()
hunter = MyHunter()
hunter_group.add(hunter)

# Tạo monster_group để lưu trữ
monster_group = pygame.sprite.Group()

# hàm main
def main():
    running = True
    clock = pygame.time.Clock()

    # Tạo đối tượng Game
    my_game = Game(hunter,monster_group)
    my_game.pause_game("Monster Hunt", "Vui lòng nhấn 'Enter' để bắt đầu")
    my_game.reset_game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Nếu người chơi muốn về vùng an toàn
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hunter.safe()

        # Gán background image cho display_surface
        display_surface.blit(background_image, background_rect)
        
        # Cập nhật và vẽ các group lên màn hình
        hunter_group.update()
        hunter_group.draw(display_surface)
    
        monster_group.update()
        monster_group.draw(display_surface)
    
        # Cập nhật và gọi hàm vẽ các đối tượng trong game
        my_game.update()
        my_game.draw()
    
        """Cập nhật game và giới hạn số khung hình mỗi giây
            của chương trình"""
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

main()


