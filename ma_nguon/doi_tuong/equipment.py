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
            full_path = os.path.join("Tai_nguyen", "hinh_anh", "trang_bi", self.image_path)
            self.image = pygame.image.load(full_path)
            # Scale to standard size for UI
            self.image = pygame.transform.scale(self.image, (60, 60))
        except Exception as e:
            print(f"Không thể load hình ảnh trang bị {self.name}: {e}")
            # Create placeholder
            self.image = pygame.Surface((60, 60))
            self.image.fill((100, 100, 100))
            
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


class CungBangLam(Equipment):
    """Cung băng lãm - Trang bị công"""
    def __init__(self):
        super().__init__("Cung Băng Lãm", "attack", "trang_bi_cong/cung_bang_lam.png")
        self.attack_bonus = 8
        self.has_slow_effect = True


class KiemRong(Equipment):
    """Kiếm rồng - Trang bị công"""
    def __init__(self):
        super().__init__("Kiếm Rồng", "attack", "trang_bi_cong/kiem_rong.png")
        self.attack_bonus = 10
        self.has_burn_effect = True
        self.burn_damage = 1
        self.burn_duration = 30


class GiapAnhSang(Equipment):
    """Giáp ánh sáng - Trang bị thủ"""
    def __init__(self):
        super().__init__("Giáp Ánh Sáng", "defense", "trang_bi_thu/giap_anh_sang.png")
        self.hp_bonus = 200
        self.has_revive_effect = True
        self.revive_hp_percent = 50


class GiayThienThan(Equipment):
    """Giày thiên thần - Trang bị tốc độ"""
    def __init__(self):
        super().__init__("Giày Thiên Thần", "speed", "trang_bi_toc_chay/giay_thien_than.png")
        self.speed_bonus = 2
        self.hp_bonus = 50


class EquipmentManager:
    """Quản lý tất cả trang bị trong game"""
    def __init__(self):
        self.all_equipment = []
        # Track equipment for each character: {character_id: {slot_type: equipment_name}}
        self.character_equipment = {}
        self.initialize_equipment()
        
    def initialize_equipment(self):
        """Khởi tạo danh sách trang bị có sẵn"""
        self.all_equipment = [
            CungBangLam(),
            KiemRong(),
            GiapAnhSang(),
            GiayThienThan()
        ]
        
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
