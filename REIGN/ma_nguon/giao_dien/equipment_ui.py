import pygame
import os
from ma_nguon.doi_tuong.equipment import Equipment, EquipmentManager, EquipmentEffectManager


class EquipmentUI:
    """UI hiển thị và quản lý trang bị"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Callback khi equipment thay đổi
        self.on_equipment_change = None  # Function(character_id, eq_type, eq_id)
        
        # Font
        try:
            self.font_title = pygame.font.Font("Tai_nguyen/font/Fz-Donsky.ttf", 28)
            self.font_normal = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 18)
            self.font_small = pygame.font.Font("Tai_nguyen/font/Fz-Futurik.ttf", 14)
        except:
            self.font_title = pygame.font.Font(None, 28)
            self.font_normal = pygame.font.Font(None, 18)
            self.font_small = pygame.font.Font(None, 14)
        
        # Trạng thái hiển thị
        self.visible = False
        
        # Kích thước và vị trí UI
        self.ui_width = 700
        self.ui_height = 500
        self.ui_x = (screen_width - self.ui_width) // 2
        self.ui_y = (screen_height - self.ui_height) // 2
        
        # Kích thước slot
        self.slot_size = 70
        self.slot_padding = 10
        
        # Vùng Equipment Slots (bên trái)
        self.equip_area_x = self.ui_x + 20
        self.equip_area_y = self.ui_y + 60
        self.equip_area_width = 200
        
        # Vùng Inventory (bên phải)
        self.inventory_area_x = self.ui_x + 240
        self.inventory_area_y = self.ui_y + 60
        self.inventory_area_width = 440
        self.inventory_area_height = 400
        
        # Số cột trong inventory
        self.inventory_cols = 5
        
        # Item được chọn
        self.selected_item = None
        self.selected_from = None  # "inventory" hoặc "equipped"
        
        # Tooltip
        self.tooltip_item = None
        self.tooltip_pos = (0, 0)
    
    def toggle(self):
        """Bật/tắt hiển thị UI"""
        self.visible = not self.visible
    
    def show(self):
        """Hiển thị UI"""
        self.visible = True
    
    def hide(self):
        """Ẩn UI"""
        self.visible = False
    
    def handle_event(self, event, equipment_manager, character, character_id=None):
        """Xử lý sự kiện chuột và bàn phím"""
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                self.hide()
                return True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Kiểm tra click vào nút đóng
            close_btn_rect = pygame.Rect(
                self.ui_x + self.ui_width - 40,
                self.ui_y + 10,
                30, 30
            )
            if close_btn_rect.collidepoint(mouse_pos):
                self.hide()
                return True
            
            # Kiểm tra click vào equipped slots
            equipped_click = self._check_equipped_click(mouse_pos, equipment_manager, character, character_id)
            if equipped_click:
                return True
            
            # Kiểm tra click vào inventory
            inventory_click = self._check_inventory_click(mouse_pos, equipment_manager, character, character_id)
            if inventory_click:
                return True
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self._update_tooltip(mouse_pos, equipment_manager)
        
        return False
    
    def _check_equipped_click(self, mouse_pos, equipment_manager, character, character_id=None):
        """Kiểm tra click vào equipped slots"""
        slot_types = [Equipment.TYPE_WEAPON, Equipment.TYPE_ARMOR, Equipment.TYPE_BOOTS]
        
        for i, slot_type in enumerate(slot_types):
            slot_x = self.equip_area_x
            slot_y = self.equip_area_y + i * (self.slot_size + self.slot_padding)
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            if slot_rect.collidepoint(mouse_pos):
                equipment = equipment_manager.get_equipped_by_type(slot_type)
                if equipment:
                    # Click vào equipped item -> unequip
                    equipment_manager.unequip(slot_type, character)
                    
                    # Notify callback
                    if self.on_equipment_change and character_id:
                        self.on_equipment_change(character_id, slot_type, None)
                return True
        
        return False
    
    def _check_inventory_click(self, mouse_pos, equipment_manager, character, character_id=None):
        """Kiểm tra click vào inventory"""
        for i, item in enumerate(equipment_manager.inventory):
            row = i // self.inventory_cols
            col = i % self.inventory_cols
            
            slot_x = self.inventory_area_x + col * (self.slot_size + self.slot_padding)
            slot_y = self.inventory_area_y + row * (self.slot_size + self.slot_padding)
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            if slot_rect.collidepoint(mouse_pos):
                # Click vào inventory item -> equip
                equipment_manager.equip(item, character)
                
                # Notify callback
                if self.on_equipment_change and character_id:
                    self.on_equipment_change(character_id, item.type, item.id)
                return True
        
        return False
    
    def _update_tooltip(self, mouse_pos, equipment_manager):
        """Cập nhật tooltip khi hover"""
        self.tooltip_item = None
        
        # Check equipped slots
        slot_types = [Equipment.TYPE_WEAPON, Equipment.TYPE_ARMOR, Equipment.TYPE_BOOTS]
        for i, slot_type in enumerate(slot_types):
            slot_x = self.equip_area_x
            slot_y = self.equip_area_y + i * (self.slot_size + self.slot_padding)
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            if slot_rect.collidepoint(mouse_pos):
                equipment = equipment_manager.get_equipped_by_type(slot_type)
                if equipment:
                    self.tooltip_item = equipment
                    self.tooltip_pos = mouse_pos
                return
        
        # Check inventory
        for i, item in enumerate(equipment_manager.inventory):
            row = i // self.inventory_cols
            col = i % self.inventory_cols
            
            slot_x = self.inventory_area_x + col * (self.slot_size + self.slot_padding)
            slot_y = self.inventory_area_y + row * (self.slot_size + self.slot_padding)
            slot_rect = pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size)
            
            if slot_rect.collidepoint(mouse_pos):
                self.tooltip_item = item
                self.tooltip_pos = mouse_pos
                return
    
    def draw(self, screen, equipment_manager):
        """Vẽ UI"""
        if not self.visible:
            return
        
        # Vẽ overlay tối
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Vẽ khung UI chính
        ui_surface = pygame.Surface((self.ui_width, self.ui_height))
        ui_surface.fill((30, 30, 50))
        pygame.draw.rect(ui_surface, (200, 200, 200), (0, 0, self.ui_width, self.ui_height), 3)
        
        # Tiêu đề
        title = self.font_title.render("TRANG BỊ", True, (255, 215, 0))
        ui_surface.blit(title, (self.ui_width // 2 - title.get_width() // 2, 15))
        
        # Nút đóng
        close_btn = self.font_title.render("X", True, (255, 100, 100))
        ui_surface.blit(close_btn, (self.ui_width - 35, 10))
        
        # Vẽ vùng Equipment Slots (bên trái)
        self._draw_equipment_slots(ui_surface, equipment_manager)
        
        # Vẽ vùng Inventory (bên phải)
        self._draw_inventory(ui_surface, equipment_manager)
        
        # Vẽ hướng dẫn
        help_text = self.font_small.render("Click vào item trong kho để trang bị | Click vào item đã trang bị để gỡ", True, (200, 200, 200))
        ui_surface.blit(help_text, (20, self.ui_height - 30))
        
        screen.blit(ui_surface, (self.ui_x, self.ui_y))
        
        # Vẽ tooltip
        if self.tooltip_item:
            self._draw_tooltip(screen)
    
    def _draw_equipment_slots(self, surface, equipment_manager):
        """Vẽ các slot trang bị đã mặc"""
        # Tiêu đề
        label = self.font_normal.render("Đang Trang Bị:", True, (255, 255, 255))
        surface.blit(label, (self.equip_area_x - self.ui_x, self.equip_area_y - self.ui_y - 30))
        
        slot_types = [
            (Equipment.TYPE_WEAPON, "Vũ Khí"),
            (Equipment.TYPE_ARMOR, "Giáp"),
            (Equipment.TYPE_BOOTS, "Giày")
        ]
        
        for i, (slot_type, slot_name) in enumerate(slot_types):
            slot_x = self.equip_area_x - self.ui_x
            slot_y = self.equip_area_y - self.ui_y + i * (self.slot_size + self.slot_padding)
            
            # Vẽ slot
            slot_color = (60, 60, 80)
            pygame.draw.rect(surface, slot_color, (slot_x, slot_y, self.slot_size, self.slot_size))
            pygame.draw.rect(surface, (100, 100, 120), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            
            # Vẽ label
            label_text = self.font_small.render(slot_name, True, (180, 180, 180))
            surface.blit(label_text, (slot_x + self.slot_size + 10, slot_y + 5))
            
            # Vẽ item nếu có
            equipment = equipment_manager.get_equipped_by_type(slot_type)
            if equipment:
                # Vẽ icon
                icon_x = slot_x + (self.slot_size - 60) // 2
                icon_y = slot_y + (self.slot_size - 60) // 2
                icon = pygame.transform.scale(equipment.image, (60, 60))
                surface.blit(icon, (icon_x, icon_y))
                
                # Vẽ tên (rút gọn)
                name_text = self.font_small.render(equipment.name[:10], True, (255, 255, 200))
                surface.blit(name_text, (slot_x + self.slot_size + 10, slot_y + 25))
    
    def _draw_inventory(self, surface, equipment_manager):
        """Vẽ kho đồ"""
        # Tiêu đề
        label = self.font_normal.render("Kho Đồ:", True, (255, 255, 255))
        surface.blit(label, (self.inventory_area_x - self.ui_x, self.inventory_area_y - self.ui_y - 30))
        
        # Vẽ background
        inv_bg_rect = pygame.Rect(
            self.inventory_area_x - self.ui_x,
            self.inventory_area_y - self.ui_y,
            self.inventory_area_width,
            self.inventory_area_height
        )
        pygame.draw.rect(surface, (40, 40, 60), inv_bg_rect)
        pygame.draw.rect(surface, (80, 80, 100), inv_bg_rect, 2)
        
        # Vẽ các item
        for i, item in enumerate(equipment_manager.inventory):
            row = i // self.inventory_cols
            col = i % self.inventory_cols
            
            slot_x = self.inventory_area_x - self.ui_x + col * (self.slot_size + self.slot_padding)
            slot_y = self.inventory_area_y - self.ui_y + row * (self.slot_size + self.slot_padding)
            
            # Vẽ slot
            slot_color = (60, 60, 80)
            pygame.draw.rect(surface, slot_color, (slot_x, slot_y, self.slot_size, self.slot_size))
            pygame.draw.rect(surface, (100, 100, 120), (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            
            # Vẽ icon
            icon_x = slot_x + (self.slot_size - 60) // 2
            icon_y = slot_y + (self.slot_size - 60) // 2
            icon = pygame.transform.scale(item.image, (60, 60))
            surface.blit(icon, (icon_x, icon_y))
    
    def _draw_tooltip(self, screen):
        """Vẽ tooltip chi tiết item"""
        if not self.tooltip_item:
            return
        
        item = self.tooltip_item
        
        # Tạo nội dung tooltip
        lines = [
            f"{item.name}",
            f"Loại: {self._get_type_name(item.type)}",
            ""
        ]
        
        # Thêm stats
        if item.stats:
            lines.append("Chỉ số:")
            for stat, value in item.stats.items():
                stat_name = self._get_stat_name(stat)
                lines.append(f"  +{value} {stat_name}")
        
        # Thêm special effect
        if item.special_effect and "description" in item.special_effect:
            lines.append("")
            lines.append("Hiệu ứng đặc biệt:")
            lines.append(f"  {item.special_effect['description']}")
        
        # Tính kích thước tooltip
        line_height = 20
        padding = 10
        max_width = max([self.font_small.size(line)[0] for line in lines]) + padding * 2
        tooltip_height = len(lines) * line_height + padding * 2
        
        # Vị trí tooltip (tránh ra ngoài màn hình)
        tooltip_x = self.tooltip_pos[0] + 15
        tooltip_y = self.tooltip_pos[1] + 15
        
        if tooltip_x + max_width > self.screen_width:
            tooltip_x = self.tooltip_pos[0] - max_width - 15
        if tooltip_y + tooltip_height > self.screen_height:
            tooltip_y = self.tooltip_pos[1] - tooltip_height - 15
        
        # Vẽ background
        tooltip_surface = pygame.Surface((max_width, tooltip_height), pygame.SRCALPHA)
        tooltip_surface.fill((20, 20, 30, 240))
        pygame.draw.rect(tooltip_surface, (200, 200, 200), (0, 0, max_width, tooltip_height), 2)
        
        # Vẽ text
        y_offset = padding
        for i, line in enumerate(lines):
            if i == 0:  # Tên item
                color = (255, 215, 0)
            elif line.startswith("  "):  # Sub-items
                color = (180, 255, 180)
            else:
                color = (220, 220, 220)
            
            text = self.font_small.render(line, True, color)
            tooltip_surface.blit(text, (padding, y_offset))
            y_offset += line_height
        
        screen.blit(tooltip_surface, (tooltip_x, tooltip_y))
    
    def _get_type_name(self, item_type):
        """Lấy tên hiển thị của loại trang bị"""
        type_names = {
            Equipment.TYPE_WEAPON: "Vũ Khí",
            Equipment.TYPE_ARMOR: "Giáp",
            Equipment.TYPE_BOOTS: "Giày"
        }
        return type_names.get(item_type, "Không rõ")
    
    def _get_stat_name(self, stat):
        """Lấy tên hiển thị của chỉ số"""
        stat_names = {
            "damage": "Sát Thương",
            "kick_damage": "Sát Thương Đá",
            "hp": "Máu",
            "speed": "Tốc Độ",
            "defense": "Phòng Thủ"
        }
        return stat_names.get(stat, stat)
