"""
Equipment Screen - Màn hình quản lý trang bị
Hiển thị kho đồ bên trái và 3 slot trang bị bên phải
"""

import pygame
from ma_nguon.doi_tuong.equipment import get_equipment_manager
from ma_nguon.doi_tuong.character_stats import get_character_stats


class EquipmentScreen:
    """Màn hình quản lý trang bị"""
    
    def __init__(self, game, player_character=None):
        self.game = game
        self.player_character = player_character
        self.equipment_manager = get_equipment_manager()
        
        # Load inventory from profile
        self._load_inventory_from_profile()
        
        # Character selection
        self.available_characters = self._get_available_characters()
        self.selected_character_idx = 0
        self.current_character_id = self.available_characters[0]['id'] if self.available_characters else None
        
        # UI Constants
        self.SLOT_SIZE = 80
        self.SLOT_MARGIN = 20
        self.INVENTORY_START_X = 50
        self.INVENTORY_START_Y = 150
        self.EQUIP_SLOTS_X = 600
        self.EQUIP_SLOTS_Y = 200
        
        # Character selection UI
        self.CHAR_CARD_SIZE = 100
        self.CHAR_CARD_MARGIN = 15
        self.CHAR_SELECTOR_Y = 120
        
        # Colors
        self.BG_COLOR = (15, 15, 35)
        self.BG_GRADIENT_TOP = (20, 20, 50)
        self.BG_GRADIENT_BOTTOM = (10, 10, 30)
        self.SLOT_COLOR = (40, 40, 70)
        self.SLOT_HOVER_COLOR = (60, 60, 100)
        self.SLOT_EQUIPPED_COLOR = (80, 120, 80)
        self.SLOT_SELECTED_COLOR = (120, 80, 150)
        self.TEXT_COLOR = (255, 255, 255)
        self.GOLD_COLOR = (255, 215, 0)
        self.ACCENT_COLOR = (100, 200, 255)
        self.CARD_BG = (30, 30, 60)
        self.CARD_SELECTED = (70, 100, 150)
        
        # Font
        try:
            self.title_font = pygame.font.Font("tai_nguyen/font/Fz-Donsky.ttf", 48)
            self.font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 24)
            self.small_font = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 18)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        
        # Selection state
        self.selected_equipment = None
        self.hovered_slot = None
        self.hovered_char_idx = None
        self.show_tooltip = False
        self.tooltip_equipment = None
        self.tooltip_pos = (0, 0)
        
        # Scrollbar state
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scrollbar_dragging = False
        self.scrollbar_drag_offset = 0
        
        # Animation
        self.pulse_timer = 0
        self.glow_alpha = 0
        self.glow_direction = 1
    
    def _load_inventory_from_profile(self):
        """Load trang bị từ profile của user"""
        from ma_nguon.core import profile_manager
        
        user = getattr(self.game, 'current_user', None)
        if user:
            profile = profile_manager.load_profile(user)
            inventory = profile.get('equipment_inventory', {})
            
            # Convert old list format to dict
            if isinstance(inventory, list):
                new_inventory = {}
                for item in inventory:
                    new_inventory[item] = new_inventory.get(item, 0) + 1
                inventory = new_inventory
            
            print(f"[EQUIPMENT_SCREEN] Loading inventory: {inventory}")
            self.equipment_manager.load_inventory_from_profile(inventory)
            
            # Load character equipment (trang bị đã lắp)
            character_equipment = profile.get('character_equipment', {})
            if character_equipment:
                print(f"[EQUIPMENT_SCREEN] Loading character equipment: {character_equipment}")
                for char_id, equipment_data in character_equipment.items():
                    self.equipment_manager.load_character_equipment(char_id, equipment_data)
        else:
            print("[EQUIPMENT_SCREEN] No user logged in, using default equipment")
    
    def _get_available_characters(self):
        """Lấy danh sách nhân vật có sẵn từ profile"""
        characters = [
            {"id": "chien_binh", "name": "Chiến binh", "preview": "tai_nguyen/hinh_anh/nhan_vat/chien_binh/dung_yen/0.png"},
            {"id": "ninja", "name": "Ninja", "preview": "tai_nguyen/hinh_anh/nhan_vat/ninja/dung_yen/0.png"},
            {"id": "vo_si", "name": "Võ sĩ", "preview": "tai_nguyen/hinh_anh/nhan_vat/vo_si/dung_yen/0.png"},
            {"id": "chien_than_lac_hong", "name": "Chiến Thần", "preview": "tai_nguyen/hinh_anh/nhan_vat/chien_than_lac_hong/dung_yen/0.png"},
            {"id": "tho_san_quai_vat", "name": "Thợ Săn", "preview": "tai_nguyen/hinh_anh/nhan_vat/tho_san_quai_vat/dung_yen/0.png"},
            {"id": "mi_anh", "name": "Mị Ảnh", "preview": "tai_nguyen/hinh_anh/nhan_vat/Mi_Anh/dung_yen/0.png"},
            {"id": "van_dao", "name": "Vân Dao", "preview": "tai_nguyen/hinh_anh/nhan_vat/Van_Dao/dung_yen/0.png"},
        ]
        
        # Load preview images
        for char in characters:
            try:
                img = pygame.image.load(char["preview"]).convert_alpha()
                char["preview_img"] = pygame.transform.scale(img, (60, 80))
            except:
                char["preview_img"] = None
        
        return characters
        
    def _get_current_character(self):
        """Lấy thông tin nhân vật hiện tại"""
        if 0 <= self.selected_character_idx < len(self.available_characters):
            return self.available_characters[self.selected_character_idx]
        return None
        
    def handle_event(self, event):
        """Xử lý sự kiện"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                # Save equipment trước khi thoát
                self._save_equipment_to_profile()
                # Quay lại menu hoặc game
                self.game.change_scene("menu")
            elif event.key == pygame.K_LEFT:
                # Chuyển sang nhân vật trước
                self.selected_character_idx = (self.selected_character_idx - 1) % len(self.available_characters)
                self.current_character_id = self.available_characters[self.selected_character_idx]['id']
                self.selected_equipment = None
            elif event.key == pygame.K_RIGHT:
                # Chuyển sang nhân vật sau
                self.selected_character_idx = (self.selected_character_idx + 1) % len(self.available_characters)
                self.current_character_id = self.available_characters[self.selected_character_idx]['id']
                self.selected_equipment = None
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_click(event.pos)
            elif event.button == 4:  # Mouse wheel up
                self.scroll_offset = max(0, self.scroll_offset - 40)
            elif event.button == 5:  # Mouse wheel down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 40)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.scrollbar_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.scrollbar_dragging:
                self._handle_scrollbar_drag(event.pos)
            else:
                self._handle_hover(event.pos)
    
    def _handle_click(self, mouse_pos):
        """Xử lý click chuột"""
        mx, my = mouse_pos
        
        # Check scrollbar click
        scrollbar_rect = self._get_scrollbar_rect()
        if scrollbar_rect and scrollbar_rect.collidepoint(mx, my):
            self.scrollbar_dragging = True
            self.scrollbar_drag_offset = my - scrollbar_rect.y
            return
        
        # Check character card clicks
        start_x = (self.game.WIDTH - (len(self.available_characters) * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN))) // 2
        for i, char in enumerate(self.available_characters):
            card_x = start_x + i * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN)
            card_y = self.CHAR_SELECTOR_Y
            card_rect = pygame.Rect(card_x, card_y, self.CHAR_CARD_SIZE, self.CHAR_CARD_SIZE)
            
            if card_rect.collidepoint(mx, my):
                self.selected_character_idx = i
                self.current_character_id = char['id']
                self.selected_equipment = None
                return
        
        # Check inventory clicks (với scroll offset)
        all_equipment = self.equipment_manager.get_all_equipment()
        inventory_y_start = 320
        items_per_row = 3  # Tăng lên 3 cột
        
        for i, equipment in enumerate(all_equipment):
            slot_x = self.INVENTORY_START_X + (i % items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN)
            slot_y = inventory_y_start + (i // items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN) - self.scroll_offset
            
            # Check if visible in panel
            if slot_y < 305 or slot_y > 730:
                continue
            
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            
            if slot_rect.collidepoint(mx, my):
                if self.selected_equipment == equipment:
                    self.selected_equipment = None  # Deselect
                else:
                    self.selected_equipment = equipment
                return
        
        # Check equip slot clicks
        equip_slots = ['attack', 'defense', 'speed']
        equip_slots_y_start = 320
        for i, slot_type in enumerate(equip_slots):
            slot_x = 580  # Match with _draw_equip_slots
            slot_y = equip_slots_y_start + i * (self.SLOT_SIZE + self.SLOT_MARGIN)
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            
            if slot_rect.collidepoint(mx, my):
                if self.selected_equipment:
                    # Try to equip
                    if self.selected_equipment.equipment_type == slot_type:
                        # Unequip from previous character if equipped
                        if self.selected_equipment.equipped_to is not None:
                            self.equipment_manager.unequip(self.selected_equipment, self.selected_equipment.equipped_to)
                        
                        # Unequip current item in that slot for this character
                        current_eq_name = self.equipment_manager.get_character_equipment(self.current_character_id).get(slot_type)
                        if current_eq_name:
                            old_eq = self.equipment_manager.get_equipment_by_name(current_eq_name)
                            if old_eq:
                                self.equipment_manager.unequip(old_eq, self.current_character_id)
                        
                        # Equip new item
                        self.equipment_manager.equip_to_character(self.selected_equipment, self.current_character_id)
                        self.selected_equipment = None
                        
                        # Auto-save sau khi equip
                        self._save_equipment_to_profile()
                else:
                    # Unequip if there's equipment in this slot
                    current_eq_name = self.equipment_manager.get_character_equipment(self.current_character_id).get(slot_type)
                    if current_eq_name:
                        eq = self.equipment_manager.get_equipment_by_name(current_eq_name)
                        if eq:
                            self.equipment_manager.unequip(eq, self.current_character_id)
                            
                            # Auto-save sau khi unequip
                            self._save_equipment_to_profile()
                return
    
    def _handle_hover(self, mouse_pos):
        """Xử lý hover chuột để hiển thị tooltip"""
        mx, my = mouse_pos
        self.show_tooltip = False
        self.hovered_char_idx = None
        
        # Check character card hover
        start_x = (self.game.WIDTH - (len(self.available_characters) * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN))) // 2
        for i, char in enumerate(self.available_characters):
            card_x = start_x + i * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN)
            card_y = self.CHAR_SELECTOR_Y
            card_rect = pygame.Rect(card_x, card_y, self.CHAR_CARD_SIZE, self.CHAR_CARD_SIZE)
            
            if card_rect.collidepoint(mx, my):
                self.hovered_char_idx = i
                break
        
        # Check inventory hover (với scroll offset)
        all_equipment = self.equipment_manager.get_all_equipment()
        inventory_y_start = 320
        items_per_row = 3
        
        for i, equipment in enumerate(all_equipment):
            slot_x = self.INVENTORY_START_X + (i % items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN)
            slot_y = inventory_y_start + (i // items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN) - self.scroll_offset
            
            # Check if visible
            if slot_y < 305 or slot_y > 730:
                continue
            
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            
            if slot_rect.collidepoint(mx, my):
                self.show_tooltip = True
                self.tooltip_equipment = equipment
                self.tooltip_pos = (mx + 10, my + 10)
                return
        
        # Check equip slot clicks
        equip_slots = ['attack', 'defense', 'speed']
        equip_slots_y_start = 320
        for i, slot_type in enumerate(equip_slots):
            slot_x = self.EQUIP_SLOTS_X
            slot_y = equip_slots_y_start + i * (self.SLOT_SIZE + self.SLOT_MARGIN)
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            
            if slot_rect.collidepoint(mx, my):
                # Get equipment for current character
                eq_name = self.equipment_manager.get_character_equipment(self.current_character_id).get(slot_type)
                if eq_name:
                    equipment = self.equipment_manager.get_equipment_by_name(eq_name)
                    if equipment:
                        self.show_tooltip = True
                        self.tooltip_equipment = equipment
                        self.tooltip_pos = (mx + 10, my + 10)
                return
    
    def _handle_scrollbar_drag(self, mouse_pos):
        """Xử lý kéo thanh cuộn"""
        mx, my = mouse_pos
        
        # Calculate scrollbar area
        scrollbar_track_y = 305
        scrollbar_track_height = 420
        
        # Calculate new scroll position
        new_y = my - self.scrollbar_drag_offset
        new_y = max(scrollbar_track_y, min(new_y, scrollbar_track_y + scrollbar_track_height - 60))
        
        # Convert to scroll offset
        if scrollbar_track_height > 60:
            ratio = (new_y - scrollbar_track_y) / (scrollbar_track_height - 60)
            self.scroll_offset = int(ratio * self.max_scroll)
    
    def _get_scrollbar_rect(self):
        """Lấy vị trí thanh cuộn"""
        if self.max_scroll <= 0:
            return None
        
        scrollbar_x = 365
        scrollbar_track_y = 305
        scrollbar_track_height = 420
        scrollbar_width = 10
        scrollbar_handle_height = 60
        
        # Calculate handle position
        if self.max_scroll > 0:
            ratio = self.scroll_offset / self.max_scroll
            handle_y = scrollbar_track_y + ratio * (scrollbar_track_height - scrollbar_handle_height)
        else:
            handle_y = scrollbar_track_y
        
        return pygame.Rect(scrollbar_x, int(handle_y), scrollbar_width, scrollbar_handle_height)
    
    def update(self):
        """Cập nhật logic"""
        # Animation cho glow effect
        self.pulse_timer += 1
        self.glow_alpha += self.glow_direction * 3
        if self.glow_alpha >= 60:
            self.glow_direction = -1
        elif self.glow_alpha <= 0:
            self.glow_direction = 1
        self.glow_alpha = max(0, min(60, self.glow_alpha))
    
    def draw(self, screen):
        """Vẽ màn hình"""
        # Draw gradient background
        self._draw_gradient_background(screen)
        
        # Title with shadow
        self._draw_title_with_shadow(screen, "TRANG BỊ NHÂN VẬT", self.game.WIDTH // 2, 40)
        
        # Instructions
        instruction_text = self.small_font.render("Click nhân vật để chọn | Click trang bị để gắn | ESC: Thoát", True, self.ACCENT_COLOR)
        instruction_rect = instruction_text.get_rect(center=(screen.get_width() // 2, 85))
        screen.blit(instruction_text, instruction_rect)
        
        # Draw character selector cards
        self._draw_character_cards(screen)
        
        # Draw panels with borders
        self._draw_panel(screen, 30, 270, 350, 480, "KHO TRANG BỊ")
        self._draw_panel(screen, 560, 270, 400, 480, "TRANG BỊ HIỆN TẠI")
        self._draw_panel(screen, 1000, 270, 350, 300, "THÔNG SỐ")
        
        # Draw inventory section
        self._draw_inventory(screen)
        
        # Draw equip slots section
        self._draw_equip_slots(screen)
        
        # Draw tooltip
        if self.show_tooltip and self.tooltip_equipment:
            self._draw_tooltip(screen)
    
    def _draw_gradient_background(self, screen):
        """Vẽ background với gradient"""
        for y in range(screen.get_height()):
            ratio = y / screen.get_height()
            r = int(self.BG_GRADIENT_TOP[0] + (self.BG_GRADIENT_BOTTOM[0] - self.BG_GRADIENT_TOP[0]) * ratio)
            g = int(self.BG_GRADIENT_TOP[1] + (self.BG_GRADIENT_BOTTOM[1] - self.BG_GRADIENT_TOP[1]) * ratio)
            b = int(self.BG_GRADIENT_TOP[2] + (self.BG_GRADIENT_BOTTOM[2] - self.BG_GRADIENT_TOP[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen.get_width(), y))
    
    def _draw_title_with_shadow(self, screen, text, x, y):
        """Vẽ tiêu đề với shadow"""
        # Shadow
        shadow_surf = self.title_font.render(text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(x + 3, y + 3))
        screen.blit(shadow_surf, shadow_rect)
        
        # Main title
        title_surf = self.title_font.render(text, True, self.GOLD_COLOR)
        title_rect = title_surf.get_rect(center=(x, y))
        screen.blit(title_surf, title_rect)
    
    def _draw_panel(self, screen, x, y, width, height, title):
        """Vẽ panel với viền và tiêu đề"""
        # Panel background với alpha
        panel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*self.CARD_BG, 180), (0, 0, width, height), border_radius=10)
        screen.blit(panel_surf, (x, y))
        
        # Border
        pygame.draw.rect(screen, self.ACCENT_COLOR, (x, y, width, height), 2, border_radius=10)
        
        # Title bar
        title_height = 35
        pygame.draw.rect(screen, (*self.ACCENT_COLOR, 100), (x, y, width, title_height), border_radius=10)
        pygame.draw.line(screen, self.ACCENT_COLOR, (x, y + title_height), (x + width, y + title_height), 2)
        
        # Title text
        title_surf = self.small_font.render(title, True, self.TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(x + width // 2, y + title_height // 2))
        screen.blit(title_surf, title_rect)
    
    def _draw_character_cards(self, screen):
        """Vẽ character cards có thể click"""
        start_x = (screen.get_width() - (len(self.available_characters) * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN))) // 2
        
        for i, char in enumerate(self.available_characters):
            card_x = start_x + i * (self.CHAR_CARD_SIZE + self.CHAR_CARD_MARGIN)
            card_y = self.CHAR_SELECTOR_Y
            
            # Determine card appearance
            is_selected = (i == self.selected_character_idx)
            is_hovered = (i == self.hovered_char_idx)
            
            # Draw card background with hover/selected effect
            if is_selected:
                # Selected card - glowing effect
                glow_surf = pygame.Surface((self.CHAR_CARD_SIZE + 10, self.CHAR_CARD_SIZE + 10), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.GOLD_COLOR, self.glow_alpha), 
                               (0, 0, self.CHAR_CARD_SIZE + 10, self.CHAR_CARD_SIZE + 10), border_radius=10)
                screen.blit(glow_surf, (card_x - 5, card_y - 5))
                
                card_color = self.CARD_SELECTED
                border_color = self.GOLD_COLOR
                border_width = 3
            elif is_hovered:
                card_color = (50, 70, 100)
                border_color = self.ACCENT_COLOR
                border_width = 2
            else:
                card_color = self.CARD_BG
                border_color = (80, 80, 100)
                border_width = 1
            
            # Card background
            card_surf = pygame.Surface((self.CHAR_CARD_SIZE, self.CHAR_CARD_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(card_surf, (*card_color, 200), (0, 0, self.CHAR_CARD_SIZE, self.CHAR_CARD_SIZE), border_radius=10)
            screen.blit(card_surf, (card_x, card_y))
            
            # Border
            pygame.draw.rect(screen, border_color, 
                           (card_x, card_y, self.CHAR_CARD_SIZE, self.CHAR_CARD_SIZE), 
                           border_width, border_radius=10)
            
            # Character preview image
            if char.get("preview_img"):
                img_x = card_x + (self.CHAR_CARD_SIZE - char["preview_img"].get_width()) // 2
                img_y = card_y + 10
                screen.blit(char["preview_img"], (img_x, img_y))
            
            # Character name
            name_surf = pygame.font.Font("tai_nguyen/font/Fz-Futurik.ttf", 14).render(
                char["name"], True, self.GOLD_COLOR if is_selected else self.TEXT_COLOR
            )
            name_rect = name_surf.get_rect(center=(card_x + self.CHAR_CARD_SIZE // 2, card_y + self.CHAR_CARD_SIZE - 15))
            screen.blit(name_surf, name_rect)
            
            # Selection indicator
            if is_selected:
                indicator_surf = self.small_font.render("✓", True, self.GOLD_COLOR)
                screen.blit(indicator_surf, (card_x + 5, card_y + 5))
    
    def _draw_inventory(self, screen):
        """Vẽ kho đồ (inventory) với scrollbar"""
        # Draw equipment items
        inventory_y_start = 320
        all_equipment = self.equipment_manager.get_all_equipment()
        items_per_row = 3  # 3 cột
        
        # Calculate max scroll
        if all_equipment:
            total_rows = (len(all_equipment) + items_per_row - 1) // items_per_row
            content_height = total_rows * (self.SLOT_SIZE + self.SLOT_MARGIN)
            visible_height = 420  # Panel height - title
            self.max_scroll = max(0, content_height - visible_height)
        else:
            self.max_scroll = 0
        
        # Create clipping area for inventory
        panel_rect = pygame.Rect(30, 305, 350, 420)
        screen.set_clip(panel_rect)
        
        for i, equipment in enumerate(all_equipment):
            slot_x = self.INVENTORY_START_X + (i % items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN)
            slot_y = inventory_y_start + (i // items_per_row) * (self.SLOT_SIZE + self.SLOT_MARGIN) - self.scroll_offset
            
            # Only draw if visible
            if slot_y + self.SLOT_SIZE < 305 or slot_y > 730:
                continue
            
            # Determine slot color
            if equipment == self.selected_equipment:
                color = self.SLOT_SELECTED_COLOR
                border_width = 4
                # Glow effect
                glow_surf = pygame.Surface((self.SLOT_SIZE + 6, self.SLOT_SIZE + 6), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.ACCENT_COLOR, self.glow_alpha), 
                               (0, 0, self.SLOT_SIZE + 6, self.SLOT_SIZE + 6), border_radius=8)
                screen.blit(glow_surf, (slot_x - 3, slot_y - 3))
            elif equipment.equipped_to:
                color = self.SLOT_EQUIPPED_COLOR
                border_width = 2
            else:
                color = self.SLOT_COLOR
                border_width = 2
            
            # Draw slot with rounded corners
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            pygame.draw.rect(screen, color, slot_rect, border_radius=8)
            pygame.draw.rect(screen, self.TEXT_COLOR, slot_rect, border_width, border_radius=8)
            
            # Draw equipment image
            if equipment.image:
                img_x = slot_x + (self.SLOT_SIZE - equipment.image.get_width()) // 2
                img_y = slot_y + (self.SLOT_SIZE - equipment.image.get_height()) // 2
                screen.blit(equipment.image, (img_x, img_y))
            
            # Show equipped indicator
            if equipment.equipped_to:
                equipped_text = self.small_font.render("✓", True, (0, 255, 0))
                screen.blit(equipped_text, (slot_x + 5, slot_y + 5))
        
        # Remove clipping
        screen.set_clip(None)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            self._draw_scrollbar(screen)
    
    def _draw_equip_slots(self, screen):
        """Vẽ các slot trang bị"""
        equip_slots_y_start = 320
        equip_slots = [
            ('attack', 'CÔNG', (255, 100, 100)),
            ('defense', 'THỦ', (100, 255, 100)),
            ('speed', 'TỐC ĐỘ', (100, 150, 255))
        ]
        
        # Get current character's equipment
        character_eq = self.equipment_manager.get_character_equipment(self.current_character_id)
        
        for i, (slot_type, label, accent_color) in enumerate(equip_slots):
            slot_x = 580
            slot_y = equip_slots_y_start + i * (self.SLOT_SIZE + self.SLOT_MARGIN)
            
            # Draw slot
            slot_rect = pygame.Rect(slot_x, slot_y, self.SLOT_SIZE, self.SLOT_SIZE)
            
            # Check if equipment is equipped in this slot for current character
            eq_name = character_eq.get(slot_type)
            equipped_item = self.equipment_manager.get_equipment_by_name(eq_name) if eq_name else None
            
            if equipped_item:
                color = self.SLOT_EQUIPPED_COLOR
                # Subtle glow for equipped items
                glow_surf = pygame.Surface((self.SLOT_SIZE + 4, self.SLOT_SIZE + 4), pygame.SRCALPHA)
                glow_alpha = int(self.glow_alpha * 0.5)
                pygame.draw.rect(glow_surf, (*accent_color, glow_alpha), 
                               (0, 0, self.SLOT_SIZE + 4, self.SLOT_SIZE + 4), border_radius=8)
                screen.blit(glow_surf, (slot_x - 2, slot_y - 2))
            else:
                color = self.SLOT_COLOR
            
            pygame.draw.rect(screen, color, slot_rect, border_radius=8)
            pygame.draw.rect(screen, accent_color, slot_rect, 2, border_radius=8)
            
            # Draw equipped item image
            if equipped_item and equipped_item.image:
                img_x = slot_x + (self.SLOT_SIZE - equipped_item.image.get_width()) // 2
                img_y = slot_y + (self.SLOT_SIZE - equipped_item.image.get_height()) // 2
                screen.blit(equipped_item.image, (img_x, img_y))
            else:
                # Draw slot type icon/text when empty
                empty_text = self.small_font.render("?", True, (100, 100, 100))
                empty_rect = empty_text.get_rect(center=(slot_x + self.SLOT_SIZE // 2, slot_y + self.SLOT_SIZE // 2))
                screen.blit(empty_text, empty_rect)
            
            # Draw label with icon
            label_text = self.font.render(label, True, accent_color)
            label_x = slot_x + self.SLOT_SIZE + 15
            label_y = slot_y + (self.SLOT_SIZE - label_text.get_height()) // 2
            screen.blit(label_text, (label_x, label_y))
            
            # Draw equipment name if equipped
            if equipped_item:
                name_surf = self.small_font.render(equipped_item.name, True, self.TEXT_COLOR)
                screen.blit(name_surf, (label_x, label_y + 25))
        
        # Draw character stats with equipment
        self._draw_stats(screen, equip_slots_y_start)
    
    def _draw_stats(self, screen, equip_slots_y_start):
        """Vẽ thông số với equipment bonus"""
        # Draw panel for stats
        stats_panel_x = 1000
        stats_panel_y = 270
        stats_panel_w = 350
        stats_panel_h = 400  # Tăng height để hiển thị đầy đủ
        self._draw_panel(screen, stats_panel_x, stats_panel_y, stats_panel_w, stats_panel_h, "THÔNG SỐ")
        
        # Get character base stats
        char_stats = get_character_stats(self.current_character_id)
        base_hp = char_stats.get('hp', 0)
        base_damage = char_stats.get('damage', 0)
        base_defense = char_stats.get('defense', 0)
        base_speed = char_stats.get('speed', 0)
        
        # Calculate equipment bonuses
        character_eq = self.equipment_manager.get_character_equipment(self.current_character_id)
        
        attack_bonus = 0
        defense_bonus = 0
        hp_bonus = 0
        speed_bonus = 0
        
        for slot_type, eq_name in character_eq.items():
            eq = self.equipment_manager.get_equipment_by_name(eq_name)
            if eq:
                attack_bonus += eq.attack_bonus
                defense_bonus += eq.defense_bonus
                hp_bonus += eq.hp_bonus
                speed_bonus += eq.speed_bonus
        
        # Stat display configuration with base + bonus
        stats_config = [
            ("HP:", base_hp, hp_bonus, (255, 100, 255)),
            ("Công:", base_damage, attack_bonus, (255, 100, 100)),
            ("Thủ:", base_defense, defense_bonus, (100, 255, 100)),
            ("Tốc độ:", base_speed, speed_bonus, (100, 150, 255))
        ]
        
        # Draw stats inside panel
        stat_y = stats_panel_y + 60
        for label, base_value, bonus, color in stats_config:
            # Draw icon/indicator
            indicator_rect = pygame.Rect(stats_panel_x + 30, stat_y, 10, 10)
            pygame.draw.circle(screen, color, indicator_rect.center, 5)
            
            # Label
            label_surf = self.font.render(label, True, self.TEXT_COLOR)
            screen.blit(label_surf, (stats_panel_x + 60, stat_y - 5))
            
            # Base value
            base_text = str(base_value)
            base_surf = self.small_font.render(base_text, True, (200, 200, 200))
            screen.blit(base_surf, (stats_panel_x + 160, stat_y))
            
            # Bonus (if any)
            if bonus > 0:
                bonus_text = f"+{bonus}"
                bonus_surf = self.small_font.render(bonus_text, True, color)
                screen.blit(bonus_surf, (stats_panel_x + 210, stat_y))
                
                # Total
                total = base_value + bonus
                total_text = f"= {total}"
                total_surf = self.font.render(total_text, True, self.GOLD_COLOR)
                value_x = stats_panel_x + stats_panel_w - total_surf.get_width() - 20
                screen.blit(total_surf, (value_x, stat_y - 5))
            else:
                # No bonus, just show base
                total_surf = self.font.render(f"= {base_value}", True, (150, 150, 150))
                value_x = stats_panel_x + stats_panel_w - total_surf.get_width() - 20
                screen.blit(total_surf, (value_x, stat_y - 5))
            
            stat_y += 50
        
        # Draw separator
        stat_y += 10
        pygame.draw.line(screen, self.ACCENT_COLOR,
                       (stats_panel_x + 30, stat_y),
                       (stats_panel_x + stats_panel_w - 30, stat_y), 1)
        stat_y += 20
        
        # Draw special effects if any equipped item has them
        effects_title = self.small_font.render("HIỆU ỨNG ĐẶC BIỆT:", True, self.GOLD_COLOR)
        screen.blit(effects_title, (stats_panel_x + 30, stat_y))
        stat_y += 30
        
        has_effects = False
        for slot_type, eq_name in character_eq.items():
            eq = self.equipment_manager.get_equipment_by_name(eq_name)
            if eq:
                effects = []
                if eq.has_slow_effect:
                    effects.append("❄️ Làm chậm địch")
                if eq.has_burn_effect:
                    effects.append(f"🔥 Thiêu {eq.burn_damage} HP/{eq.burn_duration}s")
                if eq.has_revive_effect:
                    effects.append(f"✨ Hồi sinh {eq.revive_hp_percent}% HP")
                
                for effect_text in effects:
                    has_effects = True
                    effect_surf = self.small_font.render(effect_text, True, (200, 200, 100))
                    screen.blit(effect_surf, (stats_panel_x + 40, stat_y))
                    stat_y += 25
        
        if not has_effects:
            no_effect = self.small_font.render("Chưa có hiệu ứng", True, (100, 100, 100))
            screen.blit(no_effect, (stats_panel_x + 40, stat_y))

    
    def _draw_tooltip(self, screen):
        """Vẽ tooltip cho trang bị"""
        if not self.tooltip_equipment:
            return
        
        # Get description
        desc_lines = self.tooltip_equipment.get_description().split('\n')
        
        # Calculate tooltip size
        padding = 10
        line_height = 25
        max_width = max([self.small_font.size(line)[0] for line in desc_lines]) + 2 * padding
        tooltip_height = len(desc_lines) * line_height + 2 * padding
        
        # Tooltip background
        tooltip_x, tooltip_y = self.tooltip_pos
        
        # Keep tooltip on screen
        if tooltip_x + max_width > screen.get_width():
            tooltip_x = screen.get_width() - max_width - 10
        if tooltip_y + tooltip_height > screen.get_height():
            tooltip_y = screen.get_height() - tooltip_height - 10
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, max_width, tooltip_height)
        pygame.draw.rect(screen, (40, 40, 60), tooltip_rect)
        pygame.draw.rect(screen, self.GOLD_COLOR, tooltip_rect, 2)
        
        # Draw text lines
        y_offset = tooltip_y + padding
        for line in desc_lines:
            text_surf = self.small_font.render(line, True, self.TEXT_COLOR)
            screen.blit(text_surf, (tooltip_x + padding, y_offset))
            y_offset += line_height
    
    def _draw_scrollbar(self, screen):
        """Vẽ thanh cuộn"""
        scrollbar_x = 365
        scrollbar_track_y = 305
        scrollbar_track_height = 420
        scrollbar_width = 10
        scrollbar_handle_height = 60
        
        # Draw track
        track_rect = pygame.Rect(scrollbar_x, scrollbar_track_y, scrollbar_width, scrollbar_track_height)
        pygame.draw.rect(screen, (30, 30, 50), track_rect, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 100), track_rect, 1, border_radius=5)
        
        # Draw handle
        scrollbar_rect = self._get_scrollbar_rect()
        if scrollbar_rect:
            # Glow if dragging
            if self.scrollbar_dragging:
                glow_rect = scrollbar_rect.inflate(4, 4)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*self.ACCENT_COLOR, 100), 
                               (0, 0, glow_rect.width, glow_rect.height), border_radius=5)
                screen.blit(glow_surf, glow_rect.topleft)
            
            pygame.draw.rect(screen, self.ACCENT_COLOR, scrollbar_rect, border_radius=5)
            pygame.draw.rect(screen, (150, 200, 255), scrollbar_rect, 1, border_radius=5)
    
    def _save_equipment_to_profile(self):
        """Lưu equipment vào profile của user hiện tại"""
        if not hasattr(self.game, 'current_user') or not self.game.current_user:
            print("[EQUIPMENT_SCREEN] Không có user để lưu")
            return
        
        try:
            from ma_nguon.core import profile_manager
            
            # Load current profile
            profile = profile_manager.load_profile(self.game.current_user)
            
            # Save inventory (kho trang bị)
            inventory = {}
            for eq in self.equipment_manager.get_all_equipment():
                inventory[eq.name] = inventory.get(eq.name, 0) + 1
            profile['equipment_inventory'] = inventory
            
            # Save all character equipment
            character_equipment = self.equipment_manager.save_all_character_equipment()
            profile['character_equipment'] = character_equipment
            
            # Save profile
            profile_manager.save_profile(self.game.current_user, profile)
            print(f"[EQUIPMENT_SCREEN] ✓ Đã lưu trang bị cho {self.game.current_user}")
            print(f"[EQUIPMENT_SCREEN] Inventory: {len(inventory)} items")
            print(f"[EQUIPMENT_SCREEN] Character equipment saved: {character_equipment}")
        except Exception as e:
            print(f"[EQUIPMENT_SCREEN] ✗ Lỗi khi lưu trang bị: {e}")
            import traceback
            traceback.print_exc()
