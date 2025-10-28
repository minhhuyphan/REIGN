import pygame
import random
import math
import os
from ma_nguon.core import profile_manager
from ma_nguon.doi_tuong.items import EQUIPMENT_DATA


class GachaTrangBiScene:
    """Màn hình quay gacha trang bị"""
    
    def __init__(self, game):
        self.game = game
        self.screen_width = game.WIDTH
        self.screen_height = game.HEIGHT
        
        # Fonts
        try:
            self.font_big = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 60)
            self.font_medium = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 32)
            self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
        except:
            self.font_big = pygame.font.Font(None, 60)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
        
        # Gacha settings
        self.gacha_cost = 100  # Giá 1 lượt quay
        self.gacha_cost_10 = 900  # Giá 10 lượt quay (giảm 10%)
        
        # Animation state
        self.spinning = False
        self.spin_timer = 0
        self.spin_duration = 180  # 3 giây
        self.result_items = []
        self.show_result = False
        self.result_timer = 0
        
        # Rarity colors
        self.rarity_colors = {
            "common": (200, 200, 200),      # Xám
            "rare": (100, 200, 255),         # Xanh dương
            "epic": (200, 100, 255),         # Tím
            "legendary": (255, 215, 0),      # Vàng
            "mythic": (255, 140, 0)          # Cam - Hiếm hơn Legendary
        }
        
        # Spin animation
        self.spin_angle = 0
        self.particles = []
        
        # Pre-render gradient background for performance
        self.background = self._create_gradient_background()
        
    def _get_gacha_pool(self):
        """Tạo pool trang bị + nhân vật cho gacha với tỷ lệ rarity"""
        pool = []
        
        # Kiểm tra nhân vật đã có chưa
        user = getattr(self.game, 'current_user', None)
        purchased_characters = []
        if user:
            profile = profile_manager.load_profile(user)
            purchased_characters = profile.get('purchased_characters', [])
        
        # Thêm nhân vật Vân Đao và Mị Ảnh với tỷ lệ 0.5% mỗi nhân vật (hiếm hơn vàng)
        # CHỈ thêm vào pool nếu chưa có
        if "van_dao" not in purchased_characters:
            pool.append("CHARACTER:van_dao")  # Chỉ 1 lần = 0.5% trong pool 200 items
        
        if "mi_anh" not in purchased_characters:
            pool.append("CHARACTER:mi_anh")  # Chỉ 1 lần = 0.5% trong pool 200 items
        
        # Tạo pool trang bị với tỷ lệ (tổng ~200 items):
        # Common: 60%
        # Rare: 30%
        # Epic: 8%
        # Legendary: 2%
        
        for item_id, item_data in EQUIPMENT_DATA.items():
            rarity = item_data.get("rarity", "common")
            
            if rarity == "common":
                weight = 60
            elif rarity == "rare":
                weight = 30
            elif rarity == "epic":
                weight = 8
            else:  # legendary
                weight = 2
            
            # Thêm item vào pool theo weight
            for _ in range(weight):
                pool.append(item_id)
        
        return pool
    
    def _roll_gacha(self, count=1):
        """Quay gacha và trả về kết quả"""
        pool = self._get_gacha_pool()
        results = []
        
        for _ in range(count):
            item_id = random.choice(pool)
            results.append(item_id)
        
        return results
    
    def _start_spin(self, count=1):
        """Bắt đầu quay"""
        user = getattr(self.game, 'current_user', None)
        if not user:
            self.message = "Vui lòng đăng nhập!"
            return
        
        # Check gold
        profile = profile_manager.load_profile(user)
        gold = profile.get('gold', 0)
        
        cost = self.gacha_cost if count == 1 else self.gacha_cost_10
        
        if gold < cost:
            self.message = f"Không đủ vàng! Cần {cost} vàng"
            return
        
        # Deduct gold
        profile['gold'] = gold - cost
        profile_manager.save_profile(user, profile)
        self.game.profile = profile
        
        # Start spinning animation
        self.spinning = True
        self.spin_timer = self.spin_duration
        self.result_items = self._roll_gacha(count)
        self.show_result = False
        self.particles = []
        self.message = ""
    
    def _add_items_to_inventory(self):
        """Thêm trang bị và nhân vật vào kho của người chơi"""
        user = getattr(self.game, 'current_user', None)
        if not user:
            return
        
        profile = profile_manager.load_profile(user)
        
        # Lấy inventory hiện tại - dạng dict với {item_id: count}
        inventory = profile.get('equipment_inventory', {})
        
        # Nếu inventory là list cũ, convert sang dict
        if isinstance(inventory, list):
            new_inventory = {}
            for item in inventory:
                new_inventory[item] = new_inventory.get(item, 0) + 1
            inventory = new_inventory
        
        # Lấy danh sách nhân vật đã mua
        purchased_characters = profile.get('purchased_characters', [])
        
        # Add result items to inventory (có thể trùng lặp)
        for item_id in self.result_items:
            # Kiểm tra nếu là nhân vật
            if item_id.startswith("CHARACTER:"):
                char_id = item_id.replace("CHARACTER:", "")
                if char_id not in purchased_characters:
                    purchased_characters.append(char_id)
                    print(f"[GACHA] Mở khóa nhân vật mới: {char_id}")
            else:
                # Là trang bị
                inventory[item_id] = inventory.get(item_id, 0) + 1
        
        profile['equipment_inventory'] = inventory
        profile['purchased_characters'] = purchased_characters
        profile_manager.save_profile(user, profile)
        self.game.profile = profile
        
        print(f"[GACHA] Added {len(self.result_items)} items to inventory: {self.result_items}")
        print(f"[GACHA] Current inventory: {inventory}")
        print(f"[GACHA] Purchased characters: {purchased_characters}")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.show_result:
                    # Close result and go back to menu
                    self.show_result = False
                elif not self.spinning:
                    # Go back to shop
                    self.game.change_scene("shop")
            
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.show_result:
                    # Close result and back to gacha menu
                    self.show_result = False
                elif not self.spinning:
                    # Start spin (1 roll)
                    self._start_spin(1)
            
            elif event.key == pygame.K_1:
                if not self.spinning and not self.show_result:
                    self._start_spin(1)
            
            elif event.key == pygame.K_0:
                if not self.spinning and not self.show_result:
                    self._start_spin(10)
            
            elif event.key == pygame.K_n:
                # N = Next roll (quay tiếp 1 lần)
                if self.show_result:
                    self.show_result = False
                    self._start_spin(1)
            
            elif event.key == pygame.K_m:
                # M = Multiple rolls (quay tiếp 10 lần)
                if self.show_result:
                    self.show_result = False
                    self._start_spin(10)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                
                # Check buttons in main menu
                if hasattr(self, 'btn_1_rect') and self.btn_1_rect.collidepoint(mouse_pos):
                    if not self.spinning and not self.show_result:
                        self._start_spin(1)
                
                elif hasattr(self, 'btn_10_rect') and self.btn_10_rect.collidepoint(mouse_pos):
                    if not self.spinning and not self.show_result:
                        self._start_spin(10)
                
                elif hasattr(self, 'btn_back_rect') and self.btn_back_rect.collidepoint(mouse_pos):
                    if not self.spinning:
                        self.game.change_scene("shop")
                
                # Check buttons in result screen
                if self.show_result:
                    if hasattr(self, 'btn_roll_again_rect') and self.btn_roll_again_rect.collidepoint(mouse_pos):
                        # Quay tiếp 1 lần
                        self.show_result = False
                        self._start_spin(1)
                    
                    elif hasattr(self, 'btn_roll_10_again_rect') and self.btn_roll_10_again_rect.collidepoint(mouse_pos):
                        # Quay tiếp 10 lần
                        self.show_result = False
                        self._start_spin(10)
                    
                    elif hasattr(self, 'btn_back_menu_rect') and self.btn_back_menu_rect.collidepoint(mouse_pos):
                        # Quay về menu gacha
                        self.show_result = False
    
    def _create_gradient_background(self):
        """Tạo gradient background một lần để tối ưu performance"""
        bg_surface = pygame.Surface((self.screen_width, self.screen_height))
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            color = (
                int(20 * (1 - ratio) + 40 * ratio),
                int(10 * (1 - ratio) + 20 * ratio),
                int(50 * (1 - ratio) + 80 * ratio)
            )
            pygame.draw.line(bg_surface, color, (0, y), (self.screen_width, y))
        return bg_surface
    
    def update(self):
        # Spinning animation
        if self.spinning:
            self.spin_timer -= 1
            self.spin_angle += 15
            
            # Create particles
            if random.random() < 0.3:
                particle = {
                    'x': random.randint(100, self.screen_width - 100),
                    'y': random.randint(100, self.screen_height - 100),
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(-2, 2),
                    'life': 60,
                    'color': random.choice(list(self.rarity_colors.values()))
                }
                self.particles.append(particle)
            
            # Update particles
            for p in self.particles[:]:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= 1
                if p['life'] <= 0:
                    self.particles.remove(p)
            
            # End spinning
            if self.spin_timer <= 0:
                self.spinning = False
                self.show_result = True
                self.result_timer = 300  # Show for 5 seconds
                self._add_items_to_inventory()
        
        # Result timer
        if self.show_result:
            self.result_timer -= 1
    
    def draw(self, screen):
        # Background gradient (cached)
        screen.blit(self.background, (0, 0))
        
        if self.show_result:
            self._draw_result(screen)
        elif self.spinning:
            self._draw_spinning(screen)
        else:
            self._draw_menu(screen)
    
    def _draw_menu(self, screen):
        """Vẽ menu chính"""
        # Title
        title = self.font_big.render("VÒNG QUAY", True, (255, 215, 0))
        title_shadow = self.font_big.render("VÒNG QUAY", True, (50, 50, 50))
        screen.blit(title_shadow, (self.screen_width//2 - title.get_width()//2 + 3, 33))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Gold display
        user = getattr(self.game, 'current_user', None)
        gold = 0
        if user:
            profile = profile_manager.load_profile(user)
            gold = profile.get('gold', 0)
        
        gold_text = self.font_medium.render(f"Vàng: {gold}", True, (255, 255, 0))
        screen.blit(gold_text, (self.screen_width - gold_text.get_width() - 40, 30))
        
        # Gacha box visual
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2 - 50
        
        # Chest/box
        box_size = 200
        box_rect = pygame.Rect(center_x - box_size//2, center_y - box_size//2, box_size, box_size)
        
        # Glow effect
        for i in range(5):
            alpha = 50 - i * 10
            offset = i * 5
            glow_rect = box_rect.inflate(offset * 2, offset * 2)
            glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (255, 215, 0, alpha), glow_surf.get_rect(), border_radius=20)
            screen.blit(glow_surf, glow_rect.topleft)
        
        # Main box
        pygame.draw.rect(screen, (100, 80, 50), box_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), box_rect, 5, border_radius=15)
        
        # Question mark
        question = self.font_big.render("?", True, (255, 215, 0))
        screen.blit(question, (center_x - question.get_width()//2, center_y - question.get_height()//2))
        
        # Buttons
        btn_width = 200
        btn_height = 60
        btn_y = center_y + 150
        
        # Button 1 roll
        self.btn_1_rect = pygame.Rect(center_x - btn_width - 20, btn_y, btn_width, btn_height)
        pygame.draw.rect(screen, (60, 60, 100), self.btn_1_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 200, 255), self.btn_1_rect, 3, border_radius=10)
        
        btn1_text = self.font_medium.render(f"1 lượt: {self.gacha_cost}G", True, (255, 255, 255))
        screen.blit(btn1_text, (self.btn_1_rect.centerx - btn1_text.get_width()//2, 
                                 self.btn_1_rect.centery - btn1_text.get_height()//2))
        
        # Button 10 rolls
        self.btn_10_rect = pygame.Rect(center_x + 20, btn_y, btn_width, btn_height)
        pygame.draw.rect(screen, (60, 60, 100), self.btn_10_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 100, 255), self.btn_10_rect, 3, border_radius=10)
        
        btn10_text = self.font_medium.render(f"10 lượt: {self.gacha_cost_10}G", True, (255, 255, 255))
        screen.blit(btn10_text, (self.btn_10_rect.centerx - btn10_text.get_width()//2,
                                  self.btn_10_rect.centery - btn10_text.get_height()//2))
        
        # Back button
        self.btn_back_rect = pygame.Rect(40, self.screen_height - 80, 150, 50)
        pygame.draw.rect(screen, (60, 60, 60), self.btn_back_rect, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), self.btn_back_rect, 2, border_radius=8)
        
        back_text = self.font_small.render("Quay lại (ESC)", True, (255, 255, 255))
        screen.blit(back_text, (self.btn_back_rect.centerx - back_text.get_width()//2,
                                self.btn_back_rect.centery - back_text.get_height()//2))
        
        # Instructions
        inst_text = self.font_small.render("Nhấn 1 hoặc 0 để quay nhanh", True, (200, 200, 200))
        screen.blit(inst_text, (self.screen_width//2 - inst_text.get_width()//2, self.screen_height - 40))
        
        # Message
        if hasattr(self, 'message') and self.message:
            msg_surf = self.font_small.render(self.message, True, (255, 100, 100))
            screen.blit(msg_surf, (self.screen_width//2 - msg_surf.get_width()//2, btn_y - 50))
    
    def _draw_spinning(self, screen):
        """Vẽ animation đang quay"""
        # Title
        title = self.font_big.render("ĐANG QUAY...", True, (255, 215, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 50))
        
        # Draw particles
        for p in self.particles:
            alpha = int(255 * (p['life'] / 60))
            color = (*p['color'], alpha)
            particle_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, color, (4, 4), 4)
            screen.blit(particle_surf, (int(p['x']), int(p['y'])))
        
        # Spinning circle
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Rotating glow
        for i in range(8):
            angle = self.spin_angle + i * 45
            rad = math.radians(angle)
            dist = 150
            x = center_x + math.cos(rad) * dist
            y = center_y + math.sin(rad) * dist
            
            pygame.draw.circle(screen, (255, 215, 0, 150), (int(x), int(y)), 20)
        
        # Center orb
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 60)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 50)
        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), 40)
        
        # Progress
        progress = 1 - (self.spin_timer / self.spin_duration)
        progress_text = self.font_medium.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        screen.blit(progress_text, (center_x - progress_text.get_width()//2, 
                                    center_y - progress_text.get_height()//2))
    
    def _draw_result(self, screen):
        """Vẽ kết quả gacha"""
        # Title
        title = self.font_big.render("KẾT QUẢ", True, (255, 215, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Draw items
        num_items = len(self.result_items)
        items_per_row = min(5, num_items)
        rows = (num_items + items_per_row - 1) // items_per_row
        
        card_width = 150
        card_height = 220
        gap = 20
        
        start_y = 130
        
        for idx, item_id in enumerate(self.result_items):
            row = idx // items_per_row
            col = idx % items_per_row
            
            # Center items in row
            row_items = min(items_per_row, num_items - row * items_per_row)
            total_width = row_items * card_width + (row_items - 1) * gap
            start_x = (self.screen_width - total_width) // 2
            
            x = start_x + col * (card_width + gap)
            y = start_y + row * (card_height + gap)
            
            # Kiểm tra nếu là nhân vật
            is_character = item_id.startswith("CHARACTER:")
            
            if is_character:
                # Xử lý nhân vật
                char_id = item_id.replace("CHARACTER:", "")
                character_names = {
                    "van_dao": "Vân Đao",
                    "mi_anh": "Mị Ảnh"
                }
                name = character_names.get(char_id, char_id)
                rarity = "mythic"  # Nhân vật là Mythic (cam) - hiếm hơn Legendary
                rarity_color = self.rarity_colors.get(rarity, (255, 140, 0))
            else:
                # Get item data (trang bị)
                item_data = EQUIPMENT_DATA.get(item_id, {})
                rarity = item_data.get("rarity", "common")
                name = item_data.get("name", item_id)
                image_path = item_data.get("image_path", "")
                equip_type = item_data.get("type", "")
                rarity_color = self.rarity_colors.get(rarity, (200, 200, 200))
            
            # Card background
            card_rect = pygame.Rect(x, y, card_width, card_height)
            
            # Rarity glow
            for i in range(3):
                offset = i * 3
                glow_rect = card_rect.inflate(offset * 2, offset * 2)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                alpha = 100 - i * 30
                pygame.draw.rect(glow_surf, (*rarity_color, alpha), glow_surf.get_rect(), border_radius=12)
                screen.blit(glow_surf, glow_rect.topleft)
            
            # Main card
            pygame.draw.rect(screen, (40, 40, 60), card_rect, border_radius=10)
            pygame.draw.rect(screen, rarity_color, card_rect, 3, border_radius=10)
            
            # Draw image
            if is_character:
                # Vẽ ảnh nhân vật
                char_id = item_id.replace("CHARACTER:", "")
                char_img_path = f"tai_nguyen/hinh_anh/nhan_vat/{char_id}/dung_yen/0.png"
                if os.path.exists(char_img_path):
                    try:
                        char_img = pygame.image.load(char_img_path).convert_alpha()
                        img_size = 80
                        char_img = pygame.transform.scale(char_img, (img_size, img_size))
                        img_x = x + (card_width - img_size) // 2
                        img_y = y + 30
                        screen.blit(char_img, (img_x, img_y))
                    except Exception:
                        pygame.draw.circle(screen, rarity_color, (x + card_width//2, y + 70), 30)
                else:
                    pygame.draw.circle(screen, rarity_color, (x + card_width//2, y + 70), 30)
            elif image_path:
                # Draw equipment image
                # Build full path
                full_path = os.path.join("tai_nguyen", "hinh_anh", "trang_bi", image_path)
                if not os.path.exists(full_path):
                    # Try uppercase variant
                    full_path = os.path.join("Tai_nguyen", "hinh_anh", "trang_bi", image_path)
                
                if os.path.exists(full_path):
                    try:
                        equip_img = pygame.image.load(full_path).convert_alpha()
                        # Scale image to fit card
                        img_size = 80
                        equip_img = pygame.transform.scale(equip_img, (img_size, img_size))
                        img_x = x + (card_width - img_size) // 2
                        img_y = y + 30
                        screen.blit(equip_img, (img_x, img_y))
                        print(f"[GACHA] Loaded image: {full_path}")
                    except Exception as e:
                        print(f"[GACHA] Failed to load image {full_path}: {e}")
                        # If image fails, draw placeholder
                        pygame.draw.circle(screen, rarity_color, (x + card_width//2, y + 70), 30)
                else:
                    print(f"[GACHA] Image not found: {full_path}")
                    # Placeholder icon
                    pygame.draw.circle(screen, rarity_color, (x + card_width//2, y + 70), 30)
            else:
                # Placeholder icon
                pygame.draw.circle(screen, rarity_color, (x + card_width//2, y + 70), 30)
            
            # Item name (wrapped)
            name_lines = self._wrap_text(name, self.font_small, card_width - 20)
            name_y = y + 125
            for line in name_lines:
                line_surf = self.font_small.render(line, True, rarity_color)
                screen.blit(line_surf, (x + card_width//2 - line_surf.get_width()//2, name_y))
                name_y += 22
            
            # Stats (chỉ hiển thị cho trang bị, không cho nhân vật)
            if not is_character:
                stats_y = y + card_height - 50
                stats_font = pygame.font.Font(None, 18)
                
                attack_bonus = item_data.get("attack_bonus", 0)
                hp_bonus = item_data.get("hp_bonus", 0)
                speed_bonus = item_data.get("speed_bonus", 0)
                
                if attack_bonus > 0:
                    stat_text = stats_font.render(f"+{attack_bonus} ATK", True, (255, 200, 100))
                    screen.blit(stat_text, (x + 10, stats_y))
                elif hp_bonus > 0:
                    stat_text = stats_font.render(f"+{hp_bonus} HP", True, (100, 255, 100))
                    screen.blit(stat_text, (x + 10, stats_y))
                elif speed_bonus > 0:
                    stat_text = stats_font.render(f"+{speed_bonus} SPD", True, (100, 200, 255))
                    screen.blit(stat_text, (x + 10, stats_y))
            else:
                # Hiển thị label "NHÂN VẬT" cho character
                char_label = self.font_small.render("NHÂN VẬT", True, rarity_color)
                screen.blit(char_label, (x + card_width//2 - char_label.get_width()//2, y + card_height - 50))
            
            # Rarity badge
            rarity_text = self.font_small.render(rarity.upper(), True, rarity_color)
            screen.blit(rarity_text, (x + card_width//2 - rarity_text.get_width()//2, y + 10))
        
        # Buttons at bottom
        btn_width = 200
        btn_height = 60
        btn_gap = 20
        btn_y = self.screen_height - 120
        
        # Calculate center position for 3 buttons
        total_width = btn_width * 3 + btn_gap * 2
        start_x = (self.screen_width - total_width) // 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Button "Quay tiếp 1" (Roll Again x1)
        self.btn_roll_again_rect = pygame.Rect(start_x, btn_y, btn_width, btn_height)
        hover_color_1 = (80, 100, 150) if self.btn_roll_again_rect.collidepoint(mouse_pos) else (60, 80, 130)
        
        pygame.draw.rect(screen, hover_color_1, self.btn_roll_again_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 200, 255), self.btn_roll_again_rect, 3, border_radius=10)
        
        roll_text = self.font_medium.render("Quay x1 (N)", True, (255, 255, 255))
        screen.blit(roll_text, (self.btn_roll_again_rect.centerx - roll_text.get_width()//2,
                                self.btn_roll_again_rect.centery - roll_text.get_height()//2))
        
        # Button "Quay tiếp 10" (Roll Again x10)
        self.btn_roll_10_again_rect = pygame.Rect(start_x + btn_width + btn_gap, btn_y, btn_width, btn_height)
        hover_color_2 = (120, 80, 150) if self.btn_roll_10_again_rect.collidepoint(mouse_pos) else (100, 60, 130)
        
        pygame.draw.rect(screen, hover_color_2, self.btn_roll_10_again_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 100, 255), self.btn_roll_10_again_rect, 3, border_radius=10)
        
        roll10_text = self.font_medium.render("Quay x10 (M)", True, (255, 255, 255))
        screen.blit(roll10_text, (self.btn_roll_10_again_rect.centerx - roll10_text.get_width()//2,
                                  self.btn_roll_10_again_rect.centery - roll10_text.get_height()//2))
        
        # Button "Quay về" (Back to Menu)
        self.btn_back_menu_rect = pygame.Rect(start_x + (btn_width + btn_gap) * 2, btn_y, btn_width, btn_height)
        hover_color_3 = (100, 70, 70) if self.btn_back_menu_rect.collidepoint(mouse_pos) else (80, 50, 50)
        
        pygame.draw.rect(screen, hover_color_3, self.btn_back_menu_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 150, 150), self.btn_back_menu_rect, 3, border_radius=10)
        
        back_text = self.font_medium.render("Quay về (ESC)", True, (255, 255, 255))
        screen.blit(back_text, (self.btn_back_menu_rect.centerx - back_text.get_width()//2,
                               self.btn_back_menu_rect.centery - back_text.get_height()//2))
        
        # Instructions (moved up a bit)
        continue_text = self.font_small.render("N = Quay x1 | M = Quay x10 | SPACE/ESC = Quay về", True, (200, 200, 200))
        screen.blit(continue_text, (self.screen_width//2 - continue_text.get_width()//2, 
                                    self.screen_height - 50))
    
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
