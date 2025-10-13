import pygame
import os
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character

class CharacterSelectScene:
    def __init__(self, game):
        self.game = game
        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()
        self.font_big = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 60)
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)

        self.characters = [
            {
                "name": "Chiến binh",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_binh",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/chien_binh/dung_yen/0.png"),
                "stats": {"hp": 500, "speed": 5, "damage": 30, "defense": 2},
                "color": (0, 255, 0)
            },
            {
                "name": "Ninja",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/ninja",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/ninja/dung_yen/0.png"),
                "stats": {"hp": 350, "speed": 8, "damage": 25, "defense": 1},
                "color": (0, 0, 255)
            },
            {
                "name": "Võ sĩ",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/vo_si",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/vo_si/dung_yen/0.png"),
                "stats": {"hp": 600, "speed": 4, "damage": 40, "defense": 3},
                "color": (255, 0, 0)
            },
            {
                "name": "Thợ Săn Quái Vật",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat/dung_yen/0.png"),
                "stats": {"hp": 450, "speed": 7, "damage": 35, "defense": 2},
                "color": (128, 0, 128)  # Màu tím đặc trưng cho thợ săn
            },
            {
                "name": "Chiến Thần Lạc Hồng",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong/dung_yen/0.png"),
                "stats": {"hp": 750, "speed": 6, "damage": 50, "defense": 4},
                "color": (255, 0, 127)  # Màu hồng đỏ đặc trưng
            }
        ]
        self.selected_idx = 0
        self.confirm = False
        self.preview_scale = 0.5  # Tỉ lệ phóng to ảnh preview
        
    def _load_preview(self, path):
        try:
            return pygame.image.load(path).convert_alpha()
        except:
            # Tạo ảnh mẫu nếu không tìm thấy
            img = pygame.Surface((100, 150), pygame.SRCALPHA)
            img.fill((150, 150, 150, 200))
            return img
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_idx = (self.selected_idx - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_idx = (self.selected_idx + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN:
                self.confirm = True
                self._create_player()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
    
    def _create_player(self):
        selected = self.characters[self.selected_idx]
        controls = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "attack": pygame.K_a,
            "kick": pygame.K_s,
            "defend": pygame.K_d,
            "jump": pygame.K_w,
        }
        
        # Tạo nhân vật với thuộc tính phù hợp
        player = Character(100, 300, selected["folder"], controls, selected["color"])
        
        # Cập nhật các thuộc tính từ stats
        player.hp = selected["stats"]["hp"]
        player.max_hp = selected["stats"]["hp"]
        player.speed = selected["stats"]["speed"]
        player.damage = selected["stats"]["damage"]
        player.defense = selected["stats"]["defense"]
        
        # Lưu nhân vật đã chọn vào game
        # Lưu nhân vật đã chọn vào game
        self.game.selected_player = player
        
        # Chuyển sang màn chơi đã chọn từ menu
        self.game.change_scene(self.game.target_level)
        
    def update(self):
        if self.confirm:
            # Hiệu ứng chọn nhân vật
            pass
    
    def draw(self, screen):
        # Vẽ nền
        screen.fill((30, 30, 60))
        
        # Tiêu đề
        title = self.font_big.render("CHỌN NHÂN VẬT", True, (255, 255, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Vẽ các nhân vật (5 nhân vật cạnh nhau - điều chỉnh spacing)
        num_characters = len(self.characters)
        spacing = self.screen_width // (num_characters + 1)
        
        for i, char in enumerate(self.characters):
            # Vị trí mỗi nhân vật - thu nhỏ khoảng cách để fit 5 nhân vật
            pos_x = spacing * (i + 1)
            pos_y = self.screen_height // 2 - 80
            
            # Vẽ khung nhân vật với hiệu ứng đặc biệt cho nhân vật được chọn
            if i == self.selected_idx:
                frame_color = (255, 215, 0)  # Vàng gold cho nhân vật được chọn
                # Vẽ hiệu ứng glow
                glow_rect = pygame.Rect(pos_x - 85, pos_y - 25, 170, 280)  # Thu nhỏ khung
                pygame.draw.rect(screen, (255, 255, 0, 50), glow_rect, 6)
            else:
                frame_color = (100, 100, 100)
            
            # Khung chính - thu nhỏ để fit 5 nhân vật
            main_rect = pygame.Rect(pos_x - 80, pos_y - 20, 160, 260)
            pygame.draw.rect(screen, frame_color, main_rect, 3)
            
            # Vẽ tên nhân vật với màu đặc biệt
            name_color = (255, 255, 0) if i == self.selected_idx else (255, 255, 255)
            # Font nhỏ hơn cho tên dài
            font_name = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
            name = font_name.render(char["name"], True, name_color)
            screen.blit(name, (pos_x - name.get_width()//2, pos_y - 50))
            
            # Vẽ ảnh preview - thu nhỏ hơn để fit 5 nhân vật
            preview = char["preview"]
            preview_scale = 0.35  # Thu nhỏ hơn để vừa 5 nhân vật
            preview = pygame.transform.scale(preview, 
                                          (int(preview.get_width() * preview_scale), 
                                           int(preview.get_height() * preview_scale)))
            screen.blit(preview, (pos_x - preview.get_width()//2, pos_y - 10))
            
            # Vẽ thông số với font nhỏ hơn
            stats_y = pos_y + 120
            stats = char["stats"]
            font_stats = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 18)  # Font nhỏ hơn
            
            hp_text = font_stats.render(f"HP: {stats['hp']}", True, (255, 100, 100))
            screen.blit(hp_text, (pos_x - 70, stats_y))
            
            speed_text = font_stats.render(f"Tốc độ: {stats['speed']}", True, (100, 255, 100))
            screen.blit(speed_text, (pos_x - 70, stats_y + 22))
            
            dmg_text = font_stats.render(f"ST: {stats['damage']}", True, (255, 255, 100))
            screen.blit(dmg_text, (pos_x - 70, stats_y + 44))
            
            def_text = font_stats.render(f"PT: {stats['defense']}", True, (100, 100, 255))
            screen.blit(def_text, (pos_x - 70, stats_y + 66))
            
            # Thêm chỉ báo đặc biệt
            if char["name"] == "Chiến Thần Lạc Hồng":
                special_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 16).render("★ HUYỀN THOẠI ★", True, (255, 0, 127))
                screen.blit(special_text, (pos_x - special_text.get_width()//2, stats_y + 88))
            elif char["name"] == "Thợ Săn Quái Vật":
                special_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 16).render("⚔ CHUYÊN GIA ⚔", True, (128, 0, 128))
                screen.blit(special_text, (pos_x - special_text.get_width()//2, stats_y + 88))
        
        # Hướng dẫn
        guide = self.font_small.render("← → để chọn, ENTER để xác nhận, ESC để quay lại", True, (200, 200, 200))
        screen.blit(guide, (self.screen_width//2 - guide.get_width()//2, self.screen_height - 40))