# ma_nguon/man_choi/loading.py
import pygame, time

class LoadingScene:
    def __init__(self, game, target_scene):
        self.game = game
        self.target_scene = target_scene
        self.start_time = time.time()
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 40)

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
        from ma_nguon.man_choi.map_mua_thu import MapMuaThuScene
        from ma_nguon.man_choi.map_mua_thu_man1 import MapMuaThuMan1Scene
        from ma_nguon.man_choi.map_mua_thu_man2 import MapMuaThuMan2Scene
        from ma_nguon.man_choi.map_mua_thu_man3 import MapMuaThuMan3Scene
        from ma_nguon.man_choi.chon_man_mua_thu import AutumnLevelsScene
        from ma_nguon.man_choi.help import HelpScene
        from ma_nguon.man_choi.victory import VictoryScene
        from ma_nguon.man_choi.settings import SettingsScene
        from ma_nguon.man_choi.login import LoginScene
        from ma_nguon.man_choi.register import RegisterScene
        from ma_nguon.man_choi.shop import ShopScene

        if self.target_scene == "menu":
            self.game.current_scene = MenuScene(self.game)
        elif self.target_scene == "character_select":
            self.game.current_scene = CharacterSelectScene(self.game)
        elif self.target_scene == "level1":
            self.game.current_scene = Level1Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "level2":
            self.game.current_scene = Level2Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu":
            self.game.current_scene = MapMuaThuScene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man1":
            self.game.current_scene = MapMuaThuMan1Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man2":
            self.game.current_scene = MapMuaThuMan2Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man3":
            self.game.current_scene = MapMuaThuMan3Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "autumn_levels":
            self.game.current_scene = AutumnLevelsScene(self.game)
        elif self.target_scene == "help":
            self.game.current_scene = HelpScene(self.game)
        elif self.target_scene == "victory":
            self.game.current_scene = VictoryScene(self.game)
        elif self.target_scene == "settings":
            self.game.current_scene = SettingsScene(self.game)
        elif self.target_scene == "login":
            self.game.current_scene = LoginScene(self.game)
        elif self.target_scene == "register":
            self.game.current_scene = RegisterScene(self.game)
        elif self.target_scene == "shop":
            self.game.current_scene = ShopScene(self.game)
