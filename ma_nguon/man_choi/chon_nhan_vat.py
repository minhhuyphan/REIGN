import pygame
import os
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.core import profile_manager
from ma_nguon.doi_tuong.character_stats import CHARACTER_STATS

class CharacterSelectScene:
    def __init__(self, game):
        print("[CHON_NV] Khởi tạo màn chọn nhân vật...")
        self.game = game
        self.screen_width = self.game.screen.get_width()
        self.screen_height = self.game.screen.get_height()
        self.font_big = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 60)
        self.font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 50)
        self.font_small = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 30)

        # Build character list from shared stats
        self.characters = []
        for char_id, stats in CHARACTER_STATS.items():
            char_data = {
                "id": char_id,
                "name": stats["name"],
                "folder": f"tai_nguyen/hinh_anh/nhan_vat/{char_id}",
                "preview": self._load_preview(f"tai_nguyen/hinh_anh/nhan_vat/{char_id}/dung_yen/0.png"),
                "stats": {
                    "hp": stats["hp"],
                    "speed": stats["speed"],
                    "damage": stats["damage"],
                    "defense": stats["defense"],
                    "kick_damage": stats.get("kick_damage", 20)
                },
                "color": stats["color"],
                "price": stats["price"]
            }
            self.characters.append(char_data)
        
        self.selected_idx = 0
        self.confirm = False
        self.preview_scale = 0.5  # Tỉ lệ phóng to ảnh preview
        self.message = ''
        self.msg_timer = 0
        # Scrolling support for wide character lists
        self.scroll_x = 0
        self.dragging = False
        self.drag_start_x = 0
        self.scroll_start = 0
        
        # Load equipment inventory ngay khi khởi tạo để hiển thị bonuses
        self._preload_equipment_inventory()
        
        # Animation và visual effects
        self.hover_offset = 0
        self.hover_direction = 1
        self.particle_timer = 0
        
    def _draw_gradient_background(self, screen):
        """Vẽ background gradient đẹp"""
        # Gradient từ tím đậm sang xanh dương
        for y in range(self.screen_height):
            progress = y / self.screen_height
            r = int(20 + (30 - 20) * progress)
            g = int(20 + (40 - 20) * progress)
            b = int(60 + (80 - 60) * progress)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))
    
    def _preload_equipment_inventory(self):
        """Load equipment inventory vào EquipmentManager để hiển thị bonuses"""
        try:
            if hasattr(self.game, 'current_user') and self.game.current_user:
                from ma_nguon.doi_tuong.equipment import get_equipment_manager
                
                profile = profile_manager.load_profile(self.game.current_user)
                inventory = profile.get('equipment_inventory', {})
                
                if inventory:
                    eq_manager = get_equipment_manager()
                    eq_manager.load_inventory_from_profile(inventory)
                    print(f"[CHON_NV] Preloaded {len(inventory)} equipment types for display")
        except Exception as e:
            print(f"[CHON_NV] Could not preload equipment: {e}")
        
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
                # ensure selected visible after move
                self._ensure_selected_visible()
            elif event.key == pygame.K_RIGHT:
                self.selected_idx = (self.selected_idx + 1) % len(self.characters)
                self._ensure_selected_visible()
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
                    self._set_message('khoá', 180)
            elif event.key == pygame.K_s:
                # Open shop to purchase characters
                self.game.change_scene('shop')
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
        # Mouse drag for horizontal scrolling
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # if clicked near the scrollbar area, start dragging scrollbar
            self.dragging = True
            self.drag_start_x = mx
            self.scroll_start = self.scroll_x
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, my = event.pos
            dx = mx - self.drag_start_x
            # invert: moving mouse right should decrease scroll_x
            self.scroll_x = max(0, self.scroll_start - dx)
    
    def _create_player(self):
        print("[CHON_NV] _create_player được gọi")
        selected = self.characters[self.selected_idx]
        # Không truyền controls để Character tự lấy từ settings
        
        # Tạo nhân vật với thuộc tính phù hợp - truyền stats vào constructor
        stats = {
            'hp': selected["stats"]["hp"],
            'damage': selected["stats"]["damage"],
            'speed': selected["stats"]["speed"],
            'defense': selected["stats"]["defense"],
            'kick_damage': selected["stats"].get("kick_damage", 20),
            'max_mana': selected["stats"].get("max_mana", 200),
            'mana_regen': selected["stats"].get("mana_regen", 5)
        }
        player = Character(100, 300, selected["folder"], color=selected["color"], stats=stats)
        
        print(f"\n{'='*60}")
        print(f"Tạo nhân vật: {selected['name']}")
        print(f"Base stats - HP: {player.hp}/{player.max_hp}, Damage: {player.damage}, Speed: {player.speed}")
        
        # Lưu character_id để track equipment
        player.character_id = selected["id"]
        
        # Load và áp dụng equipment từ profile
        if hasattr(self.game, 'current_user') and self.game.current_user:
            try:
                from ma_nguon.core import profile_manager
                from ma_nguon.doi_tuong.equipment import get_equipment_manager
                
                profile = profile_manager.load_profile(self.game.current_user)
                character_equipment = profile.get('character_equipment', {})
                char_id = selected["id"]
                
                # Load equipment manager
                eq_manager = get_equipment_manager()
                
                # Load inventory từ profile (QUAN TRỌNG: Phải load inventory trước)
                inventory = profile.get('equipment_inventory', {})
                if inventory:
                    eq_manager.load_inventory_from_profile(inventory)
                    print(f"[CHON_NV] Đã load {len(inventory)} loại trang bị vào inventory")
                
                if char_id in character_equipment:
                    # Load equipment data vào manager
                    eq_manager.load_character_equipment(char_id, character_equipment[char_id])
                    
                    print(f"Equipment cho {char_id}: {character_equipment[char_id]}")
                    
                    # Apply equipment to player
                    for slot_type, eq_name in character_equipment[char_id].items():
                        equipment = eq_manager.get_equipment_by_name(eq_name)
                        if equipment:
                            success = player.equip_item(equipment)
                            print(f"  Lắp {eq_name} vào {slot_type}: {success}")
                    
                    print(f"Sau khi lắp trang bị - HP: {player.hp}/{player.max_hp}, Damage: {player.damage}, Speed: {player.speed}")
                    print(f"{'='*60}\n")
                    print(f"✓ Đã áp dụng trang bị cho {selected['name']}")
                    
                    # Đánh dấu đã apply equipment để tránh apply lại trong map
                    player._equipment_applied = True
                else:
                    print(f"Không có trang bị cho {char_id}")
                    print(f"{'='*60}\n")
            except Exception as e:
                print(f"✗ Lỗi khi load trang bị cho nhân vật: {e}")
        
        # Lưu nhân vật đã chọn vào game
        self.game.selected_player = player
        
        # Kiểm tra xem có phải multi-stage map không
        if hasattr(self.game, 'multi_stage_map') and self.game.multi_stage_map:
            # Chuyển sang màn chọn màn con (ví dụ: chọn màn mùa thu)
            stage_selector = getattr(self.game, 'stage_selector_scene', self.game.target_level)
            self.game.change_scene(stage_selector)
        else:
            # Chuyển thẳng vào màn chơi
            self.game.change_scene(self.game.target_level)

    def _ensure_selected_visible(self):
        # recompute layout to determine where selected sits
        num_characters = len(self.characters)
        gap = 30
        max_card_w = 220
        available_width = max(self.screen_width - gap * (num_characters + 1), 100)
        card_w = min(max_card_w, max(100, available_width // num_characters))
        total_width = card_w * num_characters + gap * (num_characters - 1)
        start_x = max((self.screen_width - total_width) // 2, gap)
        max_scroll = max(0, total_width - self.screen_width + gap * 2)

        sel_center = start_x + self.selected_idx * (card_w + gap) + card_w // 2
        left_margin = 100
        right_margin = 100

        if sel_center - self.scroll_x < left_margin:
            self.scroll_x = max(0, sel_center - left_margin)
        elif sel_center - self.scroll_x > self.screen_width - right_margin:
            self.scroll_x = min(max_scroll, sel_center - (self.screen_width - right_margin))
        # clamp
        self.scroll_x = max(0, min(self.scroll_x, max_scroll))
        
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
        # Vẽ nền gradient đẹp
        self._draw_gradient_background(screen)
        
        # Vẽ các ngôi sao background
        import random
        random.seed(42)  # Fixed seed để stars không nhấp nháy
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height // 3)
            size = random.randint(1, 3)
            alpha = random.randint(100, 255)
            star_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            star_surf.fill((255, 255, 255, alpha))
            screen.blit(star_surf, (x, y))
        
        # Tiêu đề với shadow
        title_text = "CHỌN NHÂN VẬT"
        # Shadow
        title_shadow = self.font_big.render(title_text, True, (0, 0, 0))
        screen.blit(title_shadow, (self.screen_width//2 - title_shadow.get_width()//2 + 3, 33))
        # Main title với gradient effect
        title = self.font_big.render(title_text, True, (255, 215, 0))
        screen.blit(title, (self.screen_width//2 - title.get_width()//2, 30))
        
        # Vẽ các nhân vật với spacing và kích thước động để tránh chồng chéo
        num_characters = len(self.characters)

        # Compute layout
        gap = 30  # space between cards
        max_card_w = 220
        available_width = max(self.screen_width - gap * (num_characters + 1), 100)
        card_w = min(max_card_w, max(100, available_width // num_characters))
        top_margin = 120
        bottom_margin = 120
        max_card_h_allowed = max(150, self.screen_height - top_margin - bottom_margin)
        card_h = min(int(card_w * 1.45), max_card_h_allowed)
        total_width = card_w * num_characters + gap * (num_characters - 1)
        start_x = max((self.screen_width - total_width) // 2, gap)

        max_scroll = max(0, total_width - self.screen_width + gap * 2)
        # clamp scroll_x
        self.scroll_x = max(0, min(self.scroll_x, max_scroll))

        for i, char in enumerate(self.characters):
            # Center x for card i (apply current scroll)
            pos_x = start_x + i * (card_w + gap) + card_w // 2 - int(self.scroll_x)
            pos_y = self.screen_height // 2 - card_h // 2 - 20
            
            # Vẽ shadow cho card
            shadow_offset = 8
            shadow_rect = pygame.Rect(pos_x - card_w // 2 + shadow_offset, pos_y + shadow_offset, card_w, card_h)
            shadow_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 0, card_w, card_h), border_radius=12)
            screen.blit(shadow_surf, (shadow_rect.x, shadow_rect.y))
            
            # Determine ownership early
            cid = char.get('id') if 'id' in char else None
            user = getattr(self.game, 'current_user', None)
            owned = False
            if cid:
                if user:
                    profile = profile_manager.load_profile(user)
                    owned = cid in profile.get('purchased_characters', [])
                else:
                    owned = (char.get('price', 0) == 0)
            
            # Vẽ background card với gradient
            card_rect = pygame.Rect(pos_x - card_w // 2, pos_y, card_w, card_h)
            card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            
            # Background gradient cho card
            for y in range(card_h):
                progress = y / card_h
                if i == self.selected_idx and owned:
                    # Gold gradient cho selected
                    r = int(40 + (60 - 40) * progress)
                    g = int(30 + (45 - 30) * progress)
                    b = int(10 + (15 - 10) * progress)
                    alpha = 220
                elif owned:
                    # Blue gradient cho owned
                    r = int(20 + (30 - 20) * progress)
                    g = int(30 + (50 - 30) * progress)
                    b = int(50 + (70 - 50) * progress)
                    alpha = 200
                else:
                    # Gray gradient cho locked
                    r = int(30 + (40 - 30) * progress)
                    g = int(30 + (40 - 30) * progress)
                    b = int(35 + (45 - 35) * progress)
                    alpha = 180
                pygame.draw.line(card_surf, (r, g, b, alpha), (0, y), (card_w, y))
            
            screen.blit(card_surf, (card_rect.x, card_rect.y))
            
            # Vẽ khung nhân vật với hiệu ứng đặc biệt cho nhân vật được chọn
            if i == self.selected_idx:
                # Multi-layer glow effect
                for layer in range(3):
                    glow_offset = 8 - layer * 2
                    glow_alpha = 60 - layer * 15
                    glow_rect = pygame.Rect(pos_x - card_w // 2 - glow_offset, pos_y - glow_offset, 
                                           card_w + glow_offset * 2, card_h + glow_offset * 2)
                    glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 215, 0, glow_alpha), glow_surf.get_rect(), border_radius=12)
                    screen.blit(glow_surf, (glow_rect.x, glow_rect.y))
                
                frame_color = (255, 215, 0)  # Vàng gold
                frame_width = 4
            else:
                frame_color = (100, 150, 180) if owned else (80, 80, 80)
                frame_width = 2
            
            # Khung chính với border radius
            pygame.draw.rect(screen, frame_color, card_rect, frame_width, border_radius=12)
            
            # Vẽ tên nhân vật với shadow
            if not owned:
                name_color = (120, 120, 120)
            else:
                name_color = (255, 215, 0) if i == self.selected_idx else (220, 220, 255)
            
            font_name = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
            # Shadow cho tên
            name_shadow = font_name.render(char["name"], True, (0, 0, 0))
            screen.blit(name_shadow, (pos_x - name_shadow.get_width()//2 + 2, pos_y - 48))
            # Tên chính
            name_surf = font_name.render(char["name"], True, name_color)
            screen.blit(name_surf, (pos_x - name_surf.get_width()//2, pos_y - 50))
            
            # Vẽ ảnh preview - scale preserving aspect ratio to fit inside a preview box
            preview = char["preview"]
            p_w, p_h = preview.get_width(), preview.get_height()
            preview_max_w = int(card_w * 0.8)
            preview_max_h = int(card_h * 0.48)
            # compute scale factor preserving aspect ratio
            try:
                scale_f = min(preview_max_w / p_w, preview_max_h / p_h, 1.0)
                new_w = max(1, int(p_w * scale_f))
                new_h = max(1, int(p_h * scale_f))
                preview = pygame.transform.scale(preview, (new_w, new_h))
            except Exception:
                pass
            preview_pos = (pos_x - preview.get_width() // 2, pos_y + 8)
            screen.blit(preview, preview_pos)
            
            # Vẽ thông số với font nhỏ hơn
            stats_y = pos_y + card_h - 100
            stats = char["stats"]
            font_stats = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 18)  # Font nhỏ hơn
            
            # Get equipment bonuses for this character
            equipment_bonuses = {'hp': 0, 'damage': 0, 'defense': 0, 'speed': 0}
            if user and cid and owned:
                try:
                    from ma_nguon.doi_tuong.equipment import get_equipment_manager
                    profile = profile_manager.load_profile(user)
                    char_equipment = profile.get('character_equipment', {}).get(cid, {})
                    
                    if char_equipment:
                        eq_manager = get_equipment_manager()
                        for slot_type, eq_name in char_equipment.items():
                            eq = eq_manager.get_equipment_by_name(eq_name)
                            if eq:
                                equipment_bonuses['hp'] += eq.hp_bonus
                                equipment_bonuses['damage'] += eq.attack_bonus
                                equipment_bonuses['defense'] += eq.defense_bonus
                                equipment_bonuses['speed'] += eq.speed_bonus
                except Exception:
                    pass
            
            # Draw stats aligned inside the card với màu sắc đẹp hơn
            stat_x = pos_x - card_w // 2 + 12
            
            if owned:
                # HP với bonus (hiển thị tổng)
                hp_base = stats['hp']
                hp_bonus = equipment_bonuses['hp']
                hp_total = hp_base + hp_bonus
                if hp_bonus > 0:
                    hp_text = font_stats.render(f"HP: {hp_total}", True, (255, 120, 120))
                    hp_bonus_text = font_stats.render(f"(+{hp_bonus})", True, (120, 255, 120))
                    screen.blit(hp_text, (stat_x, stats_y))
                    screen.blit(hp_bonus_text, (stat_x + hp_text.get_width() + 5, stats_y))
                else:
                    hp_text = font_stats.render(f"HP: {hp_base}", True, (255, 120, 120))
                    screen.blit(hp_text, (stat_x, stats_y))

                # Speed với bonus
                speed_base = stats['speed']
                speed_bonus = equipment_bonuses['speed']
                speed_total = speed_base + speed_bonus
                if speed_bonus > 0:
                    speed_text = font_stats.render(f"Tốc: {speed_total}", True, (255, 255, 120))
                    speed_bonus_text = font_stats.render(f"(+{speed_bonus})", True, (120, 255, 120))
                    screen.blit(speed_text, (stat_x, stats_y + 22))
                    screen.blit(speed_bonus_text, (stat_x + speed_text.get_width() + 5, stats_y + 22))
                else:
                    speed_text = font_stats.render(f"Tốc: {speed_base}", True, (255, 255, 120))
                    screen.blit(speed_text, (stat_x, stats_y + 22))

                # Damage với bonus
                dmg_base = stats['damage']
                dmg_bonus = equipment_bonuses['damage']
                dmg_total = dmg_base + dmg_bonus
                if dmg_bonus > 0:
                    dmg_text = font_stats.render(f"ST: {dmg_total}", True, (255, 180, 100))
                    dmg_bonus_text = font_stats.render(f"(+{dmg_bonus})", True, (120, 255, 120))
                    screen.blit(dmg_text, (stat_x, stats_y + 44))
                    screen.blit(dmg_bonus_text, (stat_x + dmg_text.get_width() + 5, stats_y + 44))
                else:
                    dmg_text = font_stats.render(f"ST: {dmg_base}", True, (255, 180, 100))
                    screen.blit(dmg_text, (stat_x, stats_y + 44))

                # Defense với bonus
                def_base = stats['defense']
                def_bonus = equipment_bonuses['defense']
                def_total = def_base + def_bonus
                if def_bonus > 0:
                    def_text = font_stats.render(f"PT: {def_total}", True, (120, 180, 255))
                    def_bonus_text = font_stats.render(f"(+{def_bonus})", True, (120, 255, 120))
                    screen.blit(def_text, (stat_x, stats_y + 66))
                    screen.blit(def_bonus_text, (stat_x + def_text.get_width() + 5, stats_y + 66))
                else:
                    def_text = font_stats.render(f"PT: {def_base}", True, (120, 180, 255))
                    screen.blit(def_text, (stat_x, stats_y + 66))
                
                # Thêm chỉ báo đặc biệt cho nhân vật đặc biệt
                if cid == 'chien_than_lac_hong':
                    special_surf = pygame.Surface((card_w - 10, 25), pygame.SRCALPHA)
                    pygame.draw.rect(special_surf, (255, 0, 127, 60), special_surf.get_rect(), border_radius=8)
                    screen.blit(special_surf, (pos_x - card_w // 2 + 5, pos_y + card_h - 95))
                    special_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 14).render("★ HUYỀN THOẠI ★", True, (255, 180, 200))
                    screen.blit(special_text, (pos_x - special_text.get_width() // 2, pos_y + card_h - 92))

            else:  # Not owned - locked character
                # Dark overlay với gradient
                overlay = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                for y in range(card_h):
                    alpha = int(120 + (180 - 120) * (y / card_h))
                    pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (card_w, y))
                screen.blit(overlay, (pos_x - card_w // 2, pos_y))
                
                # Stats với màu xám
                mute_color = (130, 130, 140)
                hp_text = font_stats.render(f"HP: {stats['hp']}", True, mute_color)
                screen.blit(hp_text, (stat_x, stats_y))
                speed_text = font_stats.render(f"Tốc: {stats['speed']}", True, mute_color)
                screen.blit(speed_text, (stat_x, stats_y + 22))
                dmg_text = font_stats.render(f"ST: {stats['damage']}", True, mute_color)
                screen.blit(dmg_text, (stat_x, stats_y + 44))
                def_text = font_stats.render(f"PT: {stats['defense']}", True, mute_color)
                screen.blit(def_text, (stat_x, stats_y + 66))
                
                # Lock icon lớn ở giữa
                lock_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 48)
                lock_icon = lock_font.render("🔒", True, (200, 200, 200))
                screen.blit(lock_icon, (pos_x - lock_icon.get_width() // 2, pos_y + card_h // 2 - 40))
                
                # Hint text với background
                hint_text = "chưa sỏ hữu"
                hint_font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 14)
                hint = hint_font.render(hint_text, True, (220, 220, 220))
                hint_bg = pygame.Surface((hint.get_width() + 16, hint.get_height() + 8), pygame.SRCALPHA)
                pygame.draw.rect(hint_bg, (0, 0, 0, 140), hint_bg.get_rect(), border_radius=8)
                screen.blit(hint_bg, (pos_x - hint_bg.get_width() // 2, pos_y + card_h - 26))
                screen.blit(hint, (pos_x - hint.get_width() // 2, pos_y + card_h - 22))

        # Hướng dẫn với background đẹp
        guide_text = "← → chọn  |  ENTER xác nhận  |  ESC quay lại  |  S mở Shop"
        guide = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 22).render(guide_text, True, (220, 220, 255))
        guide_bg = pygame.Surface((guide.get_width() + 40, guide.get_height() + 20), pygame.SRCALPHA)
        pygame.draw.rect(guide_bg, (20, 30, 50, 200), guide_bg.get_rect(), border_radius=12)
        pygame.draw.rect(guide_bg, (100, 150, 200, 100), guide_bg.get_rect(), 2, border_radius=12)
        guide_x = self.screen_width // 2 - guide_bg.get_width() // 2
        guide_y = self.screen_height - 60
        screen.blit(guide_bg, (guide_x, guide_y))
        screen.blit(guide, (guide_x + 20, guide_y + 10))

        # Draw horizontal scrollbar if needed
        try:
            if total_width > self.screen_width:
                bar_h = 12
                bar_w = self.screen_width - 160
                bar_x = 80
                bar_y = self.screen_height - 60
                pygame.draw.rect(screen, (60,60,60), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
                # thumb
                thumb_w = max(40, int(bar_w * (self.screen_width / total_width)))
                max_thumb_x = bar_w - thumb_w
                thumb_x = int(bar_x + (self.scroll_x / max_scroll) * max_thumb_x) if max_scroll>0 else bar_x
                pygame.draw.rect(screen, (200,200,200), (thumb_x, bar_y, thumb_w, bar_h), border_radius=6)
        except Exception:
            pass