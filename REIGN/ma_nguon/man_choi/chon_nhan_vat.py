import pygame
import os
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.core import profile_manager

class CharacterSelectScene:
    def __init__(self, game):
        self.game = game
        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()
        self.font_big = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 60)
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)

        # Each character has an id and price (price=0 means free)
        self.characters = [
            {
                "id": "chien_binh",
                "name": "Chiến binh",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_binh",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/chien_binh/dung_yen/0.png"),
                "stats": {"hp": 500, "speed": 5, "damage": 30, "defense": 2},
                "color": (0, 255, 0),
                "price": 0
            },
            {
                "id": "ninja",
                "name": "Ninja",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/ninja",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/ninja/dung_yen/0.png"),
                "stats": {"hp": 350, "speed": 8, "damage": 25, "defense": 1},
                "color": (0, 0, 255),
                "price": 300
            },
            {
                "id": "vo_si",
                "name": "Võ sĩ",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/vo_si",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/vo_si/dung_yen/0.png"),
                "stats": {"hp": 1000, "speed": 4, "damage": 100, "defense": 3},
                "color": (255, 0, 0),
                "price": 400
            },
            {
                "id": "chien_than_lac_hong",
                "name": "Chiến Thần Lạc Hồng",
                "folder": "tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong",
                "preview": self._load_preview("tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong/dung_yen/0.png"),
                "stats": {"hp": 2000, "speed": 6, "damage": 200, "defense": 4},
                "color": (255, 0, 127),
                "price": 500
            }
        ]
        self.selected_idx = 0
        self.confirm = False
        self.preview_scale = 0.5  # Tỉ lệ phóng to ảnh preview
        self.message = ''
        self.msg_timer = 0
        
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
                # On ENTER: only select if owned; otherwise instruct to go to Shop
                cur = self.characters[self.selected_idx]
                cid = cur.get('id')
                user = getattr(self.game, 'current_user', None)
                owned = False
                if user:
                    profile = profile_manager.load_profile(user)
                    owned = cid in profile.get('purchased_characters', [])
                else:
                    owned = (cur.get('price', 0) == 0)

                if owned:
                    self.confirm = True
                    self._create_player()
                else:
                    # show hint and require shop purchase
                    self._set_message('Nhân vật bị khoá. Vào cửa hàng (nhấn S) để mua.', 180)
            elif event.key == pygame.K_s:
                # Open shop to purchase characters
                self.game.change_scene('shop')
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
    
    def _create_player(self):
        selected = self.characters[self.selected_idx]
        # Không truyền controls để Character tự lấy từ settings
        
        # Tạo nhân vật với thuộc tính phù hợp
        player = Character(100, 300, selected["folder"], color=selected["color"])
        
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
        if self.msg_timer > 0:
            self.msg_timer -= 1
            if self.msg_timer == 0:
                self.message = ''

    def _set_message(self, text: str, frames: int = 120):
        self.message = text
        self.msg_timer = frames
    
    def draw(self, screen):
        # Vẽ nền
        screen.fill((30, 30, 60))
        
        # Tiêu đề
        title = self.font_big.render("CHỌN NHÂN VẬT", True, (255, 255, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Vẽ các nhân vật (4 nhân vật cạnh nhau)
        num_characters = len(self.characters)
        spacing = self.screen_width // (num_characters + 1)
        
        for i, char in enumerate(self.characters):
            # Vị trí mỗi nhân vật
            pos_x = spacing * (i + 1)
            pos_y = self.screen_height // 2 - 80
            
            # Vẽ khung nhân vật với hiệu ứng đặc biệt cho nhân vật được chọn
            if i == self.selected_idx:
                frame_color = (255, 215, 0)  # Vàng gold cho nhân vật được chọn
                # Vẽ hiệu ứng glow
                glow_rect = pygame.Rect(pos_x - 105, pos_y - 25, 210, 280)
                pygame.draw.rect(screen, (255, 255, 0, 50), glow_rect, 6)
            else:
                frame_color = (100, 100, 100)
            
            # Khung chính
            main_rect = pygame.Rect(pos_x - 100, pos_y - 20, 200, 260)
            pygame.draw.rect(screen, frame_color, main_rect, 3)
            
            # Vẽ tên nhân vật với màu đặc biệt
            name_color = (255, 255, 0) if i == self.selected_idx else (255, 255, 255)
            name = self.font_small.render(char["name"], True, name_color)
            screen.blit(name, (pos_x - name.get_width()//2, pos_y - 50))
            
            # Vẽ ảnh preview
            preview = char["preview"]
            # Điều chỉnh kích thước preview cho phù hợp với 4 nhân vật
            preview_scale = 0.4  # Nhỏ hơn một chút để vừa 4 nhân vật
            preview = pygame.transform.scale(preview, 
                                          (int(preview.get_width() * preview_scale), 
                                           int(preview.get_height() * preview_scale)))
            preview_pos = (pos_x - preview.get_width()//2, pos_y - 10)
            screen.blit(preview, preview_pos)
            
            # Vẽ thông số với font nhỏ hơn
            stats_y = pos_y + 120
            stats = char["stats"]
            font_stats = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 20)
            
            hp_text = font_stats.render(f"HP: {stats['hp']}", True, (255, 100, 100))
            screen.blit(hp_text, (pos_x - 85, stats_y))
            
            speed_text = font_stats.render(f"Tốc độ: {stats['speed']}", True, (100, 255, 100))
            screen.blit(speed_text, (pos_x - 85, stats_y + 25))
            
            dmg_text = font_stats.render(f"ST: {stats['damage']}", True, (255, 255, 100))
            screen.blit(dmg_text, (pos_x - 85, stats_y + 50))
            
            def_text = font_stats.render(f"PT: {stats['defense']}", True, (100, 100, 255))
            screen.blit(def_text, (pos_x - 85, stats_y + 75))
            
            # Thêm chỉ báo đặc biệt cho Chiến Thần Lạc Hồng
            if char["name"] == "Chiến Thần Lạc Hồng":
                special_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 18).render("★ HUYỀN THOẠI ★", True, (255, 0, 127))
                screen.blit(special_text, (pos_x - special_text.get_width()//2, stats_y + 100))

            # Determine ownership and dim if locked
            cid = char.get('id') if 'id' in char else None
            user = getattr(self.game, 'current_user', None)
            owned = False
            if cid:
                if user:
                    profile = profile_manager.load_profile(user)
                    owned = cid in profile.get('purchased_characters', [])
                else:
                    owned = (char.get('price', 0) == 0)

            if not owned:
                # darken the entire character card to indicate locked
                overlay = pygame.Surface((200, 260), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (pos_x - 100, pos_y - 20))
                # muted text for stats
                mute_color = (140, 140, 140)
                name = self.font_small.render(char["name"], True, mute_color)
                screen.blit(name, (pos_x - name.get_width()//2, pos_y - 50))
                hp_text = font_stats.render(f"HP: {stats['hp']}", True, mute_color)
                screen.blit(hp_text, (pos_x - 85, stats_y))
                speed_text = font_stats.render(f"Tốc độ: {stats['speed']}", True, mute_color)
                screen.blit(speed_text, (pos_x - 85, stats_y + 25))
                dmg_text = font_stats.render(f"ST: {stats['damage']}", True, mute_color)
                screen.blit(dmg_text, (pos_x - 85, stats_y + 50))
                def_text = font_stats.render(f"PT: {stats['defense']}", True, mute_color)
                screen.blit(def_text, (pos_x - 85, stats_y + 75))
                # show buy hint
                hint = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18).render("Bị khoá — vào cửa hàng (S)", True, (200,200,200))
                screen.blit(hint, (pos_x - hint.get_width()//2, pos_y + 180))
        
        # Hướng dẫn
        guide = self.font_small.render("← → để chọn, ENTER để xác nhận, ESC để quay lại", True, (200, 200, 200))
        screen.blit(guide, (self.screen_width//2 - guide.get_width()//2, self.screen_height - 40))