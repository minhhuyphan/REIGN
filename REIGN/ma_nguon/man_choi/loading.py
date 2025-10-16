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
        
        # Hiệu ứng loading đặc biệt cho Map Công Nghệ
        if self.target_scene == "map_cong_nghe":
            # Nền đen với hiệu ứng tech
            screen.fill((10, 10, 30))
            
            # Loading text với màu cyan
            text = self.font.render("Đang tải Map Công Nghệ...", True, (0, 255, 255))
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2,
                               screen.get_height()//2 - text.get_height()//2))
            
            # Hiệu ứng loading bar đơn giản
            elapsed = time.time() - self.start_time
            progress = min(elapsed / 1.5, 1.0)  # 1.5 giây để load
            
            bar_width = 400
            bar_height = 20
            bar_x = screen.get_width()//2 - bar_width//2
            bar_y = screen.get_height()//2 + 50
            
            # Vẽ khung
            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            # Vẽ tiến trình
            pygame.draw.rect(screen, (0, 255, 255), (bar_x, bar_y, int(bar_width * progress), bar_height))
            
        else:
            # Loading bình thường
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
        from ma_nguon.man_choi.map_cong_nghe import MapCongNgheScene
        from ma_nguon.man_choi.equipment_scene import EquipmentScene

        if self.target_scene == "menu":
            self.game.current_scene = MenuScene(self.game)
        elif self.target_scene == "character_select":
            self.game.current_scene = CharacterSelectScene(self.game)
        elif self.target_scene == "level1":
            print(f"[DEBUG Loading] Creating Level1Scene with selected_player: {getattr(self.game, 'selected_player', None)}")
            sp = getattr(self.game, 'selected_player', None)
            if sp:
                print(f"[DEBUG Loading] selected_player stats: HP={getattr(sp,'hp',None)}, max_hp={getattr(sp,'max_hp',None)}, DMG={getattr(sp,'damage',None)}, SPD={getattr(sp,'speed',None)}")
            self.game.current_scene = Level1Scene(self.game, player=sp)
        elif self.target_scene == "level2":
            sp = getattr(self.game, 'selected_player', None)
            print(f"[DEBUG Loading] Creating Level2Scene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
            self.game.current_scene = Level2Scene(self.game, player=sp)
        elif self.target_scene == "map_mua_thu":
            sp = getattr(self.game, 'selected_player', None)
            print(f"[DEBUG Loading] Creating MapMuaThuScene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
            self.game.current_scene = MapMuaThuScene(self.game, player=sp)
        elif self.target_scene == "map_mua_thu_man1":
            sp = getattr(self.game, 'selected_player', None)
            print(f"[DEBUG Loading] Creating MapMuaThuMan1Scene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
            self.game.current_scene = MapMuaThuMan1Scene(self.game, player=sp)
        elif self.target_scene == "map_mua_thu_man2":
            sp = getattr(self.game, 'selected_player', None)
            print(f"[DEBUG Loading] Creating MapMuaThuMan2Scene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
            self.game.current_scene = MapMuaThuMan2Scene(self.game, player=sp)
        elif self.target_scene == "map_mua_thu_man3":
            sp = getattr(self.game, 'selected_player', None)
            print(f"[DEBUG Loading] Creating MapMuaThuMan3Scene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
            self.game.current_scene = MapMuaThuMan3Scene(self.game, player=sp)
        elif self.target_scene == "autumn_levels":
            self.game.current_scene = AutumnLevelsScene(self.game)
        elif self.target_scene == "map_cong_nghe":
            # Create the Map Công Nghệ scene (pass selected player if any)
            try:
                sp = getattr(self.game, 'selected_player', None)
                print(f"[DEBUG Loading] Creating MapCongNgheScene with selected_player stats: HP={getattr(sp,'hp',None) if sp else None}, DMG={getattr(sp,'damage',None) if sp else None}")
                self.game.current_scene = MapCongNgheScene(self.game, player=sp)
            except Exception:
                # If scene init fails, fall back to menu
                try:
                    self.game.current_scene = MenuScene(self.game)
                except Exception:
                    self.game.current_scene = None
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
        elif self.target_scene == "spin":
            from ma_nguon.man_choi.spin import SpinScene
            self.game.current_scene = SpinScene(self.game)
        elif self.target_scene == "equipment":
            self.game.current_scene = EquipmentScene(self.game, player=self.game.selected_player)


      
