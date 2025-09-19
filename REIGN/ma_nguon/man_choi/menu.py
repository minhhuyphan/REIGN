import pygame
class MenuScene:
    def __init__(self, game):
        self.game = game  # Tham chiếu đến GameManager hoặc SceneManager
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 50)
        self.selected = 0
        self.options = ["Màn 1", "Màn 2", "Hướng dẫn", "Thoát"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    # Lưu thông tin là chọn Màn 1
                    self.game.target_level = "level1"
                    self.game.change_scene("character_select")
                elif self.selected == 1:
                    # Lưu thông tin là chọn Màn 2
                    self.game.target_level = "level2"
                    self.game.change_scene("character_select")
                elif self.selected == 2:
                    self.game.change_scene("help")
                elif self.selected == 3:
                    self.game.running = False

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 60))
        title = self.font.render("GAME PYGAME", True, (255, 255, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 100))
        for i, text in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (180, 180, 180)
            option = self.font.render(text, True, color)
            screen.blit(option, (screen.get_width()//2 - option.get_width()//2, 250 + i*70))