"""
Global Equipment Manager - Quản lý trang bị cho tất cả nhân vật
Lưu trang bị của mỗi nhân vật và áp dụng khi tạo character
"""

import json
import os


class GlobalEquipmentManager:
    """Quản lý trang bị global cho tất cả nhân vật"""
    
    def __init__(self):
        self.save_file = "du_lieu/save/character_equipment.json"
        self.character_equipment = {}  # {character_id: {"weapon": "kiem_rong", "armor": None, "boots": None}}
        self.load()
    
    def load(self):
        """Load equipment data từ file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    self.character_equipment = json.load(f)
                print(f"[GlobalEquipment] Đã load trang bị cho {len(self.character_equipment)} nhân vật")
            except Exception as e:
                print(f"[GlobalEquipment] Lỗi khi load: {e}")
                self.character_equipment = {}
        else:
            self.character_equipment = {}
    
    def save(self):
        """Save equipment data vào file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.character_equipment, f, ensure_ascii=False, indent=2)
            print(f"[GlobalEquipment] Đã lưu trang bị cho {len(self.character_equipment)} nhân vật")
        except Exception as e:
            print(f"[GlobalEquipment] Lỗi khi save: {e}")
    
    def set_equipment(self, character_id, equipment_type, equipment_id):
        """
        Lưu trang bị cho nhân vật
        
        Args:
            character_id: ID nhân vật (vd: "chien_binh", "ninja")
            equipment_type: Loại trang bị ("weapon", "armor", "boots")
            equipment_id: ID trang bị (vd: "kiem_rong", None nếu gỡ)
        """
        if character_id not in self.character_equipment:
            self.character_equipment[character_id] = {
                "weapon": None,
                "armor": None,
                "boots": None
            }
        
        self.character_equipment[character_id][equipment_type] = equipment_id
        self.save()
        print(f"[GlobalEquipment] {character_id}: {equipment_type} = {equipment_id}")
    
    def get_equipment(self, character_id, equipment_type):
        """
        Lấy trang bị của nhân vật
        
        Args:
            character_id: ID nhân vật
            equipment_type: Loại trang bị
            
        Returns:
            equipment_id hoặc None
        """
        if character_id not in self.character_equipment:
            return None
        return self.character_equipment[character_id].get(equipment_type)
    
    def get_all_equipment(self, character_id):
        """
        Lấy tất cả trang bị của nhân vật
        
        Args:
            character_id: ID nhân vật
            
        Returns:
            Dict {"weapon": id, "armor": id, "boots": id}
        """
        if character_id not in self.character_equipment:
            return {"weapon": None, "armor": None, "boots": None}
        return self.character_equipment[character_id].copy()
    
    def clear_character_equipment(self, character_id):
        """Xóa tất cả trang bị của nhân vật"""
        if character_id in self.character_equipment:
            self.character_equipment[character_id] = {
                "weapon": None,
                "armor": None,
                "boots": None
            }
            self.save()
    
    def apply_equipment_to_character(self, character, character_id, equipment_manager):
        """
        Áp dụng trang bị đã lưu lên nhân vật
        
        Args:
            character: Character instance
            character_id: ID nhân vật
            equipment_manager: EquipmentManager instance
        """
        from ma_nguon.doi_tuong.equipment import Equipment
        
        equipped = self.get_all_equipment(character_id)
        
        print(f"[GlobalEquipment] Áp dụng trang bị cho {character_id}:")
        
        for eq_type in ["weapon", "armor", "boots"]:
            eq_id = equipped.get(eq_type)
            if eq_id:
                # Lấy equipment từ all_equipment
                if eq_id in equipment_manager.all_equipment:
                    equipment = equipment_manager.all_equipment[eq_id]
                    
                    # Add to inventory if not already there
                    if equipment not in equipment_manager.inventory:
                        equipment_manager.inventory.append(equipment)
                    
                    # Equip it through the equipment manager (this will apply stats)
                    equipment_manager.equip(equipment, character)
                    
                    print(f"  - {eq_type}: {equipment.name} (HP={character.hp}, DMG={character.damage})")
                else:
                    print(f"  - {eq_type}: {eq_id} (không tìm thấy trong all_equipment)")




# Global instance
_global_equipment_manager = None


def get_global_equipment_manager():
    """Lấy global equipment manager instance"""
    global _global_equipment_manager
    if _global_equipment_manager is None:
        _global_equipment_manager = GlobalEquipmentManager()
    return _global_equipment_manager
