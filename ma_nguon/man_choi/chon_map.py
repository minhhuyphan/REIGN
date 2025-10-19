import pygame
from ma_nguon.core import profile_manager

class ChonMapScene:
    """Màn hình chọn map"""
    
    def __init__(self, game):
        self.game = game
        self.screen_width = game.WIDTH
        self.screen_height = game.HEIGHT
        
        # Fonts
        try:
            self.font_big = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
            self.font_medium = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 28)
            self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 20)
        except:
            self.font_big = pygame.font.Font(None, 50)
            self.font_medium = pygame.font.Font(None, 28)
            self.font_small = pygame.font.Font(None, 20)
        
        # Danh sách maps
        self.maps = [
            {
                "id": "man1",
                "name": "Màn 1",
                "scene_name": "man1",
                "description": "Màn chơi cơ bản",
                "difficulty": "Dễ",
                "color": (100, 255, 100),
                "unlocked": True,
                "need_character_select": True  # Cần chọn nhân vật trước
            },
            {
                "id": "man2",
                "name": "Màn 2",
                "scene_name": "man2",
                "description": "Thử thách nâng cao",
                "difficulty": "Trung bình",
                "color": (255, 200, 100),
                "unlocked": True,
                "need_character_select": True
            },
            {
                "id": "mapmuathu",
                "name": "Map Mùa Thu",
                "scene_name": "chon_man_mua_thu",
                "description": "Khám phá mùa thu",
                "difficulty": "Trung bình",
                "color": (255, 180, 80),
                "unlocked": True,
                "need_character_select": True,  # Chọn nhân vật trước
                "multi_stage": True  # Có nhiều màn con
            },
            {
                "id": "mapninja",
                "name": "Map Ninja",
                "scene_name": "chon_man_ninja",
                "description": "Đường ninja hiểm trở",
                "difficulty": "Khó",
                "color": (200, 100, 255),
                "unlocked": True,
                "need_character_select": True,
                "multi_stage": True
            },
            {
                "id": "mapcongnghe",
                "name": "Map Công Nghệ",
                "scene_name": "map_cong_nghe",
                "description": "Thế giới tương lai",
                "difficulty": "Khó",
                "color": (100, 200, 255),
                "unlocked": True,
                "need_character_select": True
            },
            {
                "id": "maprunglinhvuc",
                "name": "Rừng Linh Vực",
                "scene_name": "maprunglinhvuc",
                "description": "Rừng bí ẩn nguy hiểm",
                "difficulty": "Rất khó",
                "color": (150, 255, 150),
                "unlocked": True,
                "need_character_select": True
            }
        ]
        
        self.selected_idx = 0
        self.scroll_offset = 0
        self.target_scroll = 0
        
        # Animation
        self.hover_animation = {}
        for i in range(len(self.maps)):
            self.hover_animation[i] = 0.0
        
        # Colors
        self.bg_gradient_top = (20, 20, 50)
        self.bg_gradient_bottom = (10, 10, 30)
        self.accent_color = (100, 200, 255)
        
        # Pre-render gradient background for performance
        self.background = self._create_gradient_background()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quay về menu
                self.game.change_scene("menu")
                
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_idx = (self.selected_idx - 1) % len(self.maps)
                self._update_scroll()
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_idx = (self.selected_idx + 1) % len(self.maps)
                self._update_scroll()
                
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_map()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicked on a map card
                mouse_pos = event.pos
                card_idx = self._get_card_at_pos(mouse_pos)
                if card_idx is not None:
                    if card_idx == self.selected_idx:
                        # Double click effect - select map
                        self._select_map()
                    else:
                        self.selected_idx = card_idx
                        self._update_scroll()
        
        elif event.type == pygame.MOUSEMOTION:
            # Update hover animation
            mouse_pos = event.pos
            for i in range(len(self.maps)):
                card_rect = self._get_card_rect(i)
                if card_rect and card_rect.collidepoint(mouse_pos):
                    self.hover_animation[i] = min(1.0, self.hover_animation[i] + 0.1)
                else:
                    self.hover_animation[i] = max(0.0, self.hover_animation[i] - 0.1)
    
    def _get_card_at_pos(self, pos):
        """Lấy index của card tại vị trí chuột"""
        for i in range(len(self.maps)):
            card_rect = self._get_card_rect(i)
            if card_rect and card_rect.collidepoint(pos):
                return i
        return None
    
    def _get_card_rect(self, idx):
        """Tính toán rect của card"""
        card_width = 280
        card_height = 350
        gap = 30
        
        total_width = len(self.maps) * card_width + (len(self.maps) - 1) * gap
        start_x = (self.screen_width - total_width) // 2 if total_width < self.screen_width else 50
        
        x = start_x + idx * (card_width + gap) - int(self.scroll_offset)
        y = (self.screen_height - card_height) // 2
        
        return pygame.Rect(x, y, card_width, card_height)
    
    def _update_scroll(self):
        """Cập nhật scroll để card đã chọn hiển thị"""
        card_width = 280
        gap = 30
        target_x = self.selected_idx * (card_width + gap)
        self.target_scroll = max(0, target_x - self.screen_width // 2 + card_width // 2)
    
    def _select_map(self):
        """Chọn map và chuyển sang màn chọn nhân vật"""
        selected_map = self.maps[self.selected_idx]
        
        if not selected_map["unlocked"]:
            print(f"Map {selected_map['name']} chưa được mở khóa!")
            return
        
        # Lưu map đã chọn vào game
        self.game.target_level = selected_map["scene_name"]
        
        # Lưu thông tin nếu map có nhiều màn con
        if selected_map.get("multi_stage", False):
            self.game.multi_stage_map = True
            self.game.stage_selector_scene = selected_map["scene_name"]
        else:
            self.game.multi_stage_map = False
        
        # Nếu map cần chọn nhân vật, chuyển sang màn chọn nhân vật
        if selected_map.get("need_character_select", True):
            self.game.change_scene("chon_nhan_vat")
        else:
            # Nếu không cần chọn nhân vật, đi thẳng vào map
            self.game.change_scene(selected_map["scene_name"])
    
    def _create_gradient_background(self):
        """Tạo gradient background một lần để tối ưu performance"""
        bg_surface = pygame.Surface((self.screen_width, self.screen_height))
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = (
                int(self.bg_gradient_top[0] * (1 - ratio) + self.bg_gradient_bottom[0] * ratio),
                int(self.bg_gradient_top[1] * (1 - ratio) + self.bg_gradient_bottom[1] * ratio),
                int(self.bg_gradient_top[2] * (1 - ratio) + self.bg_gradient_bottom[2] * ratio)
            )
            pygame.draw.line(bg_surface, color, (0, y), (self.screen_width, y))
        return bg_surface
    
    def update(self):
        # Smooth scroll
        if abs(self.scroll_offset - self.target_scroll) > 1:
            self.scroll_offset += (self.target_scroll - self.scroll_offset) * 0.15
        else:
            self.scroll_offset = self.target_scroll
        
        # Update hover animations
        for i in range(len(self.maps)):
            if i != self.selected_idx:
                if self.hover_animation[i] > 0:
                    self.hover_animation[i] = max(0.0, self.hover_animation[i] - 0.05)
    
    def draw(self, screen):
        # Vẽ gradient background (cached)
        screen.blit(self.background, (0, 0))
        
        # Tiêu đề
        title = self.font_big.render("CHỌN BẢN ĐỒ", True, (255, 215, 0))
        title_shadow = self.font_big.render("CHỌN BẢN ĐỒ", True, (50, 50, 50))
        screen.blit(title_shadow, (self.screen_width//2 - title.get_width()//2 + 3, 33))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Vẽ các map cards
        card_width = 280
        card_height = 350
        gap = 30
        
        for i, map_data in enumerate(self.maps):
            card_rect = self._get_card_rect(i)
            
            # Skip if card is off screen
            if card_rect.right < 0 or card_rect.left > self.screen_width:
                continue
            
            # Animation scale
            is_selected = (i == self.selected_idx)
            hover = self.hover_animation[i]
            
            if is_selected:
                scale = 1.05
                glow_alpha = 100
            else:
                scale = 1.0 + hover * 0.03
                glow_alpha = int(50 * hover)
            
            # Calculate scaled rect
            scaled_width = int(card_width * scale)
            scaled_height = int(card_height * scale)
            scaled_rect = pygame.Rect(
                card_rect.centerx - scaled_width // 2,
                card_rect.centery - scaled_height // 2,
                scaled_width,
                scaled_height
            )
            
            # Glow effect
            if is_selected or hover > 0:
                glow_surf = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.accent_color, glow_alpha), glow_surf.get_rect(), border_radius=15)
                screen.blit(glow_surf, (scaled_rect.x - 10, scaled_rect.y - 10))
            
            # Card background
            card_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
            pygame.draw.rect(card_surf, (30, 30, 50, 220), card_surf.get_rect(), border_radius=12)
            
            # Border
            border_color = (255, 215, 0) if is_selected else (100, 100, 120)
            pygame.draw.rect(card_surf, border_color, card_surf.get_rect(), 3, border_radius=12)
            
            screen.blit(card_surf, scaled_rect)
            
            # Map name
            name_surf = self.font_medium.render(map_data["name"], True, (255, 255, 255))
            name_x = scaled_rect.centerx - name_surf.get_width() // 2
            name_y = scaled_rect.top + 20
            screen.blit(name_surf, (name_x, name_y))
            
            # Difficulty
            diff_color = map_data["color"]
            diff_surf = self.font_small.render(f"Độ khó: {map_data['difficulty']}", True, diff_color)
            diff_x = scaled_rect.centerx - diff_surf.get_width() // 2
            diff_y = name_y + 40
            screen.blit(diff_surf, (diff_x, diff_y))
            
            # Description
            desc_lines = self._wrap_text(map_data["description"], self.font_small, scaled_width - 40)
            desc_y = diff_y + 50
            for line in desc_lines:
                line_surf = self.font_small.render(line, True, (200, 200, 200))
                line_x = scaled_rect.centerx - line_surf.get_width() // 2
                screen.blit(line_surf, (line_x, desc_y))
                desc_y += 25
            
            # Lock/Unlock indicator
            if map_data["unlocked"]:
                status_surf = self.font_small.render("✓ Đã mở khóa", True, (100, 255, 100))
            else:
                status_surf = self.font_small.render("🔒 Chưa mở khóa", True, (255, 100, 100))
            
            status_x = scaled_rect.centerx - status_surf.get_width() // 2
            status_y = scaled_rect.bottom - 60
            screen.blit(status_surf, (status_x, status_y))
            
            # Press ENTER hint for selected
            if is_selected:
                hint_surf = self.font_small.render("ENTER để chọn", True, (255, 215, 0))
                hint_x = scaled_rect.centerx - hint_surf.get_width() // 2
                hint_y = scaled_rect.bottom - 30
                screen.blit(hint_surf, (hint_x, hint_y))
        
        # Hướng dẫn
        guide = self.font_small.render("← → để chọn map | ENTER để xác nhận | ESC để quay lại", True, (200, 200, 200))
        screen.blit(guide, (self.screen_width//2 - guide.get_width()//2, self.screen_height - 40))
    
    def _wrap_text(self, text, font, max_width):
        """Chia text thành nhiều dòng"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
