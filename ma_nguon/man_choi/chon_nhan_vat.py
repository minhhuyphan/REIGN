import pygame
import os
from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
from ma_nguon.core import profile_manager
from ma_nguon.doi_tuong.character_stats import CHARACTER_STATS

class CharacterSelectScene:
    def __init__(self, game):
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
                    self._set_message('Nhân vật bị khoá. Vào cửa hàng (nhấn S) để mua.', 180)
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
                
                if char_id in character_equipment:
                    eq_manager = get_equipment_manager()
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
        # Vẽ nền
        screen.fill((30, 30, 60))
        
        # Tiêu đề
        title = self.font_big.render("CHỌN NHÂN VẬT", True, (255, 255, 0))
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
            
            # Vẽ khung nhân vật với hiệu ứng đặc biệt cho nhân vật được chọn
            if i == self.selected_idx:
                frame_color = (255, 215, 0)  # Vàng gold cho nhân vật được chọn
                # Vẽ hiệu ứng glow
                glow_rect = pygame.Rect(pos_x - card_w // 2 - 5, pos_y - 10, card_w + 10, card_h + 20)
                try:
                    # draw with alpha if supported
                    glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, (255, 215, 0, 40), glow_surf.get_rect(), border_radius=8)
                    screen.blit(glow_surf, (glow_rect.x, glow_rect.y))
                except Exception:
                    pygame.draw.rect(screen, (255, 255, 0), glow_rect, 6)
            else:
                frame_color = (100, 100, 100)
            
            # Khung chính
            main_rect = pygame.Rect(pos_x - card_w // 2, pos_y, card_w, card_h)
            pygame.draw.rect(screen, frame_color, main_rect, 3, border_radius=6)
            
            # Determine ownership early so we can color the name appropriately
            cid = char.get('id') if 'id' in char else None
            user = getattr(self.game, 'current_user', None)
            owned = False
            if cid:
                if user:
                    profile = profile_manager.load_profile(user)
                    owned = cid in profile.get('purchased_characters', [])
                else:
                    owned = (char.get('price', 0) == 0)

            # Vẽ tên nhân vật với màu đặc biệt (muted if locked)
            if not owned:
                name_color = (140, 140, 140)
            else:
                name_color = (255, 215, 0) if i == self.selected_idx else (255, 255, 255)
            # Font nhỏ hơn cho tên dài
            font_name = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 24)
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
            
            # Draw stats aligned inside the card
            stat_x = pos_x - card_w // 2 + 12
            
            # HP với bonus (hiển thị tổng)
            hp_base = stats['hp']
            hp_bonus = equipment_bonuses['hp']
            hp_total = hp_base + hp_bonus
            if hp_bonus > 0:
                hp_text = font_stats.render(f"HP: {hp_total}", True, (255, 100, 100))
                hp_bonus_text = font_stats.render(f"(+{hp_bonus})", True, (100, 255, 100))
                screen.blit(hp_text, (stat_x, stats_y))
                screen.blit(hp_bonus_text, (stat_x + hp_text.get_width() + 5, stats_y))
            else:
                hp_text = font_stats.render(f"HP: {hp_base}", True, (255, 100, 100))
                screen.blit(hp_text, (stat_x, stats_y))

            # Speed với bonus
            speed_base = stats['speed']
            speed_bonus = equipment_bonuses['speed']
            speed_total = speed_base + speed_bonus
            if speed_bonus > 0:
                speed_text = font_stats.render(f"Tốc: {speed_total}", True, (100, 255, 100))
                speed_bonus_text = font_stats.render(f"(+{speed_bonus})", True, (100, 255, 100))
                screen.blit(speed_text, (stat_x, stats_y + 22))
                screen.blit(speed_bonus_text, (stat_x + speed_text.get_width() + 5, stats_y + 22))
            else:
                speed_text = font_stats.render(f"Tốc: {speed_base}", True, (100, 255, 100))
                screen.blit(speed_text, (stat_x, stats_y + 22))

            # Damage với bonus
            dmg_base = stats['damage']
            dmg_bonus = equipment_bonuses['damage']
            dmg_total = dmg_base + dmg_bonus
            if dmg_bonus > 0:
                dmg_text = font_stats.render(f"ST: {dmg_total}", True, (255, 255, 100))
                dmg_bonus_text = font_stats.render(f"(+{dmg_bonus})", True, (100, 255, 100))
                screen.blit(dmg_text, (stat_x, stats_y + 44))
                screen.blit(dmg_bonus_text, (stat_x + dmg_text.get_width() + 5, stats_y + 44))
            else:
                dmg_text = font_stats.render(f"ST: {dmg_base}", True, (255, 255, 100))
                screen.blit(dmg_text, (stat_x, stats_y + 44))

            # Defense với bonus
            def_base = stats['defense']
            def_bonus = equipment_bonuses['defense']
            def_total = def_base + def_bonus
            if def_bonus > 0:
                def_text = font_stats.render(f"PT: {def_total}", True, (100, 100, 255))
                def_bonus_text = font_stats.render(f"(+{def_bonus})", True, (100, 255, 100))
                screen.blit(def_text, (stat_x, stats_y + 66))
                screen.blit(def_bonus_text, (stat_x + def_text.get_width() + 5, stats_y + 66))
            else:
                def_text = font_stats.render(f"PT: {def_base}", True, (100, 100, 255))
                screen.blit(def_text, (stat_x, stats_y + 66))
            
            # Thêm chỉ báo đặc biệt chỉ cho Chiến Thần Lạc Hồng
            if cid == 'chien_than_lac_hong':
                special_text = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 16).render("★ HUYỀN THOẠI ★", True, (255, 0, 127))
                screen.blit(special_text, (pos_x - special_text.get_width() // 2, stats_y + 40))

            if not owned:
                # darken the entire character card to indicate locked
                overlay = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                screen.blit(overlay, (pos_x - card_w // 2, pos_y))
                # muted text for stats already handled by name_color above
                mute_color = (140, 140, 140)
                hp_text = font_stats.render(f"HP: {stats['hp']}", True, mute_color)
                screen.blit(hp_text, (stat_x, stats_y))
                speed_text = font_stats.render(f"Tốc độ: {stats['speed']}", True, mute_color)
                screen.blit(speed_text, (stat_x, stats_y + 22))
                dmg_text = font_stats.render(f"ST: {stats['damage']}", True, mute_color)
                screen.blit(dmg_text, (stat_x, stats_y + 44))
                def_text = font_stats.render(f"PT: {stats['defense']}", True, mute_color)
                screen.blit(def_text, (stat_x, stats_y + 66))
                # show buy hint
                hint = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18).render("Bị khoá — vào cửa hàng (S)", True, (200,200,200))
                screen.blit(hint, (pos_x - hint.get_width() // 2, pos_y + card_h - 40))

        # Hướng dẫn
        guide = self.font_small.render("← → để chọn, ENTER để xác nhận, ESC để quay lại", True, (200, 200, 200))
        screen.blit(guide, (self.screen_width//2 - guide.get_width()//2, self.screen_height - 40))

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