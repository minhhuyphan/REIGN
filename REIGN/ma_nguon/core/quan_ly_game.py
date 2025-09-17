import pygame, sys
from ma_nguon.doi_tuong.nhan_vat import Character


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # --- Cấu hình cửa sổ ---
        WIDTH, HEIGHT = 1600, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Có Âm Thanh & Animation")
        self.clock = pygame.time.Clock()
        self.screen = screen
        # --- Load ảnh nền ---
        self.bg_image = pygame.image.load("tai_nguyen/hinh_anh/giao_dien/bg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        # --- Load nhạc nền ---
        try:
            pygame.mixer.music.load("tai_nguyen/am_thanh/nhac/bg.crdownload")  # đổi sang mp3/wav/ogg
            pygame.mixer.music.play(-1)  # phát lặp vô hạn
        except Exception as e:
            print("Không load được nhạc nền:", e)

        # Nhân vật
        folder = "tai_nguyen/hinh_anh/nhan_vat"
        controls_p1 = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "attack": pygame.K_a,
            "kick": pygame.K_s,
            "defend": pygame.K_d,
            "jump": pygame.K_w,
        }
        self.player1 = Character(100, 300, folder, controls_p1, color=(0,255,0))
        self.enemy = Character(700, 300, folder, {}, color=(255,0,0), auto=True)

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.screen.blit(self.bg_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player1.update(keys)
            self.enemy.update(keys, target=self.player1)

            # Va chạm
            rect1 = self.player1.image.get_rect(topleft=(self.player1.x, self.player1.y))
            rect2 = self.enemy.image.get_rect(topleft=(self.enemy.x, self.enemy.y))
            if rect1.colliderect(rect2):
                if self.player1.state in ["danh", "da"] and self.enemy.hp > 0 and not self.enemy.actioning:
                    self.enemy.hp -= 1
                if self.enemy.state in ["danh", "da"] and self.player1.hp > 0 and not self.player1.actioning:
                    self.player1.hp -= 1

            self.player1.draw(self.screen)
            self.enemy.draw(self.screen)

            pygame.display.flip()
        pygame.quit()
        sys.exit()