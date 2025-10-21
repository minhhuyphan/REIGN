"""
Module quản lý trang bị (Equipment System)
Hỗ trợ 3 loại trang bị: Công (Attack), Thủ (Defense), Tốc độ (Speed)
"""

import pygame
import os

class Equipment:
    """Base class cho trang bị"""
    def __init__(self, name, equipment_type, image_path):
        self.name = name
        self.equipment_type = equipment_type  # 'attack', 'defense', 'speed'
        self.image_path = image_path
        self.image = None
        self.equipped_to = None  # Tên nhân vật đang trang bị
        self.load_image()
        
        # Stats bonuses
        self.attack_bonus = 0
        self.defense_bonus = 0
        self.hp_bonus = 0
        self.speed_bonus = 0
        
        # Special effects
        self.has_slow_effect = False
        self.has_burn_effect = False
        self.burn_damage = 0
        self.burn_duration = 0
        self.has_revive_effect = False
        self.revive_hp_percent = 0
        
    def load_image(self):
        """Load hình ảnh trang bị"""
        try:
            # Try lowercase first (tai_nguyen)
            full_path = os.path.join("tai_nguyen", "hinh_anh", "trang_bi", self.image_path)
            if not os.path.exists(full_path):
                # Try uppercase (Tai_nguyen)
                full_path = os.path.join("Tai_nguyen", "hinh_anh", "trang_bi", self.image_path)
            
            if os.path.exists(full_path):
                self.image = pygame.image.load(full_path).convert_alpha()
                # Scale to standard size for UI
                self.image = pygame.transform.scale(self.image, (60, 60))
                print(f"[EQUIPMENT] Loaded image for {self.name}: {full_path}")
            else:
                raise FileNotFoundError(f"Image not found: {self.image_path}")
        except Exception as e:
            print(f"[EQUIPMENT] Cannot load image for {self.name}: {e}")
            print(f"[EQUIPMENT] Tried path: {self.image_path}")
            # Create placeholder with rarity color
            self.image = self._create_placeholder_image()
    
    def _create_placeholder_image(self):
        """Tạo placeholder image khi không load được ảnh"""
        size = 60
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Background color based on type
        if self.equipment_type == "attack":
            bg_color = (200, 100, 100)
            icon = "⚔"
        elif self.equipment_type == "defense":
            bg_color = (100, 200, 100)
            icon = "🛡"
        elif self.equipment_type == "speed":
            bg_color = (100, 150, 255)
            icon = "⚡"
        else:
            bg_color = (150, 150, 150)
            icon = "?"
        
        # Draw background
        pygame.draw.rect(surface, bg_color, (0, 0, size, size), border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, size, size), 2, border_radius=8)
        
        # Draw icon text
        try:
            font = pygame.font.Font(None, 32)
            text = font.render(icon, True, (255, 255, 255))
            text_rect = text.get_rect(center=(size//2, size//2))
            surface.blit(text, text_rect)
        except:
            pass
        
        return surface
            
    def draw(self, surface, x, y):
        """Vẽ trang bị tại vị trí (x, y)"""
        if self.image:
            surface.blit(self.image, (x, y))
            
    def get_description(self):
        """Trả về mô tả trang bị"""
        desc = f"{self.name}\n"
        if self.attack_bonus > 0:
            desc += f"+{self.attack_bonus} Công\n"
        if self.defense_bonus > 0:
            desc += f"+{self.defense_bonus} Thủ\n"
        if self.hp_bonus > 0:
            desc += f"+{self.hp_bonus} HP\n"
        if self.speed_bonus > 0:
            desc += f"+{self.speed_bonus} Tốc độ\n"
        if self.has_slow_effect:
            desc += "Làm chậm địch\n"
        if self.has_burn_effect:
            desc += f"Thiêu đốt {self.burn_damage} máu/giây trong {self.burn_duration}s\n"
        if self.has_revive_effect:
            desc += f"Hồi sinh với {self.revive_hp_percent}% máu\n"
        return desc.strip()


class EquipmentManager:
    """Quản lý tất cả trang bị trong game"""
    def __init__(self):
        self.all_equipment = []
        # Track equipment for each character: {character_id: {slot_type: equipment_name}}
        self.character_equipment = {}
        self.profile_inventory = {}  # Track inventory from profile
        # Không cần initialize_equipment nữa vì sẽ load từ profile
        
    def load_inventory_from_profile(self, profile_inventory):
        """Load trang bị từ profile inventory (từ gacha)
        profile_inventory format: {item_name: count}
        """
        from ma_nguon.doi_tuong.items import EQUIPMENT_DATA
        
        self.profile_inventory = profile_inventory
        self.all_equipment = []  # Clear current
        
        # Create equipment objects từ inventory
        for item_name, count in profile_inventory.items():
            item_data = EQUIPMENT_DATA.get(item_name)
            if not item_data:
                continue
            
            # Create equipment với số lượng count
            for i in range(count):
                eq = self._create_equipment_from_data(item_name, item_data)
                if eq:
                    self.all_equipment.append(eq)
    
    def _create_equipment_from_data(self, item_name, item_data):
        """Tạo Equipment object từ EQUIPMENT_DATA"""
        eq_type = item_data.get("type", "attack")
        image_path = item_data.get("image_path", "")
        
        # image_path từ EQUIPMENT_DATA đã là đường dẫn tương đối từ trang_bi
        # VD: "trang_bi_vang/trang_bi_cong/kiem_rong.png"
        # Không cần cắt gì thêm, giữ nguyên
        
        print(f"[EQUIPMENT] Creating {item_name} with image_path: {image_path}")
        eq = Equipment(item_name, eq_type, image_path)
        # Preserve rarity for UI coloring and other logic
        eq.rarity = item_data.get("rarity", "common")

        # Set stats
        eq.attack_bonus = item_data.get("attack_bonus", 0)
        eq.hp_bonus = item_data.get("hp_bonus", 0)
        eq.speed_bonus = item_data.get("speed_bonus", 0)
        
        # Set special effects
        effects = item_data.get("effects", [])
        if "burn" in effects or "burn_area" in effects:
            eq.has_burn_effect = True
            eq.burn_damage = 2
            eq.burn_duration = 30
        if "slow" in effects or "freeze" in effects:
            eq.has_slow_effect = True
        if "revive" in effects:
            eq.has_revive_effect = True
            eq.revive_hp_percent = 50
        
        return eq
        
    def get_equipment_by_type(self, equipment_type):
        """Lấy danh sách trang bị theo loại"""
        return [eq for eq in self.all_equipment if eq.equipment_type == equipment_type]
        
    def get_all_equipment(self):
        """Lấy toàn bộ trang bị"""
        return self.all_equipment
        
    def get_available_equipment(self):
        """Lấy trang bị chưa được trang bị"""
        return [eq for eq in self.all_equipment if eq.equipped_to is None]
    
    def get_equipment_by_name(self, name):
        """Lấy equipment theo tên"""
        for eq in self.all_equipment:
            if eq.name == name:
                return eq
        return None
        
    def equip_to_character(self, equipment, character_id):
        """Trang bị cho nhân vật"""
        if equipment.equipped_to is None:
            equipment.equipped_to = character_id
            # Track in character_equipment dict
            if character_id not in self.character_equipment:
                self.character_equipment[character_id] = {}
            self.character_equipment[character_id][equipment.equipment_type] = equipment.name
            return True
        return False
        
    def unequip(self, equipment, character_id=None):
        """Gỡ trang bị"""
        old_char = equipment.equipped_to
        equipment.equipped_to = None
        # Remove from character_equipment tracking
        if old_char and old_char in self.character_equipment:
            if equipment.equipment_type in self.character_equipment[old_char]:
                del self.character_equipment[old_char][equipment.equipment_type]
    
    def get_character_equipment(self, character_id):
        """Lấy equipment hiện tại của character"""
        return self.character_equipment.get(character_id, {})
    
    def load_character_equipment(self, character_id, equipment_data):
        """Load equipment cho character từ saved data
        equipment_data format: {'attack': 'Cung Băng Lãm', 'defense': 'Giáp Ánh Sáng', ...}
        """
        # Clear current equipment for this character
        if character_id in self.character_equipment:
            for slot_type, eq_name in list(self.character_equipment[character_id].items()):
                eq = self.get_equipment_by_name(eq_name)
                if eq:
                    eq.equipped_to = None
        
        self.character_equipment[character_id] = {}
        
        # Load new equipment
        for slot_type, eq_name in equipment_data.items():
            if eq_name:
                eq = self.get_equipment_by_name(eq_name)
                if eq and eq.equipped_to is None:
                    eq.equipped_to = character_id
                    self.character_equipment[character_id][slot_type] = eq_name
    
    def save_all_character_equipment(self):
        """Export all character equipment để save vào profile"""
        return dict(self.character_equipment)


# Singleton instance
_equipment_manager = None

def get_equipment_manager():
    """Lấy instance của EquipmentManager"""
    global _equipment_manager
    if _equipment_manager is None:
        _equipment_manager = EquipmentManager()
    return _equipment_manager
