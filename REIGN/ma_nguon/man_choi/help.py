import pygame

class HelpScene:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 50)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 30))
        text = self.font.render("Hướng dẫn chơi:", True, (0,255,255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 150))
        hd = self.font.render("- Mũi tên: Di chuyển", True, (255,255,255))
        screen.blit(hd, (screen.get_width()//2 - hd.get_width()//2, 220))
        hd2 = self.font.render("- A/S/D/W: Đánh/Đá/Đỡ/Nhảy", True, (255,255,255))
        screen.blit(hd2, (screen.get_width()//2 - hd2.get_width()//2, 270))
        info = self.font.render("Nhấn ESC để về menu", True, (255,255,0))
        screen.blit(info, (screen.get_width()//2 - info.get_width()//2, 350))
