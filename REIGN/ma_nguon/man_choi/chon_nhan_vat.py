import pygame
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from doi_tuong.nhan_vat.nhan_vat import Character

class CharacterSelectScene:
    def __init__(self, game):
        self.game = game
        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()
        self.font_big = pygame.font.Font("../Tai_nguyen/font/Fz-Futurik.ttf", 60)
        self.font = pygame.font.Font("../Tai_nguyen/font/Fz-Futurik.ttf", 50)
        self.font_small = pygame.font.Font("../Tai_nguyen/font/Fz-Futurik.ttf", 30)

        self.characters = [
            {
                "name": "Chiến binh",
                "folder": "../Tai_nguyen/hinh_anh/nhan_vat/chien_binh",
                "preview": self._load_preview("../Tai_nguyen/hinh_anh/nhan_vat/chien_binh/dung_yen/0.png"),
                "stats": {"hp": 500, "speed": 5, "damage": 30, "defense": 2},
                "color": (0, 255, 0)
            },
            {
                "name": "Ninja",
                "folder": "../Tai_nguyen/hinh_anh/nhan_vat/ninja",
                "preview": self._load_preview("../Tai_nguyen/hinh_anh/nhan_vat/ninja/dung_yen/0.png"),
                "stats": {"hp": 350, "speed": 8, "damage": 25, "defense": 1},
                "color": (0, 0, 255)
            },
            {
                "name": "Võ sĩ",
                "folder": "../Tai_nguyen/hinh_anh/nhan_vat/vo_si",
                "preview": self._load_preview("../Tai_nguyen/hinh_anh/nhan_vat/vo_si/dung_yen/0.png"),
                "stats": {"hp": 600, "speed": 4, "damage": 40, "defense": 3},
                "color": (255, 0, 0)
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
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        # Vẽ các nhân vật (3 nhân vật cạnh nhau)
        spacing = self.screen_width // 4
        
        for i, char in enumerate(self.characters):
            # Vị trí mỗi nhân vật
            pos_x = spacing * (i + 1)
            pos_y = self.screen_height // 2 - 100
            
            # Vẽ khung nhân vật
            frame_color = (255, 255, 0) if i == self.selected_idx else (100, 100, 100)
            pygame.draw.rect(screen, frame_color, (pos_x - 100, pos_y - 20, 200, 300), 3)
            
            # Vẽ tên nhân vật
            name = self.font.render(char["name"], True, (255, 255, 255))
            screen.blit(name, (pos_x - name.get_width()//2, pos_y - 60))
            
            # Vẽ ảnh preview
            preview = char["preview"]
            preview = pygame.transform.scale(preview, 
                                          (preview.get_width() * self.preview_scale, 
                                           preview.get_height() * self.preview_scale))
            screen.blit(preview, (pos_x - preview.get_width()//2, pos_y))
            
            # Vẽ thông số
            stats_y = pos_y + 180
            stats = char["stats"]
            hp_text = self.font_small.render(f"HP: {stats['hp']}", True, (255, 255, 255))
            screen.blit(hp_text, (pos_x - 80, stats_y))
            
            speed_text = self.font_small.render(f"Tốc độ: {stats['speed']}", True, (255, 255, 255))
            screen.blit(speed_text, (pos_x - 80, stats_y + 30))
            
            dmg_text = self.font_small.render(f"Sát thương: {stats['damage']}", True, (255, 255, 255))
            screen.blit(dmg_text, (pos_x - 80, stats_y + 60))
            
            def_text = self.font_small.render(f"Phòng thủ: {stats['defense']}", True, (255, 255, 255))
            screen.blit(def_text, (pos_x - 80, stats_y + 90))
        
        # Hướng dẫn
        guide = self.font.render("← → để chọn, ENTER để xác nhận, ESC để quay lại", True, (200, 200, 200))
        screen.blit(guide, (self.screen_width//2 - guide.get_width()//2, self.screen_height - 60))