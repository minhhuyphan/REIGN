import pygame
import os

class Equipment:
    """Lớp đại diện cho một món trang bị"""
    
    # Định nghĩa các loại trang bị
    TYPE_WEAPON = "weapon"  # Công
    TYPE_ARMOR = "armor"    # Thủ
    TYPE_BOOTS = "boots"    # Tốc độ
    
    def __init__(self, item_id, name, item_type, image_path, stats, special_effect=None):
        """
        Args:
            item_id: ID duy nhất của item
            name: Tên hiển thị
            item_type: Loại trang bị (weapon/armor/boots)
            image_path: Đường dẫn đến hình ảnh
            stats: Dict chứa các chỉ số tăng {"damage": 10, "hp": 50, ...}
            special_effect: Dict chứa hiệu ứng đặc biệt
        """
        self.id = item_id
        self.name = name
        self.type = item_type
        self.image_path = image_path
        self.stats = stats or {}
        self.special_effect = special_effect or {}
        
        # Load hình ảnh
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
        except:
            # Tạo placeholder nếu không load được
            self.image = pygame.Surface((64, 64))
            self.image.fill((100, 100, 100))
    
    def apply_to_character(self, character):
        """Áp dụng stats của trang bị lên nhân vật"""
        if "damage" in self.stats:
            character.damage += self.stats["damage"]
        if "kick_damage" in self.stats:
            character.kick_damage += self.stats["kick_damage"]
        if "hp" in self.stats:
            character.max_hp += self.stats["hp"]
            character.hp += self.stats["hp"]  # Cộng luôn vào HP hiện tại
        if "speed" in self.stats:
            character.speed += self.stats["speed"]
        if "defense" in self.stats:
            character.defense += self.stats["defense"]
        
        # Apply special effects
        if self.special_effect:
            effect_type = self.special_effect.get("type")
            
            # Set revive flag if armor has revive effect
            if effect_type == "revive" and self.type == Equipment.TYPE_ARMOR:
                character.equipped_armor_has_revive = True
                print(f"[Equipment] {self.name} revive effect enabled!")
    
    def remove_from_character(self, character):
        """Gỡ bỏ stats của trang bị khỏi nhân vật"""
        if "damage" in self.stats:
            character.damage -= self.stats["damage"]
        if "kick_damage" in self.stats:
            character.kick_damage -= self.stats["kick_damage"]
        if "hp" in self.stats:
            character.max_hp -= self.stats["hp"]
            character.hp = min(character.hp, character.max_hp)  # Điều chỉnh HP
        if "speed" in self.stats:
            character.speed -= self.stats["speed"]
        if "defense" in self.stats:
            character.defense -= self.stats["defense"]
        
        # Remove special effects
        if self.special_effect:
            effect_type = self.special_effect.get("type")
            
            # Remove revive flag if armor had revive effect
            if effect_type == "revive" and self.type == Equipment.TYPE_ARMOR:
                character.equipped_armor_has_revive = False
                print(f"[Equipment] {self.name} revive effect disabled!")


class EquipmentManager:
    """Quản lý kho đồ và trang bị của nhân vật"""
    
    def __init__(self):
        # Kho đồ - danh sách tất cả items đang có
        self.inventory = []
        
        # Trang bị đang mặc - dict {type: Equipment}
        self.equipped = {
            Equipment.TYPE_WEAPON: None,
            Equipment.TYPE_ARMOR: None,
            Equipment.TYPE_BOOTS: None
        }
        
        # Khởi tạo danh sách tất cả equipment có sẵn
        self._init_all_equipment()
    
    def _init_all_equipment(self):
        """Khởi tạo tất cả các loại trang bị trong game"""
        self.all_equipment = {
            # Vũ khí (Công)
            "cung_bang_lam": Equipment(
                item_id="cung_bang_lam",
                name="Cung Băng Lam",
                item_type=Equipment.TYPE_WEAPON,
                image_path="Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/cung_bang_lam.png",
                stats={"damage": 8},
                special_effect={
                    "type": "slow",
                    "description": "Làm chậm kẻ địch",
                    "slow_factor": 0.5,  # Giảm 50% tốc độ
                    "duration": 3  # 3 giây
                }
            ),
            "kiem_rong": Equipment(
                item_id="kiem_rong",
                name="Kiếm Rồng",
                item_type=Equipment.TYPE_WEAPON,
                image_path="Tai_nguyen/hinh_anh/trang_bi/trang_bi_cong/kiem_rong.png",
                stats={"damage": 10},
                special_effect={
                    "type": "burn",
                    "description": "Thiêu đốt 1 HP/giây trong 30s",
                    "damage_per_sec": 1,
                    "duration": 30
                }
            ),
            
            # Giáp (Thủ)
            "giap_anh_sang": Equipment(
                item_id="giap_anh_sang",
                name="Giáp Ánh Sáng",
                item_type=Equipment.TYPE_ARMOR,
                image_path="Tai_nguyen/hinh_anh/trang_bi/trang_bi_thu/giap_anh_sang.png",
                stats={"hp": 200},
                special_effect={
                    "type": "revive",
                    "description": "Hồi sinh với 50% HP tối đa",
                    "revive_hp_percent": 0.5,
                    "cooldown": 120  # 120 giây cooldown
                }
            ),
            
            # Giày (Tốc độ)
            "giay_thien_than": Equipment(
                item_id="giay_thien_than",
                name="Giày Thiên Thần",
                item_type=Equipment.TYPE_BOOTS,
                image_path="Tai_nguyen/hinh_anh/trang_bi/trang_bi_toc_chay/giay_thien_than.png",
                stats={"speed": 2, "hp": 50},
                special_effect={
                    "type": "speed_boost",
                    "description": "Tăng tốc độ di chuyển"
                }
            )
        }
    
    def add_to_inventory(self, equipment_id):
        """Thêm trang bị vào kho"""
        if equipment_id in self.all_equipment:
            equipment = self.all_equipment[equipment_id]
            self.inventory.append(equipment)
            return True
        return False
    
    def equip(self, equipment, character):
        """Trang bị một item lên nhân vật"""
        if equipment not in self.inventory:
            return False
        
        # Gỡ trang bị cũ nếu có
        old_equipment = self.equipped[equipment.type]
        if old_equipment:
            old_equipment.remove_from_character(character)
            self.inventory.append(old_equipment)
        
        # Mặc trang bị mới
        self.equipped[equipment.type] = equipment
        self.inventory.remove(equipment)
        equipment.apply_to_character(character)
        return True
    
    def unequip(self, equipment_type, character):
        """Gỡ trang bị ra khỏi nhân vật"""
        equipment = self.equipped[equipment_type]
        if equipment:
            equipment.remove_from_character(character)
            self.inventory.append(equipment)
            self.equipped[equipment_type] = None
            return True
        return False
    
    def get_equipped_by_type(self, equipment_type):
        """Lấy trang bị đang mặc theo loại"""
        return self.equipped.get(equipment_type)


class EquipmentEffectManager:
    """Quản lý các hiệu ứng đặc biệt từ trang bị"""
    
    def __init__(self):
        # Danh sách các effect đang active
        self.active_effects = []
        # Cooldowns cho các effect
        self.cooldowns = {}
    
    def add_effect(self, effect_type, target, params):
        """Thêm một effect mới"""
        effect = {
            "type": effect_type,
            "target": target,
            "params": params,
            "start_time": pygame.time.get_ticks()
        }
        self.active_effects.append(effect)
    
    def update(self, dt):
        """Cập nhật tất cả effects"""
        current_time = pygame.time.get_ticks()
        remaining_effects = []
        
        for effect in self.active_effects:
            elapsed = (current_time - effect["start_time"]) / 1000.0
            
            if effect["type"] == "burn":
                # Áp dụng burn damage
                duration = effect["params"].get("duration", 0)
                if elapsed < duration:
                    # Burn mỗi giây
                    if int(elapsed) > int(elapsed - dt):
                        damage = effect["params"].get("damage_per_sec", 1)
                        effect["target"].hp -= damage
                    remaining_effects.append(effect)
            
            elif effect["type"] == "slow":
                # Áp dụng slow
                duration = effect["params"].get("duration", 0)
                if elapsed < duration:
                    remaining_effects.append(effect)
                else:
                    # Hết hiệu ứng slow, khôi phục tốc độ
                    if hasattr(effect["target"], "speed_modifier"):
                        effect["target"].speed_modifier = 1.0
        
        self.active_effects = remaining_effects
    
    def apply_slow(self, target, slow_factor, duration):
        """Áp dụng hiệu ứng làm chậm"""
        if not hasattr(target, "speed_modifier"):
            target.speed_modifier = 1.0
        target.speed_modifier = slow_factor
        
        self.add_effect("slow", target, {
            "slow_factor": slow_factor,
            "duration": duration
        })
    
    def apply_burn(self, target, damage_per_sec, duration):
        """Áp dụng hiệu ứng thiêu đốt"""
        self.add_effect("burn", target, {
            "damage_per_sec": damage_per_sec,
            "duration": duration
        })
    
    def can_revive(self, equipment_id):
        """Kiểm tra xem có thể hồi sinh không (cooldown)"""
        current_time = pygame.time.get_ticks()
        if equipment_id in self.cooldowns:
            if current_time - self.cooldowns[equipment_id] < 120000:  # 120s cooldown
                return False
        return True
    
    def trigger_revive(self, character, equipment_id):
        """Kích hoạt hồi sinh"""
        if self.can_revive(equipment_id):
            character.hp = int(character.max_hp * 0.5)
            character.dead = False
            self.cooldowns[equipment_id] = pygame.time.get_ticks()
            return True
        return False
