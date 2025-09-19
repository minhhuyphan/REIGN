import pygame, sys
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.man_choi.menu import MenuScene
from ma_nguon.man_choi.chon_nhan_vat import CharacterSelectScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # --- Cấu hình cửa sổ ---
        self.WIDTH, self.HEIGHT = 1600, 700
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Có Âm Thanh & Animation")
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.selected_player = None
        self.target_level = "level1" 
        # --- Camera và map ---
        self.camera_x = 0
        self.map_width = self.WIDTH * 3  # Map dài gấp 3 màn hình
        
        # --- Load ảnh nền ---
        self.bg_image = pygame.image.load("tai_nguyen/hinh_anh/giao_dien/bg.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.map_width, self.HEIGHT))
        # --- Load nhạc nền ---
        try:
            pygame.mixer.music.load("tai_nguyen/am_thanh/nhac/bg.mp3")  # đổi sang mp3/wav/ogg
            pygame.mixer.music.play(-1)  # phát lặp vô hạn
        except Exception as e:
            print("Không load được nhạc nền:", e)

        # --- Scene quản lý ---
        self.running = True
        self.current_scene = MenuScene(self)

    def change_scene(self, scene_name):
        from ma_nguon.man_choi.loading import LoadingScene
        if scene_name == "exit":
            self.running = False
        elif scene_name == "game_over":
            # Chuyển trực tiếp đến Game Over mà không qua Loading
            if hasattr(self, 'game_over_scene'):
                self.current_scene = self.game_over_scene
            else:
                # Fallback nếu không có scene được tạo trước
                from ma_nguon.man_choi.game_over import GameOverScene
                self.current_scene = GameOverScene(self, "Unknown", 0)
        else:
            # Luôn dùng LoadingScene để chuyển tiếp
            self.current_scene = LoadingScene(self, scene_name)
    
    def load_scene(self, scene_name, level_name="Unknown", score=0):
        """Tạo scene mới mà không chuyển đổi ngay lập tức"""
        if scene_name == "game_over":
            from ma_nguon.man_choi.game_over import GameOverScene
            return GameOverScene(self, level_name, score)
        return None
            
    def draw_player_health_bar(self, screen, player):
        """Vẽ thanh máu ở góc màn hình"""
        if not player:
            return
            
        # Vị trí và kích thước thanh máu
        bar_x = 20
        bar_y = 20
        bar_width = 300
        bar_height = 30
        
        # Vẽ khung
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Vẽ nền máu tối (biểu thị máu đã mất)
        pygame.draw.rect(screen, (150, 0, 0), (bar_x + 3, bar_y + 3, bar_width - 6, bar_height - 6))
        
        # Vẽ máu hiện tại
        health_width = int((player.hp / player.max_hp) * (bar_width - 6))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x + 3, bar_y + 3, health_width, bar_height - 6))
        
        # Vẽ viền ngoài
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Vẽ số máu
        if hasattr(self, 'font_manager'):
            font = self.font_manager.get_font(size=20)
        else:
            font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 20)
            
        health_text = f"{player.hp}/{player.max_hp} HP"
        text_surf = font.render(health_text, True, (255, 255, 255))
        text_x = bar_x + bar_width // 2 - text_surf.get_width() // 2
        text_y = bar_y + bar_height // 2 - text_surf.get_height() // 2
        screen.blit(text_surf, (text_x, text_y))
        
        # Thêm avatar nhân vật (tuỳ chọn)
        if player.image:
            avatar_size = bar_height * 2
            avatar_x = bar_x + bar_width + 10
            avatar_y = bar_y - bar_height // 2
            
            # Lấy frame đầu tiên của animation dung_yen
            if "dung_yen" in player.animations and player.animations["dung_yen"]:
                avatar = player.animations["dung_yen"][0]
                # Scale ảnh về kích thước phù hợp
                avatar = pygame.transform.scale(avatar, (avatar_size, avatar_size))
                # Vẽ khung ảnh
                pygame.draw.rect(screen, player.color, 
                            (avatar_x - 2, avatar_y - 2, avatar_size + 4, avatar_size + 4), 2)
                # Vẽ ảnh
                screen.blit(avatar, (avatar_x, avatar_y))

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_event(event)
            
            # Xóa màn hình trước khi vẽ frame mới
            self.screen.fill((0, 0, 0))  # Đảm bảo xóa hết màn hình trước mỗi frame
            
            self.current_scene.update()
            self.current_scene.draw(self.screen)
            
            # Vẽ thanh máu của người chơi nếu đang ở trong màn chơi
            if hasattr(self.current_scene, 'player'):
                self.draw_player_health_bar(self.screen, self.current_scene.player)
            
            pygame.display.flip()
        pygame.quit()
        sys.exit()