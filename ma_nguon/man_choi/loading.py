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
        from ma_nguon.man_choi.maprunglinhvuc import MapRungLinhVucScene
        from ma_nguon.man_choi.equipment_screen import EquipmentScreen
        from ma_nguon.man_choi.gacha_trang_bi import GachaTrangBiScene

        if self.target_scene == "menu":
            self.game.current_scene = MenuScene(self.game)
        elif self.target_scene == "character_select" or self.target_scene == "chon_nhan_vat":
            self.game.current_scene = CharacterSelectScene(self.game)
        elif self.target_scene == "level1" or self.target_scene == "man1":
            self.game.current_scene = Level1Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "level2" or self.target_scene == "man2":
            self.game.current_scene = Level2Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu":
            self.game.current_scene = MapMuaThuScene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man1":
            self.game.current_scene = MapMuaThuMan1Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man2":
            self.game.current_scene = MapMuaThuMan2Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "map_mua_thu_man3":
            self.game.current_scene = MapMuaThuMan3Scene(self.game, player=self.game.selected_player)
        elif self.target_scene == "autumn_levels" or self.target_scene == "chon_man_mua_thu":
            self.game.current_scene = AutumnLevelsScene(self.game)
        elif self.target_scene == "map_cong_nghe":
            # Create the Map Công Nghệ scene (pass selected player if any)
            try:
                self.game.current_scene = MapCongNgheScene(self.game, player=self.game.selected_player)
            except Exception:
                # If scene init fails, fall back to menu
                try:
                    self.game.current_scene = MenuScene(self.game)
                except Exception:
                    self.game.current_scene = None
        elif self.target_scene == "map_rung_linh_vuc" or self.target_scene == "maprunglinhvuc":
            # Create the Map Rừng Linh Vực scene (pass selected player if any)
            try:
                self.game.current_scene = MapRungLinhVucScene(self.game, player=self.game.selected_player)
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
        elif self.target_scene == "gacha_trang_bi":
            self.game.current_scene = GachaTrangBiScene(self.game)
        elif self.target_scene == "equipment":
            # Get player if available
            player = getattr(self.game, 'selected_player', None)
            equipment_screen = EquipmentScreen(self.game, player)
            
            # Load equipment từ profile
            if hasattr(self.game, 'current_user') and self.game.current_user:
                try:
                    from ma_nguon.core import profile_manager
                    profile = profile_manager.load_profile(self.game.current_user)
                    character_equipment = profile.get('character_equipment', {})
                    
                    # Load equipment cho mỗi character
                    eq_manager = equipment_screen.equipment_manager
                    for char_id, eq_data in character_equipment.items():
                        eq_manager.load_character_equipment(char_id, eq_data)
                    print(f"✓ Đã load trang bị cho {len(character_equipment)} nhân vật")
                except Exception as e:
                    print(f"✗ Lỗi khi load trang bị: {e}")
            
            self.game.current_scene = equipment_screen

#mapninja
        elif self.target_scene == "map_ninja" or self.target_scene == "chon_man_ninja":
            from ma_nguon.man_choi.chon_man_ninja import AutumnLevelsSceneninja
            self.game.current_scene = AutumnLevelsSceneninja(self.game)

        elif self.target_scene == "map_ninja_man1":
            from ma_nguon.man_choi.map_ninja_man1 import mapninjaman1Scene
            self.game.current_scene = mapninjaman1Scene(self.game, player=self.game.selected_player)

        elif self.target_scene == "autumn_levels_ninja":
            from ma_nguon.man_choi.chon_man_ninja import AutumnLevelsSceneninja
            self.game.current_scene = AutumnLevelsSceneninja(self.game)

      
