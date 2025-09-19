# ma_nguon/man_choi/loading.py
import pygame, time

class LoadingScene:
    def __init__(self, game, target_scene):
        self.game = game
        self.target_scene = target_scene
        self.start_time = time.time()
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 40)

    def handle_event(self, event):
        pass  # không cần xử lý input khi loading

    def update(self):
        # Sau 1.5 giây thì đổi sang scene thật
        if time.time() - self.start_time > 1.5:
            self.load_next_scene()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("Đang tải...", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2,
                           screen.get_height()//2 - text.get_height()//2))

    def load_next_scene(self):
        from ma_nguon.man_choi.menu import MenuScene
        from ma_nguon.man_choi.chon_nhan_vat import CharacterSelectScene
        from ma_nguon.man_choi.man1 import Level1Scene
        from ma_nguon.man_choi.man2 import Level2Scene
        from ma_nguon.man_choi.help import HelpScene
        from ma_nguon.man_choi.victory import VictoryScene

        if self.target_scene == "menu":
            self.game.current_scene = MenuScene(self.game)
        elif self.target_scene == "character_select":
            self.game.current_scene = CharacterSelectScene(self.game)
        elif self.target_scene == "level1":
            self.game.current_scene = Level1Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "level2":
            self.game.current_scene = Level2Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "help":
            self.game.current_scene = HelpScene(self.game)
        elif self.target_scene == "victory":
            self.game.current_scene = VictoryScene(self.game)
