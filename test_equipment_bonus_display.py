"""Test script để kiểm tra hiển thị bonus equipment trong màn chọn nhân vật"""

# Mock các dependencies cần thiết
import sys
import os

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ma_nguon.core import profile_manager
from ma_nguon.doi_tuong.items import EQUIPMENT_DATA

def test_equipment_bonuses():
    """Test lấy equipment bonuses từ profile"""
    
    # Test với user 'test'
    username = 'test'
    
    print("="*60)
    print("TEST HIỂN THỊ BONUS EQUIPMENT")
    print("="*60)
    
    try:
        profile = profile_manager.load_profile(username)
        
        print(f"\nProfile của user '{username}':")
        print(f"  - Gold: {profile.get('gold', 0)}")
        print(f"  - Purchased characters: {profile.get('purchased_characters', [])}")
        
        # Kiểm tra inventory
        inventory = profile.get('equipment_inventory', {})
        print(f"\n  - Equipment inventory: {len(inventory)} loại")
        for item_name, count in inventory.items():
            print(f"    • {item_name}: x{count}")
        
        # Kiểm tra character equipment
        char_equipment = profile.get('character_equipment', {})
        print(f"\n  - Character equipment: {len(char_equipment)} nhân vật")
        
        for char_id, equipment in char_equipment.items():
            print(f"\n    📌 {char_id}:")
            total_bonuses = {'hp': 0, 'damage': 0, 'defense': 0, 'speed': 0}
            
            for slot_type, eq_name in equipment.items():
                eq_data = EQUIPMENT_DATA.get(eq_name)
                if eq_data:
                    hp_bonus = eq_data.get('hp_bonus', 0)
                    atk_bonus = eq_data.get('attack_bonus', 0)
                    def_bonus = eq_data.get('defense_bonus', 0)
                    spd_bonus = eq_data.get('speed_bonus', 0)
                    
                    total_bonuses['hp'] += hp_bonus
                    total_bonuses['damage'] += atk_bonus
                    total_bonuses['defense'] += def_bonus
                    total_bonuses['speed'] += spd_bonus
                    
                    print(f"      • {slot_type}: {eq_name}")
                    if hp_bonus > 0:
                        print(f"        ↳ HP +{hp_bonus}")
                    if atk_bonus > 0:
                        print(f"        ↳ ATK +{atk_bonus}")
                    if def_bonus > 0:
                        print(f"        ↳ DEF +{def_bonus}")
                    if spd_bonus > 0:
                        print(f"        ↳ SPD +{spd_bonus}")
                else:
                    print(f"      • {slot_type}: {eq_name} (KHÔNG TÌM THẤY TRONG EQUIPMENT_DATA)")
            
            print(f"    ✓ Tổng bonus:")
            print(f"      HP: +{total_bonuses['hp']}")
            print(f"      Damage: +{total_bonuses['damage']}")
            print(f"      Defense: +{total_bonuses['defense']}")
            print(f"      Speed: +{total_bonuses['speed']}")
        
        if not char_equipment:
            print("    (Chưa có nhân vật nào được trang bị)")
        
        print("\n" + "="*60)
        print("✓ TEST HOÀN TẤT")
        print("="*60)
        
    except FileNotFoundError:
        print(f"✗ Không tìm thấy profile cho user '{username}'")
        print("  Hãy đăng nhập vào game và trang bị một số items trước")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_equipment_bonuses()
