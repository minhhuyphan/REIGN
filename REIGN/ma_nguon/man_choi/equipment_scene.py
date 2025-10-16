import pygame
from ma_nguon.doi_tuong.equipment import Equipment, EquipmentManager, EquipmentEffectManager
from ma_nguon.giao_dien.equipment_ui import EquipmentUI
from ma_nguon.core.equipment_manager_global import get_global_equipment_manager
from ma_nguon.core.character_data import get_all_characters


class EquipmentScene:
    """Màn hình quản lý trang bị"""
    
    def __init__(self, game, player=None):
        self.game = game
        
        # Nếu không có player, tạo dummy player để preview
        if player is None:
            from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
            import os
            folder_nv = os.path.join("Tai_nguyen", "hinh_anh", "nhan_vat", "chien_binh")
            self.player = Character(100, 300, folder_nv, color=(0,255,0))
            self.is_preview_mode = True
        else:
            self.player = player
            self.is_preview_mode = False
        
        # Font
        try:
            self.font = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 40)
        except:
            self.font = pygame.font.Font(None, 40)
        
        # Equipment Manager
        if not hasattr(self.game, 'equipment_manager'):
            self.game.equipment_manager = EquipmentManager()
        self.equipment_manager = self.game.equipment_manager
        
        # Effect Manager
        if not hasattr(self.game, 'equipment_effect_manager'):
            self.game.equipment_effect_manager = EquipmentEffectManager()
        self.effect_manager = self.game.equipment_effect_manager
        
        # Equipment UI
        self.equipment_ui = EquipmentUI(self.game.WIDTH, self.game.HEIGHT)
        self.equipment_ui.show()
        
        # Global equipment manager
        self.global_eq_manager = get_global_equipment_manager()
        
        # Current selected character ID
        self.current_character_id = "chien_binh"  # Default
        
        # Set callback for equipment changes
        self.equipment_ui.on_equipment_change = self._on_equipment_change
        
        # Character selector - Load from central character data
        self.character_selector_visible = False
        self.available_characters = get_all_characters()
        
        # Test: Thêm một số items vào inventory để test
        if len(self.equipment_manager.inventory) == 0:
            self.equipment_manager.add_to_inventory("cung_bang_lam")
            self.equipment_manager.add_to_inventory("kiem_rong")
            self.equipment_manager.add_to_inventory("giap_anh_sang")
            self.equipment_manager.add_to_inventory("giay_thien_than")
        
        # Background
        try:
            self.background = pygame.image.load("Tai_nguyen/hinh_anh/giao_dien/bg.png")
            self.background = pygame.transform.scale(self.background, (self.game.WIDTH, self.game.HEIGHT))
        except:
            self.background = None
    
    def _on_equipment_change(self, character_id, equipment_type, equipment_id):
        """Callback khi trang bị thay đổi"""
        self.global_eq_manager.set_equipment(character_id, equipment_type, equipment_id)
        print(f"[Equipment] Saved: {character_id} - {equipment_type} - {equipment_id}")
    
    def handle_event(self, event):
        """Xử lý sự kiện"""
        # Xử lý character selector nếu đang mở
        if self.character_selector_visible:
            if self._handle_character_selector_event(event):
                return
        
        # Xử lý nút chọn nhân vật
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            select_char_btn = self._get_select_character_button_rect()
            if select_char_btn.collidepoint(mouse_pos):
                self.character_selector_visible = True
                return
        
        # Xử lý UI trước
        if self.equipment_ui.handle_event(event, self.equipment_manager, self.player, self.current_character_id):
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Quay lại menu
                self.game.change_scene("menu")
    
    def update(self):
        """Cập nhật trạng thái"""
        # Update equipment effects nếu có
        dt = self.game.clock.get_time() / 1000.0
        self.effect_manager.update(dt)
    
    def draw(self, screen):
        """Vẽ màn hình"""
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((20, 20, 40))
        
        # Draw title
        title = self.font.render("TRANG BỊ", True, (255, 215, 0))
        screen.blit(title, (self.game.WIDTH // 2 - title.get_width() // 2, 20))
        
        # Draw preview mode warning
        if self.is_preview_mode:
            try:
                warn_font = pygame.font.Font("Tai_nguon/font/Fz-Futurik.ttf", 20)
            except:
                warn_font = pygame.font.Font(None, 20)
            warning = warn_font.render("(Chế độ xem trước - Chọn nhân vật để áp dụng trang bị)", True, (255, 200, 100))
            screen.blit(warning, (self.game.WIDTH // 2 - warning.get_width() // 2, 70))
        
        # Draw equipment UI
        self.equipment_ui.draw(screen, self.equipment_manager)
        
        # Draw select character button
        self._draw_select_character_button(screen)
        
        # Draw player stats
        if self.player:
            self._draw_player_stats(screen)
        
        # Draw character selector if visible
        if self.character_selector_visible:
            self._draw_character_selector(screen)
        
        # Draw hint
        try:
            hint_font = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 18)
        except:
            hint_font = pygame.font.Font(None, 18)
        
        hint = hint_font.render("Nhấn ESC để quay lại menu", True, (200, 200, 200))
        screen.blit(hint, (10, self.game.HEIGHT - 30))
    
    def _draw_player_stats(self, screen):
        """Vẽ thông tin stats của player"""
        try:
            stats_font = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 20)
        except:
            stats_font = pygame.font.Font(None, 20)
        
        # Vẽ khung stats bên phải trên
        stats_x = self.game.WIDTH - 320
        stats_y = 100
        stats_width = 300
        stats_height = 200
        
        # Background
        stats_surface = pygame.Surface((stats_width, stats_height), pygame.SRCALPHA)
        stats_surface.fill((30, 30, 50, 200))
        pygame.draw.rect(stats_surface, (100, 100, 120), (0, 0, stats_width, stats_height), 2)
        
        # Title
        title = stats_font.render("Chỉ Số Nhân Vật", True, (255, 215, 0))
        stats_surface.blit(title, (stats_width // 2 - title.get_width() // 2, 10))
        
        # Stats
        y_offset = 45
        line_height = 25
        
        stats_list = [
            ("HP", f"{int(self.player.hp)}/{int(self.player.max_hp)}"),
            ("Sát Thương", f"{int(self.player.damage)}"),
            ("Đá", f"{int(self.player.kick_damage)}"),
            ("Tốc Độ", f"{int(self.player.speed)}"),
            ("Phòng Thủ", f"{int(self.player.defense)}")
        ]
        
        for stat_name, stat_value in stats_list:
            # Label
            label = stats_font.render(f"{stat_name}:", True, (200, 200, 200))
            stats_surface.blit(label, (20, y_offset))
            
            # Value
            value = stats_font.render(stat_value, True, (100, 255, 100))
            stats_surface.blit(value, (stats_width - 100, y_offset))
            
            y_offset += line_height
        
        screen.blit(stats_surface, (stats_x, stats_y))
    
    def _get_select_character_button_rect(self):
        """Lấy rect của nút chọn nhân vật"""
        btn_width = 200
        btn_height = 50
        btn_x = self.game.WIDTH - 320
        btn_y = 320
        return pygame.Rect(btn_x, btn_y, btn_width, btn_height)
    
    def _draw_select_character_button(self, screen):
        """Vẽ nút chọn nhân vật"""
        btn_rect = self._get_select_character_button_rect()
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = btn_rect.collidepoint(mouse_pos)
        
        # Draw button
        color = (80, 150, 255) if is_hover else (50, 100, 200)
        pygame.draw.rect(screen, color, btn_rect)
        pygame.draw.rect(screen, (150, 150, 150), btn_rect, 2)
        
        # Draw text
        try:
            btn_font = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 22)
        except:
            btn_font = pygame.font.Font(None, 22)
        
        text = btn_font.render("Chọn Nhân Vật", True, (255, 255, 255))
        text_x = btn_rect.x + (btn_rect.width - text.get_width()) // 2
        text_y = btn_rect.y + (btn_rect.height - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))
    
    def _handle_character_selector_event(self, event):
        """Xử lý events của character selector"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.character_selector_visible = False
                return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check close button
            close_btn_rect = pygame.Rect(
                self.game.WIDTH // 2 + 350,
                self.game.HEIGHT // 2 - 250,
                30, 30
            )
            if close_btn_rect.collidepoint(mouse_pos):
                self.character_selector_visible = False
                return True
            
            # Check character cards
            selector_x = self.game.WIDTH // 2 - 400
            selector_y = self.game.HEIGHT // 2 - 200
            card_width = 150
            card_height = 220
            padding = 10
            
            for i, char_data in enumerate(self.available_characters):
                col = i % 5
                row = i // 5
                
                card_x = selector_x + 20 + col * (card_width + padding)
                card_y = selector_y + 60 + row * (card_height + padding)
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                
                if card_rect.collidepoint(mouse_pos):
                    self._select_character(char_data)
                    self.character_selector_visible = False
                    return True
        
        return False
    
    def _select_character(self, char_data):
        """Chọn nhân vật"""
        from ma_nguon.doi_tuong.nhan_vat.nhan_vat import Character
        
        # Gỡ tất cả trang bị khỏi player cũ
        if self.player:
            for eq_type in [Equipment.TYPE_WEAPON, Equipment.TYPE_ARMOR, Equipment.TYPE_BOOTS]:
                if self.equipment_manager.get_equipped_by_type(eq_type):
                    self.equipment_manager.unequip(eq_type, self.player)
        
        # Tạo player mới
        self.player = Character(
            100, 300,
            char_data["folder"],
            stats=char_data["stats"],
            color=(0, 255, 0)
        )
        self.is_preview_mode = False
        
        # Update current character ID
        self.current_character_id = char_data["id"]
        
        # Load and apply saved equipment for this character
        self.global_eq_manager.apply_equipment_to_character(
            self.player,
            self.current_character_id,
            self.equipment_manager
        )
        
        print(f"[Equipment] Đã chọn nhân vật: {char_data['name']} (ID: {char_data['id']})")

    
    def _draw_character_selector(self, screen):
        """Vẽ popup chọn nhân vật"""
        # Overlay
        overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Selector box
        selector_width = 800
        selector_height = 500
        selector_x = (self.game.WIDTH - selector_width) // 2
        selector_y = (self.game.HEIGHT - selector_height) // 2
        
        selector_surface = pygame.Surface((selector_width, selector_height))
        selector_surface.fill((30, 30, 50))
        pygame.draw.rect(selector_surface, (200, 200, 200), (0, 0, selector_width, selector_height), 3)
        
        # Title
        try:
            title_font = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 32)
            char_font = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 18)
        except:
            title_font = pygame.font.Font(None, 32)
            char_font = pygame.font.Font(None, 18)
        
        title = title_font.render("CHỌN NHÂN VẬT", True, (255, 215, 0))
        selector_surface.blit(title, (selector_width // 2 - title.get_width() // 2, 15))
        
        # Close button
        close_btn = title_font.render("X", True, (255, 100, 100))
        selector_surface.blit(close_btn, (selector_width - 35, 10))
        
        # Character cards
        card_width = 150
        card_height = 220
        padding = 10
        
        for i, char_data in enumerate(self.available_characters):
            col = i % 5
            row = i // 5
            
            card_x = 20 + col * (card_width + padding)
            card_y = 60 + row * (card_height + padding)
            
            # Card background
            mouse_pos = pygame.mouse.get_pos()
            # Adjust mouse pos relative to selector surface
            rel_mouse_x = mouse_pos[0] - selector_x
            rel_mouse_y = mouse_pos[1] - selector_y
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            is_hover = card_rect.collidepoint(rel_mouse_x, rel_mouse_y)
            
            card_color = (70, 70, 100) if is_hover else (50, 50, 80)
            pygame.draw.rect(selector_surface, card_color, card_rect)
            pygame.draw.rect(selector_surface, (100, 100, 120), card_rect, 2)
            
            # Character preview image
            try:
                preview_path = f"{char_data['folder']}/dung_yen/0.png"
                preview_img = pygame.image.load(preview_path).convert_alpha()
                # Scale to fit card
                preview_img = pygame.transform.scale(preview_img, (100, 120))
                img_x = card_x + (card_width - 100) // 2
                img_y = card_y + 10
                selector_surface.blit(preview_img, (img_x, img_y))
            except:
                # Placeholder if image not found
                placeholder = pygame.Surface((100, 120))
                placeholder.fill((100, 100, 100))
                selector_surface.blit(placeholder, (card_x + 25, card_y + 10))
            
            # Character name
            name_text = char_font.render(char_data["name"], True, (255, 255, 200))
            name_x = card_x + (card_width - name_text.get_width()) // 2
            selector_surface.blit(name_text, (name_x, card_y + 140))
            
            # Stats preview
            stats_y = card_y + 165
            stats_font_small = pygame.font.Font(None, 16)
            
            hp_text = stats_font_small.render(f"HP: {char_data['stats']['hp']}", True, (200, 200, 200))
            selector_surface.blit(hp_text, (card_x + 10, stats_y))
            
            dmg_text = stats_font_small.render(f"DMG: {char_data['stats']['damage']}", True, (200, 200, 200))
            selector_surface.blit(dmg_text, (card_x + 10, stats_y + 18))
            
            spd_text = stats_font_small.render(f"SPD: {char_data['stats']['speed']}", True, (200, 200, 200))
            selector_surface.blit(spd_text, (card_x + 10, stats_y + 36))
        
        screen.blit(selector_surface, (selector_x, selector_y))
